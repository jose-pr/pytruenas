"""Build a self-contained bundle of a distribution and the deps a target lacks.

Deliberately generic: this module knows nothing about pytruenas, TrueNAS, or
any particular transport. It answers one question -- "given a distribution
installed here and a list of what is installed there, what has to be shipped,
and how is it laid out?" -- so it can be reused, or lifted into its own
package, without dragging a client library behind it. Policy (which
distribution, where it goes, how the bytes travel) belongs to the caller; see
:mod:`pytruenas.cmd.deploy` for one.

The point is bootstrapping a host that cannot install for itself: no ``pip``, a
read-only root, or no outbound network. What works there is a zipapp -- a zip
of pure-Python packages with a ``__main__.py``, which CPython runs directly off
``sys.path`` -- or the same file set unpacked as a plain tree.

Three steps, each deliberately dumb:

1. **What do we need?** Read the installed distribution metadata
   (:func:`requirements`), not the source. Declared dependencies resolve
   transitively and already account for extras and environment markers;
   walking imports would re-derive that badly -- ``import yaml`` does not name
   ``pyyaml``, and a lazily-imported module inside a function body is invisible
   to a naive scan.
2. **What does the target already have?** Ask it (:data:`PROBE_SOURCE`), rather
   than assume. A TrueNAS 26.0 appliance already ships ``requests``,
   ``websocket-client``, ``pyyaml``, ``asyncssh``, ``jinja2`` and the whole
   ``requests`` transitive set -- and which ones varies by release, which is
   why it is asked. The probe is stdlib-only for exactly this reason: it has to
   run before anything is installed.
3. **Ship the difference** (:func:`build` for a zipapp, :func:`export` for a
   tree).

A distribution containing a compiled extension is refused rather than silently
shipped: a ``.so`` built for the local interpreter and platform will not load
on a different one, and failing at build time with a clear message beats an
``ImportError`` after deployment.
"""

from __future__ import annotations

import typing as _ty
import zipfile as _zipfile
from pathlib import Path as _Path

__all__ = [
    "PROBE_SOURCE",
    "BundleError",
    "requirements",
    "missing_on",
    "build",
    "export",
    "tar_tree",
    "tar_digest",
    "default_package",
]

#: Distributions never worth shipping: they are either part of the standard
#: library's tooling surface or present on any interpreter that can run the
#: probe at all.
_NEVER_BUNDLE = frozenset({"pip", "setuptools", "wheel", "pkg-resources"})

#: Stdlib-only source run *on the target* to list installed distributions.
#:
#: Kept as source text rather than a module so it can be fed to a remote
#: ``python3 -`` over any transport, before pytruenas exists there. It prints
#: one normalized distribution name per line; the caller diffs.
PROBE_SOURCE = """\
import sys
try:
    from importlib.metadata import distributions
except ImportError:  # pragma: no cover - Python < 3.8
    sys.exit("probe requires Python 3.8+")
seen = set()
for dist in distributions():
    name = (dist.metadata["Name"] or "").strip()
    if name:
        seen.add(name.lower().replace("_", "-"))
for name in sorted(seen):
    print(name)
"""


class BundleError(RuntimeError):
    """Raised when a bundle cannot be built correctly."""


def _canonical(name: str) -> str:
    """PEP 503 normalization, enough for matching distribution names."""
    return name.lower().replace("_", "-").replace(".", "-")


def default_package(root: str) -> str:
    """The import name to assume for a distribution named ``root``.

    ``my-tool`` -> ``my_tool``: right for the overwhelmingly common case where
    the two match. They genuinely can differ (a ``tnas-config`` distribution
    may install a ``tnasconfig`` package), which is why the two are separate
    parameters everywhere rather than one -- guessing wrong produces a bundle
    that builds and then cannot import.
    """
    return root.replace("-", "_")


def requirements(root: str, extras: "_ty.Sequence[str]" = ()) -> "dict[str, object]":
    """Resolve ``root``'s full transitive dependency closure, from metadata.

    Returns ``{canonical_name: Distribution}``, including ``root`` itself. A
    dependency that is declared but not installed is skipped with no error:
    the closure describes what *this* environment can contribute, and an
    uninstalled optional dependency is simply not ours to ship.

    ``extras`` selects declared extras (``("ssh",)``); by default only the core
    requirements are followed, since an extra the caller did not ask for should
    not silently enlarge the payload.
    """
    from importlib.metadata import PackageNotFoundError, distribution

    try:
        from packaging.requirements import Requirement
    except ImportError:  # pragma: no cover - packaging ships with pip/setuptools
        Requirement = None  # type: ignore[assignment]

    found: "dict[str, object]" = {}
    pending = [root]
    while pending:
        name = pending.pop()
        key = _canonical(name)
        if key in found or key in _NEVER_BUNDLE:
            continue
        try:
            dist = distribution(name)
        except PackageNotFoundError:
            continue
        found[key] = dist
        for raw in dist.requires or []:
            if Requirement is None:  # pragma: no cover - degraded fallback
                pending.append(raw.split(";")[0].split("[")[0].strip())
                continue
            requirement = Requirement(raw)
            marker = requirement.marker
            if marker is not None:
                # An extra-gated requirement is included only when that extra
                # was asked for. Evaluating with extra="" answers the plain
                # environment markers (python_version, sys_platform).
                contexts = [{"extra": extra} for extra in extras] or []
                contexts.append({"extra": ""})
                if not any(marker.evaluate(ctx) for ctx in contexts):
                    continue
            pending.append(requirement.name)
    return found


def _top_level_paths(dist) -> "list[_Path]":
    """The importable files/dirs a distribution installs, as real paths."""
    base = getattr(dist, "_path", None)
    anchor = _Path(base).parent if base else None
    tops: "set[str]" = set()

    text = dist.read_text("top_level.txt")
    if text:
        tops.update(line.strip() for line in text.splitlines() if line.strip())
    if not tops:
        # No top_level.txt (common for modern wheels): derive it from RECORD.
        for file in dist.files or []:
            parts = _Path(str(file)).parts
            if not parts:
                continue
            first = parts[0]
            # RECORD lists installed-file paths RELATIVE TO site-packages, and
            # they may escape it: a console script is `../../Scripts/foo.exe`.
            # Taking parts[0] blindly yields "..", which resolves to the parent
            # of site-packages -- so the whole tree gets scanned and any stray
            # compiled artifact there is misattributed to this distribution.
            # (That is not hypothetical: it made a mypyc `.pyd` belonging to
            # black look like part of hostctl.)
            if first in {"..", "."} or first.endswith(
                (".dist-info", ".egg-info", ".pth")
            ):
                continue
            tops.add(first[:-3] if first.endswith(".py") else first)

    paths: "list[_Path]" = []
    for top in sorted(tops):
        if anchor is not None:
            package = anchor / top
            module = anchor / f"{top}.py"
            # `is_dir()` alone is not enough: an uninstall can leave a stale
            # directory of the right name with no `__init__.py` behind, and
            # taking it would bundle a package that cannot be imported (or,
            # worse, an OLD copy shadowing the real one). Require the marker
            # that makes it a package before believing it.
            if (package / "__init__.py").is_file():
                paths.append(package)
                continue
            if module.is_file():
                paths.append(module)
                continue
        # Not beside the metadata. That is the normal shape of an EDITABLE
        # install: its RECORD lists only a `.pth` shim (plus any force-included
        # data file), and the real package lives in the source tree the `.pth`
        # points at. Resolving it by import is the only way to find it, and
        # getting this wrong is quiet -- the bundle builds, and only fails at
        # `import` on the target, with a package that looked present locally.
        located = _locate_by_import(top)
        if located is not None:
            paths.append(located)
    return paths


def _locate_by_import(top: str) -> "_Path | None":
    """Find an importable top-level name's real file, without importing it."""
    import importlib.util

    try:
        spec = importlib.util.find_spec(top)
    except (ImportError, ValueError):  # pragma: no cover - unimportable name
        return None
    if spec is None or not spec.origin or spec.origin == "built-in":
        return None
    origin = _Path(spec.origin)
    # A package's origin is its __init__.py; ship the directory that contains
    # it. A single-file module ships as itself.
    return origin.parent if origin.name == "__init__.py" else origin


def _reject_native(name: str, paths: "_ty.Iterable[_Path]") -> None:
    """Refuse a distribution carrying a compiled extension.

    A ``.so``/``.pyd`` is built for one interpreter version and platform. Ship
    one to an appliance and it fails at import, long after the operation that
    could have explained why -- so fail here instead, where the message can.
    """
    for path in paths:
        if path.is_dir():
            native = [
                str(child.relative_to(path))
                for child in path.rglob("*")
                if child.suffix in {".so", ".pyd", ".dll"}
            ]
        else:
            native = [path.name] if path.suffix in {".so", ".pyd", ".dll"} else []
        if native:
            raise BundleError(
                f"{name!r} contains a compiled extension ({native[0]}) and cannot "
                "be bundled: it is built for this interpreter and platform, and "
                "would fail to import on the target. Install it on the target by "
                "other means and exclude it with --skip."
            )


def missing_on(
    installed: "_ty.Iterable[str]",
    root: str,
    extras: "_ty.Sequence[str]" = (),
    skip: "_ty.Iterable[str]" = (),
) -> "dict[str, object]":
    """The closure entries that ``installed`` does not already provide.

    ``installed`` is what :data:`PROBE_SOURCE` printed on the target. The
    comparison is on canonical names, so ``pathlib_next`` and ``pathlib-next``
    are one package.
    """
    have = {_canonical(name) for name in installed}
    have.update(_canonical(name) for name in skip)
    return {
        key: dist for key, dist in requirements(root, extras).items() if key not in have
    }


def _collect(
    distributions: "_ty.Mapping[str, object]",
) -> "list[tuple[str, _Path]]":
    """``[(arcname, source_path)]`` for every file the bundle should carry.

    Shared by :func:`build` and :func:`export` so the two layouts can never
    disagree about what "the bundle" contains -- only about how it is written.

    ``__pycache__`` and loose ``.pyc``/``.pyo`` are dropped: they are specific
    to the building interpreter's version, so on the target they would be
    ignored at best and stale at worst.
    """
    contents: "list[tuple[str, _Path]]" = []
    for name, dist in sorted(distributions.items()):
        paths = _top_level_paths(dist)
        if not paths:
            raise BundleError(
                f"cannot locate the installed files for {name!r}: its metadata "
                "lists no importable top-level package, and none could be "
                "imported by name"
            )
        # A distribution that contributes only data files would build a bundle
        # that imports nothing -- which is what an editable install looked like
        # before `_locate_by_import`: `pytruenas` shipped as a lone README.md
        # and failed with ModuleNotFoundError on the target. Fail here instead,
        # where the cause is still visible.
        if not any(path.is_dir() or path.suffix == ".py" for path in paths):
            raise BundleError(
                f"{name!r} resolved to data files only ({paths[0].name}) with no "
                "importable module; the bundle would not be able to import it"
            )
        _reject_native(name, paths)
        for path in paths:
            if path.is_dir():
                for child in sorted(path.rglob("*")):
                    if not child.is_file() or "__pycache__" in child.parts:
                        continue
                    if child.suffix in {".pyc", ".pyo"}:
                        continue
                    contents.append(
                        (f"{path.name}/{child.relative_to(path).as_posix()}", child)
                    )
            else:
                contents.append((path.name, path))
    return contents


def export(
    destination: "str | _Path", distributions: "_ty.Mapping[str, object]"
) -> "_Path":
    """Write ``distributions`` as an unpacked tree under ``destination``.

    The directory counterpart of :func:`build`: same file set, laid out as
    importable packages rather than zipped, for a deployment that should be
    readable and editable on the target.
    """
    import shutil

    destination = _Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for arcname, source in _collect(distributions):
        target = destination / arcname
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return destination


def tar_tree(
    path: "str | _Path", executable_dirs: "_ty.Sequence[str]" = ("bin",)
) -> bytes:
    """Tar a directory in memory with ownership and modes normalized.

    For shipping :func:`export`'s output as one transfer. Everything is owned by
    uid/gid 0 and given a deterministic mode -- 0755 for directories and for
    files directly under ``executable_dirs``, 0644 otherwise -- so the archive
    does not carry the building machine's user ids or umask onto the target,
    and so a launcher script arrives runnable. (Windows in particular has no
    POSIX permission bits to preserve, so *something* has to decide them.)

    Caches are skipped for the same reason :func:`_collect` drops them: they
    belong to the building interpreter.
    """
    import io as _io
    import tarfile as _tarfile

    topdir = _Path(path)
    executable = {directory.strip("/") for directory in executable_dirs}
    fileobj = _io.BytesIO()

    def _filter(tarinfo: "_tarfile.TarInfo"):
        relative = tarinfo.name[len(topdir.name) :].lstrip("/")
        parts = relative.split("/") if relative else []
        if "__pycache__" in parts or relative.endswith((".pyc", ".pyo")):
            return None
        tarinfo.uid = tarinfo.gid = 0
        tarinfo.uname = tarinfo.gname = "root"
        if tarinfo.isdir():
            tarinfo.mode = 0o755
        elif len(parts) == 2 and parts[0] in executable:
            tarinfo.mode = 0o755
        else:
            tarinfo.mode = 0o644
        return tarinfo

    with _tarfile.open(fileobj=fileobj, mode="w") as tar:
        tar.add(topdir.as_posix(), topdir.name, filter=_filter)
    return fileobj.getvalue()


def tar_digest(
    path: "str | _Path", executable_dirs: "_ty.Sequence[str]" = ("bin",)
) -> "tuple[str, bytes]":
    """``(sha256_hex, tar_bytes)`` for :func:`tar_tree`.

    The digest is over the archive, which :func:`tar_tree` makes deterministic
    for a given tree -- so a caller can record it on the target and skip the
    whole transfer next time when it still matches.
    """
    import hashlib as _hashlib

    content = tar_tree(path, executable_dirs)
    return _hashlib.sha256(content).hexdigest(), content


#: The zipapp entry point, parameterized by the package to launch.
#:
#: ``runpy`` rather than a direct ``from <pkg>.main import main``: the entry
#: point of the caller's own package is theirs to define, and ``-m`` semantics
#: (``__main__.py``, or ``main()`` via whatever they expose) is the one
#: convention every Python package already agrees on. Hardcoding
#: a specific module path only works while that package *is* the deliverable.
_MAIN_TEMPLATE = """\
import runpy
import sys

sys.argv[0] = {package!r}
runpy.run_module({package!r}, run_name="__main__", alter_sys=True)
"""


def build(
    destination: "str | _Path",
    distributions: "_ty.Mapping[str, object]",
    package: str,
    interpreter: "str | None" = "/usr/bin/env python3",
) -> "_Path":
    """Write a zipapp containing ``distributions`` and return its path.

    ``package`` is the import name the zipapp runs when executed -- the
    caller's own package when this library is bundled as a dependency of it.
    Required rather than defaulted: the wrong entry point produces a bundle
    that builds and then does nothing useful.

    ``interpreter`` becomes the ``#!`` line so the file is directly executable;
    pass ``None`` for a plain zip to be run as ``python3 bundle.pyz``.

    Compiled artifacts and caches are excluded: ``__pycache__`` is per-version
    and would be stale on the target anyway, and ``.pyc`` outside it is dead
    weight.
    """
    destination = _Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    contents = _collect(distributions)

    raw = destination.with_suffix(destination.suffix + ".tmp")
    with _zipfile.ZipFile(raw, "w", _zipfile.ZIP_DEFLATED) as archive:
        for arcname, source in contents:
            archive.write(source, arcname)
        archive.writestr("__main__.py", _MAIN_TEMPLATE.format(package=package))

    # Prepend the shebang by hand rather than using `zipapp.create_archive`:
    # the sources here are individual files from several distributions, not one
    # directory, which is the only shape zipapp accepts.
    payload = raw.read_bytes()
    raw.unlink()
    with open(destination, "wb") as handle:
        if interpreter:
            handle.write(f"#!{interpreter}\n".encode())
        handle.write(payload)
    destination.chmod(0o755)
    return destination
