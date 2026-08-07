"""Install pytruenas onto a target so it can run there, then optionally run it.

TrueNAS has a read-only root and no ``pip``, so the usual "install it on the
box" answer does not apply. This command bootstraps instead: it asks the target
what it already has, bundles only the difference, and copies that over.

That probe is the interesting part. TrueNAS 26.0 already ships ``requests``,
``websocket-client``, ``pyyaml``, ``asyncssh``, ``jinja2`` and the whole
``requests`` transitive set, so a full vendored payload would be mostly
redundant -- and *which* packages are present varies by release, which is why
it is asked rather than assumed. In practice the bundle is five pure-Python
packages, well under a megabyte.

Two layouts, ``--mode``:

* ``pyz`` (default) -- one executable zipapp. A single file to copy, verify and
  replace, which makes it the better default for "just make the command work".
* ``dir`` -- an unpacked tree, for when the deployment needs to be *readable*
  on the target: editable in place, greppable, and able to carry extra data or
  templates alongside the code.

Orthogonal to ``--mode`` is ``--source``, which decides where the bundled
CONTENT comes from:

* ``installed`` (default) -- the dependency-closure path above: what this
  environment has installed, probed against what the target already has.
* ``repo`` -- copy a repo working tree as-is (``--repo-root``, default the
  current directory), filtered by whichever of ``.gitignore``/``.ignore``/
  ``.bundleignore`` exist (``--ignore-file`` narrows the selection,
  ``--ignore-pattern`` adds more patterns on the command line). This does
  **not** vendor the repo's own dependencies -- that needs them installed
  here, which is exactly what repo mode exists to avoid requiring -- so it is
  for shipping source to be read, edited, or run by an interpreter that
  already has (or can reach) what the repo declares. ``--include``/
  ``--exclude`` (a bare name or a bracketed ``[extra]``) only affect the
  dependency names LOGGED as a heads-up, not which files are copied.

  Only ``--mode dir`` supports ``--source repo``: a zipapp needs its package
  importable at the archive root, which a ``src/``-layout repo copy does not
  have. ``--mode dir``'s launcher instead puts every directory a package was
  found under (``src/``, ``lib/``, ``vendor/``, or the repo root itself,
  auto-detected -- or named explicitly with ``--pythonpath``) on
  ``PYTHONPATH``.

Everything after ``--`` is passed to the deployed copy and run there, so a
single invocation can install and use it::

    pytruenas deploy nas1                      # install only
    pytruenas deploy nas1 -- query user        # install, then run remotely
    pytruenas deploy --mode dir nas1 -- call system.info
    pytruenas deploy --source repo --mode dir nas1 -- call system.info

The default destination is under ``/var/db/system``. That is deliberate and was
verified on a live appliance: ``/var/db/system`` is the mountpoint of the
``<pool>/.system`` dataset on a *data* pool, so it survives an update, whereas
``/var/db`` itself lives in the boot environment
(``boot-pool/ROOT/<version>/var``) and is replaced by one. Writable, and
persistent for the right reason rather than by luck.
"""

from __future__ import annotations

import hashlib
import shlex
import typing as _ty
from logging import Logger
from pathlib import Path, PurePosixPath

from duho import Arg, NS

from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs

#: Under the persistent system dataset -- see the module docstring for why this
#: and not ``/var/db``, ``/root`` or ``/data`` (all in the boot environment).
DEFAULT_PREFIX = "/var/db/system/pytruenas"

#: Where the digest of the deployed tree is recorded, relative to the target
#: directory. Lets a redeploy answer "is what is already there current?"
#: without hashing the remote tree file by file.
DIGEST_NAME = ".digest"


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``deploy``."""

    path: "Arg[str, NS(metavar='PATH')]" = DEFAULT_PREFIX
    """Where to install on the target. Defaults to a location on the
    persistent system dataset, which survives a TrueNAS update."""
    ("--path",)  # type: ignore

    mode: "Arg[str, NS(choices=('pyz', 'dir'), metavar='MODE')]" = "pyz"
    "Layout to install: a single executable zipapp, or an unpacked tree"
    ("--mode",)  # type: ignore

    pkg_root: "Arg[str, NS(metavar='DIST')]" = ""
    """Distribution to deploy, with its dependencies (default: the
    PYTRUENAS_PKG_ROOT environment variable, else pytruenas itself). Set this
    when pytruenas is a *dependency* of the thing being deployed."""
    ("--pkg-root",)  # type: ignore

    pkg_name: "Arg[str, NS(metavar='PACKAGE')]" = ""
    """Package the deployed bundle runs (default: PYTRUENAS_PKG_NAME, else the
    root's name). Only needed when the distribution and import names differ."""
    ("--pkg-name",)  # type: ignore

    extras: "Arg[list[str], NS(metavar='EXTRA')]" = []
    "Include an extra's dependencies in the bundle (repeatable)"
    ("--extra",)  # type: ignore

    skip: "Arg[list[str], NS(metavar='DIST')]" = []
    "Never bundle this distribution, even if the target lacks it (repeatable)"
    ("--skip",)  # type: ignore

    force: bool = False
    "Reinstall even when the target already has this exact bundle"
    ("--force",)  # type: ignore

    source: "Arg[str, NS(choices=('installed', 'repo'), metavar='SOURCE')]" = "installed"
    """Where the bundled content comes from: the installed dependency closure
    (default), or a repo working tree copied as-is, filtered by ignore files.
    Orthogonal to --mode, which decides the OUTPUT layout either way."""
    ("--source",)  # type: ignore

    repo_root: "Arg[str, NS(metavar='PATH')]" = "."
    "Repo directory to copy, for --source repo (default: the current directory)"
    ("--repo-root",)  # type: ignore

    ignore_files: "Arg[list[str], NS(metavar='FILE')]" = []
    """Ignore file(s) to apply for --source repo (repeatable; default:
    .gitignore, .ignore, and .bundleignore, whichever exist)."""
    ("--ignore-file",)  # type: ignore

    ignore_pattern: "Arg[list[str], NS(metavar='PATTERN')]" = []
    """An extra gitignore-style pattern for --source repo, applied AFTER the
    ignore file(s) -- so it can exclude something they keep, or (with a
    leading '!') un-ignore something they exclude (repeatable)."""
    ("--ignore-pattern",)  # type: ignore

    include: "Arg[list[str], NS(metavar='NAME')]" = []
    """Include a dependency or '[extra]' in the names --source repo LOGS as a
    heads-up (repeatable) -- it does not vendor anything or change which files
    are copied. Has no effect on --source installed."""
    ("--include",)  # type: ignore

    exclude: "Arg[list[str], NS(metavar='NAME')]" = []
    """Exclude a dependency or '[extra]' from that same logged list, overriding
    --include (repeatable). Has no effect on --source installed -- use --skip
    there instead."""
    ("--exclude",)  # type: ignore

    pythonpath: "Arg[list[str], NS(metavar='DIR')]" = []
    """Directory (relative to --repo-root) to put on PYTHONPATH for --source
    repo, so the launcher can find the package (repeatable; default: whichever
    of src/, lib/, vendor/, and the repo root itself contain an importable
    <package>, checked in that order)."""
    ("--pythonpath",)  # type: ignore


def _resolve_root(
    root: "str | None" = None, package: "str | None" = None
) -> "tuple[str, str]":
    """Decide what is being deployed: ``(distribution_name, package_name)``.

    This is *policy* and lives here rather than in
    :mod:`~pytruenas.utils.bundle`, which is deliberately agnostic about who is
    using it.

    pytruenas is normally a dependency, not the deliverable. The usual caller
    has their own package -- ``tnasconfig`` -- that imports pytruenas, and what
    they want on the appliance is *their* package with pytruenas bundled
    underneath. So the closure root has to be nameable, and falls back to
    pytruenas only when nothing else says otherwise.

    Resolution order, highest first:

    1. the explicit arguments (``--pkg-root`` / ``--pkg-name``);
    2. ``PYTRUENAS_PKG_ROOT`` / ``PYTRUENAS_PKG_NAME``, so a project sets it
       once in its own tooling instead of at every call;
    3. ``pytruenas`` itself.
    """
    from pytruenas.utils.bundle import default_package
    from pytruenas.utils.cmd import ENV

    root = root or ENV.get("PKG_ROOT") or "pytruenas"
    package = package or ENV.get("PKG_NAME") or default_package(root)
    return root, package


def _remote_python(client: TrueNASClient) -> str:
    """The interpreter to drive on the target.

    ``python3`` by name: the appliance's own middleware runs on it, so it is
    always present and on PATH, and pinning a version here would break on the
    next release that moves.
    """
    return "python3"


def _probe(client: TrueNASClient, logger: Logger) -> "list[str]":
    """Ask the target which distributions it already has."""
    from pytruenas.utils.bundle import PROBE_SOURCE

    logger.info("Probing installed packages")
    result = client.run(
        f"{_remote_python(client)} -",
        input=PROBE_SOURCE,
        capture_output="stdout",
        encoding="utf-8",
        check=True,
    )
    installed = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    logger.debug("target reports %d installed distributions", len(installed))
    return installed


def _ensure_parent(client: TrueNASClient, target: str) -> None:
    """Create ``target``'s parent directory if it is missing.

    Guarded by an ``exists()`` check rather than relying on
    ``mkdir(exist_ok=True)``: the SFTP backend surfaces an existing directory as
    a bare ``OSError: Failure`` from the server, which ``exist_ok`` never sees
    and which says nothing useful about what went wrong.

    ``PurePosixPath``, never ``Path``: the target is POSIX regardless of what
    the machine running this is, and ``Path("/var/db/x").parent`` on Windows
    yields ``\\var\\db`` -- a path that does not exist remotely, so the guard
    would pass and the mkdir would then fail on a mangled name.
    """
    parent = client.path(str(PurePosixPath(target).parent))
    if not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)


def _current_digest(client: TrueNASClient, marker: str) -> "str | None":
    """The digest recorded by a previous deploy, or ``None`` if absent."""
    try:
        path = client.path(marker)
        if not path.exists():
            return None
        return path.read_text().strip() or None
    except Exception:
        # A missing or unreadable marker means "no usable prior deploy"; it must
        # never turn into a failure, since the fix is simply to deploy again.
        return None


def _deploy_pyz(
    client: TrueNASClient,
    payload: bytes,
    digest: str,
    target: str,
    args: Args,
    logger: Logger,
) -> bool:
    """Install a single zipapp. Returns whether anything was written."""
    marker = f"{target}.digest"
    if not args.force and _current_digest(client, marker) == digest:
        logger.info("Already current (%s); nothing to do", digest[:12])
        return False

    _ensure_parent(client, target)
    logger.info("Writing %s (%d bytes)", target, len(payload))
    client.path(target).write_bytes(payload)
    # argv as a list, not a shell string: no quoting to get wrong, and no shell
    # involved to reinterpret a path that happens to contain a metacharacter.
    client.run(["chmod", "755", target], check=True)
    # Bytes, so a Windows controller does not write "\r\n" into a file that
    # lives on a POSIX host (see the launcher below).
    client.path(marker).write_bytes(f"{digest}\n".encode())
    return True


def _deploy_dir(
    client: TrueNASClient,
    payload: bytes,
    digest: str,
    target: str,
    args: Args,
    logger: Logger,
) -> bool:
    """Install an unpacked tree from a tar payload. Returns whether it wrote."""
    marker = f"{target}/{DIGEST_NAME}"
    if not args.force and _current_digest(client, marker) == digest:
        logger.info("Already current (%s); nothing to do", digest[:12])
        return False

    staging = f"{target}.incoming.tar"
    _ensure_parent(client, target)
    logger.info("Uploading %d bytes to %s", len(payload), target)
    client.path(staging).write_bytes(payload)

    # Unpack beside the target and swap, so an interrupted transfer never
    # leaves a half-written tree at a path something may already be running
    # from. Each step is its own argv list -- no shell, so nothing here depends
    # on how a path would be quoted. The sequencing that a `&&` chain provided
    # comes from check=True instead: the first failure raises.
    incoming, previous = f"{target}.new", f"{target}.old"
    client.run(["rm", "-rf", incoming, previous], check=True)
    client.run(["mkdir", "-p", incoming], check=True)
    client.run(
        ["tar", "-xf", staging, "-C", incoming, "--strip-components=1"], check=True
    )
    if client.path(target).exists():
        client.run(["mv", target, previous], check=True)
    client.run(["mv", incoming, target], check=True)
    client.run(["rm", "-rf", previous, staging], check=True)

    # Bytes, so a Windows controller does not write "\r\n" into a file that
    # lives on a POSIX host (see the launcher below).
    client.path(marker).write_bytes(f"{digest}\n".encode())
    return True


def _passthrough(args: Args) -> "list[str]":
    """Arguments after ``--``, to run on the target after installing.

    Read from :data:`pytruenas.main.PASSTHROUGH`, which is split off before
    argparse runs -- see there for why an argparse field cannot express this.
    """
    from pytruenas.main import PASSTHROUGH

    return list(PASSTHROUGH)


#: Directories checked, in order, for an importable ``<package>`` when
#: ``--pythonpath`` is not given explicitly. Covers the common Python project
#: layouts: PEP 517 ``src/``, a vendored ``lib/`` or ``vendor/`` tree, and the
#: package sitting directly at the repo root (the flat layout).
_PYTHONPATH_CANDIDATES = ("src", "lib", "vendor", "")


def _detect_pythonpath(repo_root: "Path", package: str) -> "list[str]":
    """Which of :data:`_PYTHONPATH_CANDIDATES` actually contain ``package``.

    Checked locally, against the repo tree being bundled -- not guessed at
    launch time on the target, which cannot see this machine's layout anyway.
    A directory counts if it holds ``<package>/__init__.py`` or
    ``<package>.py``, the same two shapes :func:`~pytruenas.utils.bundle.
    _top_level_paths` already recognises for an installed distribution.

    Returns every match rather than the first: a repo that vendors under
    ``lib/`` while its own code lives in ``src/`` needs both on PYTHONPATH,
    and there is no way to tell that apart from "only take the first hit"
    without ALSO breaking the (more common) single-layout case.
    """
    found: "list[str]" = []
    for candidate in _PYTHONPATH_CANDIDATES:
        base = repo_root / candidate if candidate else repo_root
        if (base / package / "__init__.py").is_file() or (
            base / f"{package}.py"
        ).is_file():
            found.append(candidate)
    return found


class _RepoContents(_ty.NamedTuple):
    files: "list[tuple[str, Path]]"
    #: Relative-to-repo-root directories to arrange onto PYTHONPATH; see
    #: `_detect_pythonpath`/`--pythonpath`.
    pythonpath: "list[str]"


def _repo_contents(args: Args, package: str, logger: Logger) -> "_RepoContents":
    """Build --source repo's file list, its PYTHONPATH entries, and log a
    dependency heads-up.

    Copies the repo tree as-is (:func:`~pytruenas.utils.bundle.collect_repo`).
    Deliberately does NOT vendor the repo's own dependencies alongside it --
    that needs a resolved transitive closure, which requires those
    dependencies to be INSTALLED here (:func:`~pytruenas.utils.bundle.
    requirements`), the exact thing repo mode exists to avoid needing. So a
    caller wanting a fully self-contained pyz from a repo still uses
    ``--source installed`` (the default); this mode is for the read-only-root
    workflow of shipping source to be *read*, edited, or run by an interpreter
    that already has (or can reach) what it declares.

    ``--include``/``--exclude`` only affect the dependency NAMES this logs,
    via :func:`~pytruenas.utils.bundle.repo_requirements` -- they do not
    change which files are copied. `--ignore-pattern` is what affects that.
    """
    from pytruenas.utils import bundle as _bundle

    root = Path(args.repo_root)
    logger.info("Collecting repo tree from %s", root)
    contents = _bundle.collect_repo(
        root,
        ignore_files=args.ignore_files or None,
        extra_ignores=tuple(args.ignore_pattern or ()),
    )
    logger.info("Repo tree: %d files", len(contents))

    pythonpath = list(args.pythonpath or ())
    if not pythonpath:
        pythonpath = _detect_pythonpath(root, package)
        if not pythonpath:
            raise _bundle.BundleError(
                f"could not find an importable {package!r} under {root} "
                f"(checked {', '.join(c or '.' for c in _PYTHONPATH_CANDIDATES)}"
                f"); pass --pythonpath to say where it lives"
            )
        logger.debug("Detected PYTHONPATH entries: %s", ", ".join(pythonpath) or ".")

    try:
        declared = _bundle.repo_requirements(
            root,
            extras=tuple(args.extras or ()),
            include=tuple(args.include or ()),
            exclude=tuple(args.exclude or ()),
        )
    except _bundle.BundleError as exc:
        # Advisory only -- a repo with neither pyproject.toml nor
        # requirements.txt (or no TOML parser available) still ships fine;
        # this is a heads-up, not a requirement of the copy succeeding.
        logger.debug("Could not read declared dependencies: %s", exc)
    else:
        if declared:
            logger.info(
                "Repo declares %d dependenc%s (not vendored -- ensure the "
                "target can resolve them): %s",
                len(declared),
                "y" if len(declared) == 1 else "ies",
                ", ".join(sorted(declared)),
            )
    return _RepoContents(contents, pythonpath)


def run(client: TrueNASClient, args: Args, logger: Logger):
    from pytruenas.utils import bundle as _bundle

    dist_root, package = _resolve_root(
        getattr(args, "pkg_root", "") or None, getattr(args, "pkg_name", "") or None
    )
    if dist_root != "pytruenas":
        logger.info("Deploying %s (running %s)", dist_root, package)

    source = getattr(args, "source", "installed")
    if source == "repo" and args.mode == "pyz":
        # A zipapp needs the package importable at the ZIP ROOT (that is how
        # zipimport works); collect_repo keeps a repo's own src/lib/vendor
        # layout intact instead of flattening it there, which is what
        # --mode dir's multi-entry PYTHONPATH is for. Reject rather than
        # silently produce a zipapp that cannot import anything.
        raise _bundle.BundleError(
            "--source repo does not support --mode pyz: a zipapp needs the "
            "package at the archive root, which a src/-layout repo copy does "
            "not have. Use --mode dir, whose launcher can PYTHONPATH into "
            "src/lib/vendor directly."
        )

    contents: "list[tuple[str, Path]] | None" = None
    pythonpath: "list[str]" = []
    missing: "dict[str, object]" = {}
    if source == "repo":
        contents, pythonpath = _repo_contents(args, package, logger)
    else:
        installed = _probe(client, logger)
        missing = _bundle.missing_on(
            installed,
            root=dist_root,
            extras=tuple(args.extras or ()),
            skip=tuple(args.skip or ()),
        )
        if not missing:
            logger.info("Target already provides every dependency")
        else:
            logger.info("Bundling %s", ", ".join(sorted(missing)))

    target = args.path
    if args.mode == "pyz":
        # A zipapp is one file; name it as one even if a directory was given.
        if not target.endswith(".pyz"):
            target = f"{target}.pyz"
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            if contents is not None:
                local = _bundle.build(
                    Path(tmp) / "bundle.pyz", contents=contents, package=package
                )
            else:
                local = _bundle.build(
                    Path(tmp) / "bundle.pyz", missing, package=package
                )
            payload = local.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        wrote = _deploy_pyz(client, payload, digest, target, args, logger)
        entry = [_remote_python(client), target]
    else:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            # PurePosixPath for the remote name (see _ensure_parent); Path for
            # the local staging dir, which really is this machine's flavour.
            root = Path(tmp) / PurePosixPath(target).name
            (root / "lib").mkdir(parents=True)
            if contents is not None:
                _bundle.export(root / "lib", contents=contents)
            else:
                _bundle.export(root / "lib", missing)
            (root / "bin").mkdir()
            # write_bytes, not write_text: on Windows text mode rewrites "\n"
            # as "\r\n", which turns the shebang into "#!/bin/sh\r" and makes
            # the launcher fail on the target with "bad interpreter" -- naming
            # a path that visibly exists.
            if pythonpath:
                # collect_repo arranges everything under one prefix (the
                # repo's own directory name) inside lib/, so each PYTHONPATH
                # entry needs that prefix -- lib/<repo-name>/src, not lib/src.
                repo_prefix = Path(args.repo_root).resolve().name
                entries = ":".join(
                    f"$here/lib/{repo_prefix}/{entry}" if entry else f"$here/lib/{repo_prefix}"
                    for entry in pythonpath
                )
                launcher = _REPO_LAUNCHER_TEMPLATE.format(
                    package=package, pythonpath=entries
                )
            else:
                launcher = _LAUNCHER_TEMPLATE.format(package=package)
            (root / "bin" / package).write_bytes(launcher.encode())
            # tar_tree normalizes ownership and marks bin/* executable, so the
            # launcher arrives runnable without a follow-up chmod.
            digest, payload = _bundle.tar_digest(root)
        wrote = _deploy_dir(client, payload, digest, target, args, logger)
        entry = [f"{target}/bin/{package}"]

    logger.info("%s at %s", "Deployed" if wrote else "Verified", target)

    extra = _passthrough(args)
    if not extra:
        return 0

    command = [*entry, *extra]
    logger.info("Running: %s", " ".join(shlex.quote(part) for part in command))
    result = client.run(command, check=False)
    return result.returncode


#: ``bin/<package>`` for the unpacked layout: put the sibling ``lib`` on the
#: path and hand off. A shell wrapper rather than a Python script so the
#: interpreter is chosen at run time on the target, and ``-m`` so the deployed
#: package's own entry point decides what running it means.
_LAUNCHER_TEMPLATE = """\
#!/bin/sh
here=$(cd "$(dirname "$0")/.." && pwd)
PYTHONPATH="$here/lib:$PYTHONPATH" exec python3 -m {package} "$@"
"""

#: The --source repo counterpart of `_LAUNCHER_TEMPLATE`. Puts EVERY detected
#: PYTHONPATH entry on the path (see `_detect_pythonpath`) rather than one
#: `lib` directory -- a repo copy is not flattened into one importable root
#: the way `_collect` arranges an installed distribution, so `src/`, `lib/`,
#: and `vendor/` may all need to be reachable at once.
_REPO_LAUNCHER_TEMPLATE = """\
#!/bin/sh
here=$(cd "$(dirname "$0")/.." && pwd)
PYTHONPATH="{pythonpath}:$PYTHONPATH" exec python3 -m {package} "$@"
"""
