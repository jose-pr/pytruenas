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

Everything after ``--`` is passed to the deployed copy and run there, so a
single invocation can install and use it::

    pytruenas deploy nas1                      # install only
    pytruenas deploy nas1 -- query user        # install, then run remotely
    pytruenas deploy --mode dir nas1 -- call system.info

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


def run(client: TrueNASClient, args: Args, logger: Logger):
    from pytruenas.utils import bundle as _bundle

    dist_root, package = _resolve_root(
        getattr(args, "pkg_root", "") or None, getattr(args, "pkg_name", "") or None
    )
    if dist_root != "pytruenas":
        logger.info("Deploying %s (running %s)", dist_root, package)

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
            local = _bundle.build(Path(tmp) / "bundle.pyz", missing, package=package)
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
            _bundle.export(root / "lib", missing)
            (root / "bin").mkdir()
            # write_bytes, not write_text: on Windows text mode rewrites "\n"
            # as "\r\n", which turns the shebang into "#!/bin/sh\r" and makes
            # the launcher fail on the target with "bad interpreter" -- naming
            # a path that visibly exists.
            (root / "bin" / package).write_bytes(
                _LAUNCHER_TEMPLATE.format(package=package).encode()
            )
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
