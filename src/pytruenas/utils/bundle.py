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

Repo mode (:func:`collect_repo`, :func:`repo_requirements`) is a fourth, PARALLEL
path answering a different question: not "what does an installed distribution
need", but "what would a clone of this working tree have". It copies files as
the tree's own ``.gitignore``/``.ignore``/``.bundleignore`` says to, and reads
declared dependencies straight from ``pyproject.toml``/``requirements.txt`` with
no import and nothing installed. Both feed the same :func:`build`/:func:`export`
sinks as the installed-metadata path -- see those functions' ``contents=``
parameter -- so the output layout (zipapp vs. tree) is identical either way;
only where the file list comes from differs.

Repo mode has its own, OPTIONAL dependency: :func:`collect_repo` needs
``pathspec`` (the ``repo`` extra) for gitignore-accurate pattern matching, and
:func:`repo_requirements` needs a TOML parser -- ``tomllib`` on 3.11+, else
``tomli`` (also in the ``repo`` extra) -- ONLY when reading a ``pyproject.toml``
(a plain ``requirements.txt`` needs neither). Both are imported lazily inside
the functions that need them, so every other function in this module, and
every existing caller, keeps working with nothing extra installed.
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
    "collect_repo",
    "repo_requirements",
    "DEFAULT_IGNORE_FILES",
]

#: The ignore files consulted by default, in the order their patterns are
#: layered. Order matters for gitignore semantics: a later file's negation
#: (``!keep.txt``) can un-ignore something an earlier file ignored, so
#: `.bundleignore` -- the most bundle-specific, and the one most likely to
#: intentionally override the other two -- is applied last.
DEFAULT_IGNORE_FILES = (".gitignore", ".ignore", ".bundleignore")

#: pathspec's registered pattern factory used for every ignore-file line and
#: every ``--ignore-pattern``. ``"gitignore"`` (``GitIgnoreBasicPattern``),
#: not the older ``"gitwildmatch"`` (``GitWildMatchPattern``, deprecated by
#: pathspec as of the version this depends on) -- they are DIFFERENT classes,
#: not a rename, so this was checked for parity on the cases this module
#: actually relies on (negation, a directory-anchored pattern, a nested
#: match) before switching, rather than assumed equivalent from the name.
_PATTERN_FACTORY = "gitignore"

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


#: Always excluded from a repo-mode walk, regardless of any ignore file's
#: content. A repo's own VCS metadata is never part of "the files a clone
#: would have" -- a `.bundleignore` that forgets to say so must not ship it.
_ALWAYS_IGNORED = (".git",)


def _require_pathspec():
    """Import ``pathspec``, or raise the one clear error every repo-mode entry
    point should give when the ``repo`` extra is not installed."""
    try:
        import pathspec
    except ImportError as exc:
        raise BundleError(
            "repo mode requires the 'repo' extra: pip install pytruenas[repo]"
        ) from exc
    return pathspec


def _load_ignore(
    root: "_Path",
    files: "_ty.Sequence[str] | None" = None,
    extra_patterns: "_ty.Sequence[str]" = (),
) -> object:
    """Build one combined ``PathSpec`` from whichever ``files`` exist under ``root``.

    Requires the ``repo`` extra (``pathspec``); imported here, not at module
    level, so plain dependency-closure bundling -- what every existing caller
    does -- keeps working with nothing extra installed. Only a repo-mode call
    pays for it.

    ``files`` defaults to :data:`DEFAULT_IGNORE_FILES`, all three combined. A
    missing file is silently skipped: a repo that only has ``.gitignore``
    should not need an explicit override just to avoid a raised error for
    files it was never going to have.

    ``extra_patterns`` -- a caller's own patterns (e.g. ``--exclude``) -- are
    compiled as a SEPARATE spec and added last via ``PathSpec.__add__``, which
    layers pattern lists rather than merging them into one; that preserves
    gitignore's actual semantics, where a later pattern's negation can
    un-ignore something an earlier one matched. String-concatenating pattern
    text first would work too, but round-trips through each compiled
    pattern's source text for no benefit -- ``__add__`` is the library's own
    supported way to layer specs and is used instead.
    """
    pathspec = _require_pathspec()

    lines: "list[str]" = []
    for name in files if files is not None else DEFAULT_IGNORE_FILES:
        path = root / name
        if path.is_file():
            lines.extend(path.read_text(encoding="utf-8").splitlines())
    spec = pathspec.PathSpec.from_lines(_PATTERN_FACTORY, lines)
    if extra_patterns:
        spec = spec + pathspec.PathSpec.from_lines(_PATTERN_FACTORY, extra_patterns)
    return spec


def collect_repo(
    root: "str | _Path",
    *,
    ignore_files: "_ty.Sequence[str] | None" = None,
    extra_ignores: "_ty.Sequence[str]" = (),
    prefix: "str | None" = None,
) -> "list[tuple[str, _Path]]":
    """``[(arcname, source_path)]`` for a repo tree, filtered like a clone would be.

    The repo-mode counterpart to :func:`_collect`: same output shape, so it
    feeds :func:`build`/:func:`export`/:func:`tar_tree` with no changes to
    those functions beyond accepting a pre-built list (their ``contents=``
    parameter) instead of resolving one from installed metadata.

    ``ignore_files`` selects which ignore file(s) to honour (default: all of
    :data:`DEFAULT_IGNORE_FILES` that exist). ``extra_ignores`` are additional
    gitwildmatch patterns layered AFTER the files -- e.g. a caller's own
    ``--exclude``, which should be able to override what an ignore file says,
    not just add to it. ``.git`` is excluded unconditionally; see
    :data:`_ALWAYS_IGNORED`.

    ``prefix`` names the top-level directory files are arranged under in the
    returned arcnames (default: ``root``'s own directory name) -- matching how
    :func:`_collect` arranges each distribution under its own top-level name,
    so a repo bundle has the same "one recognisable top directory" shape a
    dependency bundle does.

    Directories matched by an ignore pattern are pruned rather than merely
    having their files filtered out one by one: ``rglob`` has already
    descended into a directory by the time a file inside it could be checked,
    so pruning means checking the directory's OWN path (with a trailing slash,
    since gitwildmatch's directory-anchor patterns like ``.venv*/`` only match
    that form) before recursing rather than after.
    """
    # Resolved before anything else: `Path(".").name` is `""`, which would
    # arrange every arcname under a leading "/" instead of a real top
    # directory -- exactly the "." a caller runs this from is the common case.
    root = _Path(root).resolve()
    if not root.is_dir():
        raise BundleError(f"{root} is not a directory")
    spec = _load_ignore(root, ignore_files, extra_ignores)
    name = prefix if prefix is not None else root.name

    def _ignored(relative: str, *, is_dir: bool) -> bool:
        parts = _Path(relative).parts
        if parts and parts[0] in _ALWAYS_IGNORED:
            return True
        candidate = relative + "/" if is_dir else relative
        return spec.match_file(candidate)

    contents: "list[tuple[str, _Path]]" = []

    def _walk(directory: "_Path") -> None:
        for child in sorted(directory.iterdir()):
            relative = child.relative_to(root).as_posix()
            if child.is_dir():
                if _ignored(relative, is_dir=True):
                    continue
                _walk(child)
            elif child.is_file():
                if _ignored(relative, is_dir=False):
                    continue
                contents.append((f"{name}/{relative}", child))
            # Anything else (a symlink to nowhere, a socket, ...) is skipped:
            # neither a directory to descend into nor a file to ship.

    _walk(root)
    return contents


def _toml_loader():
    """``tomllib``/``tomli``'s ``loads``, or ``None`` if neither is importable.

    ``tomllib`` (stdlib, 3.11+) is tried first so a modern interpreter never
    reaches for the optional dependency it does not need; ``tomli`` (the
    ``repo`` extra's fallback below 3.11) is tried second. Returning ``None``
    rather than raising here lets a caller reading ``requirements.txt`` --
    which needs no TOML parser at all -- proceed with no dependency on either.
    """
    try:
        import tomllib

        return tomllib.loads
    except ImportError:
        pass
    try:
        import tomli

        return tomli.loads
    except ImportError:
        return None


def _dependency_name(raw: str) -> str:
    """The bare distribution name from one PEP 508 requirement string.

    Degrades the same way :func:`requirements` does when ``packaging`` is
    absent (bundle.py:118-121): a plain split on the marker/extras/version
    delimiters. Good enough for a name; not a substitute for real parsing if
    the caller needs the marker or the extras too.
    """
    try:
        from packaging.requirements import Requirement

        return Requirement(raw).name
    except ImportError:  # pragma: no cover - packaging ships with pip/setuptools
        return raw.split(";")[0].split("[")[0].split("=")[0].split("<")[0].split(
            ">"
        )[0].split("~")[0].strip()


def _parse_pyproject(
    text: str, extras: "_ty.Sequence[str]", *, include_base: bool = True
) -> "list[str]":
    """Dependency names from a ``pyproject.toml``'s ``[project]`` table.

    Only the PEP 621 fields this needs are read -- ``dependencies`` and the
    requested keys of ``optional-dependencies`` -- not a general TOML->object
    mapping of the whole file.

    ``include_base`` (default ``True``) includes ``[project.dependencies]``
    alongside any requested ``extras``. The primary :func:`repo_requirements`
    call wants both together; resolving what ONE extra alone contributes (for
    an ``[extra]``-bracketed ``include``/``exclude`` -- see there) needs
    ``include_base=False``, or a base dependency shared with no extra at all
    would be wrongly attributed to it. This bit BEFORE the fix: excluding
    ``[ssh]`` removed every core dependency too, because "what ssh
    contributes" was computed as base-plus-ssh rather than ssh alone.
    """
    loads = _toml_loader()
    if loads is None:
        raise BundleError(
            "reading dependencies from pyproject.toml requires a TOML parser: "
            "install the 'repo' extra (pip install pytruenas[repo]) on Python "
            "< 3.11, or use Python 3.11+ where tomllib is built in"
        )
    data = loads(text)
    project = data.get("project", {})
    names = (
        [_dependency_name(raw) for raw in project.get("dependencies", [])]
        if include_base
        else []
    )
    optional = project.get("optional-dependencies", {})
    for extra in extras:
        for raw in optional.get(extra, []):
            names.append(_dependency_name(raw))
    return names


def _parse_requirements_txt(text: str) -> "list[str]":
    """Dependency names from a ``requirements.txt``-style file.

    Handles what actually appears in one of these: comments (``#``), blank
    lines, and per-line PEP 508 requirement strings. Deliberately does NOT
    follow ``-r other.txt``/``-c constraints.txt`` includes or ``-e``/VCS
    lines -- those name other files or non-index sources, not a distribution
    this function can return a name for, and silently skipping them would
    misreport what the repo actually depends on. A caller needing those
    should read the file themselves; this covers the common case.
    """
    names: "list[str]" = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        names.append(_dependency_name(line))
    return names


def repo_requirements(
    root: "str | _Path",
    extras: "_ty.Sequence[str]" = (),
    *,
    include: "_ty.Sequence[str]" = (),
    exclude: "_ty.Sequence[str]" = (),
) -> "list[str]":
    """Declared dependency NAMES from ``pyproject.toml`` or ``requirements.txt``.

    The static counterpart to :func:`requirements`: no import, and nothing
    needs to be installed. ``pyproject.toml`` is preferred when present (its
    ``[project.dependencies]``, plus ``[project.optional-dependencies]`` for
    each requested ``extras`` entry); ``requirements.txt`` is the fallback.

    This does NOT resolve a transitive closure or return ``Distribution``
    objects the way :func:`requirements` does -- that needs the packages
    installed, which is exactly what this function exists to avoid requiring.
    It answers "what does this repo declare", for a caller to act on directly
    (e.g. writing the names into a ``requirements.txt`` the TARGET's own pip
    resolves, rather than vendoring the packages here).

    ``include``/``exclude`` accept a plain distribution name (``"requests"``)
    or a bracketed extra name (``"[ssh]"``) -- the same syntax
    ``deploy.py``'s ``--include``/``--exclude`` flags take, resolved here so
    both a CLI caller and a library caller get identical behaviour. An
    extras-bracket ``include`` re-reads that extra's dependencies from the
    same source even if it was not in ``extras``; a plain-name ``include`` is
    added as a literal name with no version/marker information, since there is
    nowhere else to resolve one from. ``exclude`` is applied LAST and always
    wins, even over an ``include`` naming the same thing -- an explicit "never
    ship this" should not be silently overridable by an equally explicit
    "ship this".
    """
    root = _Path(root)
    pyproject = root / "pyproject.toml"
    reqtxt = root / "requirements.txt"

    if pyproject.is_file():
        names = _parse_pyproject(
            pyproject.read_text(encoding="utf-8"), extras
        )
    elif reqtxt.is_file():
        names = _parse_requirements_txt(reqtxt.read_text(encoding="utf-8"))
    else:
        raise BundleError(
            f"no pyproject.toml or requirements.txt found under {root}"
        )

    result = list(dict.fromkeys(names))  # de-duplicate, keep first occurrence
    for item in include:
        if item.startswith("[") and item.endswith("]"):
            extra = item[1:-1]
            if pyproject.is_file():
                for extra_name in _parse_pyproject(
                    pyproject.read_text(encoding="utf-8"),
                    (extra,),
                    include_base=False,
                ):
                    if extra_name not in result:
                        result.append(extra_name)
            # A requirements.txt has no concept of extras; a bracketed
            # --include against one names nothing and is silently a no-op,
            # matching how an --extra the target format cannot express is
            # handled elsewhere in this module (missing_on's `skip`, etc).
        elif item not in result:
            result.append(item)

    excluded_names = {item for item in exclude if not item.startswith("[")}
    excluded_extras = {
        item[1:-1] for item in exclude if item.startswith("[") and item.endswith("]")
    }
    if excluded_extras and pyproject.is_file():
        for extra in excluded_extras:
            for extra_name in _parse_pyproject(
                pyproject.read_text(encoding="utf-8"),
                (extra,),
                include_base=False,
            ):
                excluded_names.add(extra_name)
    result = [name for name in result if name not in excluded_names]
    return result


def export(
    destination: "str | _Path",
    distributions: "_ty.Mapping[str, object] | None" = None,
    *,
    contents: "_ty.Sequence[tuple[str, _Path]] | None" = None,
) -> "_Path":
    """Write a file set as an unpacked tree under ``destination``.

    The directory counterpart of :func:`build`: same file set, laid out as
    importable packages rather than zipped, for a deployment that should be
    readable and editable on the target.

    Exactly one of ``distributions`` (resolved through :func:`_collect`, the
    installed-metadata path every existing caller uses) or ``contents`` (an
    already-built ``[(arcname, source_path)]`` list -- what
    :func:`collect_repo` returns) must be given. Accepting either here, rather
    than writing a separate repo-mode export function, is what lets ``--mode
    dir`` behave identically regardless of ``--source``: the zip/tree-writing
    code is the same code either way, only where the file list came from
    differs.
    """
    import shutil

    if (distributions is None) == (contents is None):
        raise TypeError("pass exactly one of distributions= or contents=")
    if contents is None:
        contents = _collect(_ty.cast("_ty.Mapping[str, object]", distributions))

    destination = _Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for arcname, source in contents:
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
    distributions: "_ty.Mapping[str, object] | None" = None,
    package: "str | None" = None,
    interpreter: "str | None" = "/usr/bin/env python3",
    *,
    contents: "_ty.Sequence[tuple[str, _Path]] | None" = None,
) -> "_Path":
    """Write a zipapp containing a file set and return its path.

    ``package`` is the import name the zipapp runs when executed -- the
    caller's own package when this library is bundled as a dependency of it.
    Required rather than defaulted: the wrong entry point produces a bundle
    that builds and then does nothing useful.

    ``interpreter`` becomes the ``#!`` line so the file is directly executable;
    pass ``None`` for a plain zip to be run as ``python3 bundle.pyz``.

    Compiled artifacts and caches are excluded: ``__pycache__`` is per-version
    and would be stale on the target anyway, and ``.pyc`` outside it is dead
    weight.

    Exactly one of ``distributions`` or ``contents`` must be given -- see
    :func:`export`'s docstring for why both exist on the same function rather
    than a separate repo-mode zipapp builder.
    """
    if package is None:
        raise TypeError("package is required")
    if (distributions is None) == (contents is None):
        raise TypeError("pass exactly one of distributions= or contents=")
    if contents is None:
        contents = _collect(_ty.cast("_ty.Mapping[str, object]", distributions))

    destination = _Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

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
