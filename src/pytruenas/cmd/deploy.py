"""Install pytruenas (or the package built on it) on a target, then run it there.

TrueNAS has a read-only root and no pip, so only what the target lacks is
bundled, and it is installed under /var/db/system, which survives an update.
--mode pyz (default) installs one zipapp; --mode dir an unpacked tree.
--source repo (with --mode dir) copies a working tree instead of the installed
packages. Anything after -- runs on the target once installed, e.g.
`pytruenas deploy nas1 -- query user`.
"""

# hostctl.deploy.deploy does the bundling: it asks the target what it already
# has and copies the difference, atomically and only when the digest changed.
# TrueNAS 26.0 already ships requests, websocket-client, pyyaml, asyncssh,
# jinja2 and packaging, so the bundle is a few pure-Python packages. This module
# is the policy around it: what to deploy, where, the .pyz name, and running it.
#
# --mode pyz is one file to copy, verify and replace; --mode dir is readable on
# the target (editable in place, greppable, can carry data alongside). --source
# repo needs --mode dir: a zipapp needs its package at the archive root, which a
# src/-layout copy does not have. Its own dependencies are not vendored;
# --include/--exclude only adjust the names it logs as a heads-up.
#
# /var/db/system is the mountpoint of the <pool>/.system dataset on a data pool,
# so it survives an update; /var/db itself lives in the boot environment
# (boot-pool/ROOT/<version>/var) and is replaced by one.

from __future__ import annotations

import shlex
import typing as _ty
from logging import Logger

from duho import Arg, Meta

from pytruenas import TrueNASClient
from pytruenas.utils.cmd import PyTrueNASArgs
from pytruenas.utils.target import redact

#: The command to run on the target once installed comes after `--`.
_allow_passthrough_ = True

#: Under the persistent system dataset -- see the module docstring for why this
#: and not ``/var/db``, ``/root`` or ``/data`` (all in the boot environment).
DEFAULT_PREFIX = "/var/db/system/pytruenas"

#: The interpreter on the target: the appliance's middleware runs on it, so it
#: is always present, and pinning a version would break on the next release.
REMOTE_PYTHON = "python3"


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``deploy``."""

    path: "Arg[str, Meta(metavar='PATH')]" = DEFAULT_PREFIX
    """Where to install on the target. Defaults to a location on the
    persistent system dataset, which survives a TrueNAS update."""
    ("--path",)  # type: ignore

    mode: "Arg[str, Meta(choices=('pyz', 'dir'), metavar='MODE')]" = "pyz"
    "Layout to install: a single executable zipapp, or an unpacked tree"
    ("--mode",)  # type: ignore

    pkg_root: "Arg[str, Meta(metavar='DIST')]" = ""
    """Distribution to deploy, with its dependencies (default: the
    PYTRUENAS_PKG_ROOT environment variable, else pytruenas itself). Set this
    when pytruenas is a *dependency* of the thing being deployed."""
    ("--pkg-root",)  # type: ignore

    pkg_name: "Arg[str, Meta(metavar='PACKAGE')]" = ""
    """Package the deployed bundle runs (default: PYTRUENAS_PKG_NAME, else the
    root's name). Only needed when the distribution and import names differ."""
    ("--pkg-name",)  # type: ignore

    extras: "Arg[list[str], Meta(metavar='EXTRA')]" = []
    "Include an extra's dependencies in the bundle (repeatable)"
    ("--extra",)  # type: ignore

    skip: "Arg[list[str], Meta(metavar='DIST')]" = []
    "Never bundle this distribution, even if the target lacks it (repeatable)"
    ("--skip",)  # type: ignore

    force: bool = False
    "Reinstall even when the target already has this exact bundle"
    ("--force",)  # type: ignore

    source: "Arg[str, Meta(choices=('installed', 'repo'), metavar='SOURCE')]" = (
        "installed"
    )
    """Where the bundled content comes from: the installed dependency closure
    (default), or a repo working tree copied as-is, filtered by ignore files.
    `repo` requires `--mode dir`: a zipapp needs an importable package root."""
    ("--source",)  # type: ignore

    repo_root: "Arg[str, Meta(metavar='PATH')]" = "."
    "Repo directory to copy, for --source repo (default: the current directory)"
    ("--repo-root",)  # type: ignore

    ignore_files: "Arg[list[str], Meta(metavar='FILE')]" = []
    """Ignore file(s) to apply for --source repo (repeatable; default:
    .gitignore, .ignore, and .bundleignore, whichever exist)."""
    ("--ignore-file",)  # type: ignore

    ignore_pattern: "Arg[list[str], Meta(metavar='PATTERN')]" = []
    """An extra gitignore-style pattern for --source repo, applied AFTER the
    ignore file(s) -- so it can exclude something they keep, or (with a
    leading '!') un-ignore something they exclude (repeatable)."""
    ("--ignore-pattern",)  # type: ignore

    include: "Arg[list[str], Meta(metavar='NAME')]" = []
    """Include a dependency or '[extra]' in the names --source repo LOGS as a
    heads-up (repeatable) -- it does not vendor anything or change which files
    are copied. Has no effect on --source installed."""
    ("--include",)  # type: ignore

    exclude: "Arg[list[str], Meta(metavar='NAME')]" = []
    """Exclude a dependency or '[extra]' from that same logged list, overriding
    --include (repeatable). Has no effect on --source installed -- use --skip
    there instead."""
    ("--exclude",)  # type: ignore

    pythonpath: "Arg[list[str], Meta(metavar='DIR')]" = []
    """Directory (relative to --repo-root) to put on PYTHONPATH for --source
    repo, so the launcher can find the package (repeatable; default: whichever
    of src/, lib/, vendor/, and the repo root itself contain an importable
    <package>, checked in that order)."""
    ("--pythonpath",)  # type: ignore


def _resolve_root(
    root: "str | None" = None, package: "str | None" = None
) -> "tuple[str, str]":
    """Decide what is being deployed: ``(distribution_name, package_name)``.

    pytruenas is normally a dependency, not the deliverable: the usual caller
    has their own package that imports pytruenas, and what they want on the
    appliance is *their* package with pytruenas bundled underneath. So the
    closure root is nameable, and falls back to pytruenas only when nothing
    else says otherwise. Highest first: the arguments (``--pkg-root`` /
    ``--pkg-name``), then ``PYTRUENAS_PKG_ROOT`` / ``PYTRUENAS_PKG_NAME``, then
    ``pytruenas``; the package defaults to the root with ``-`` as ``_``.
    """
    from pytruenas.utils.cmd import ENV

    root = root or ENV.get("PKG_ROOT") or "pytruenas"
    package = package or ENV.get("PKG_NAME") or root.replace("-", "_")
    return root, package


def _target(args: Args) -> str:
    """The install path: ``--path``, named as a ``.pyz`` file for a zipapp."""
    target = args.path.rstrip("/") or args.path
    if args.mode == "pyz" and not target.endswith(".pyz"):
        target = f"{target}.pyz"
    return target


def _source(args: Args) -> object:
    """``--source installed``'s distribution name, or ``--source repo``'s tree."""
    from hostctl.deploy import SourceTree

    root, _ = _resolve_root(args.pkg_root or None, args.pkg_name or None)
    if args.source != "repo":
        return root
    return SourceTree(
        args.repo_root,
        ignore_files=args.ignore_files or None,
        ignore_patterns=tuple(args.ignore_pattern or ()),
        pythonpath=args.pythonpath or None,
    )


def _log_declared(tree: _ty.Any, args: Args, logger: Logger) -> None:
    """Name what a repo tree declares but does not ship, after the filters."""
    from hostctl.exceptions import BundleError

    try:
        declared = tree.requirements(
            tuple(args.extras or ()),
            include=tuple(args.include or ()),
            exclude=tuple(args.exclude or ()),
        )
    except BundleError as exc:
        logger.debug("Could not read declared dependencies: %s", exc)
        return
    if declared:
        logger.info(
            "Repo declares %d dependenc%s (not vendored -- ensure the target "
            "can resolve them): %s",
            len(declared),
            "y" if len(declared) == 1 else "ies",
            ", ".join(sorted(declared)),
        )


def _passthrough(args: Args) -> "list[str]":
    """Arguments after ``--``, to run on the target after installing.

    duho captures them on the parsed instance as ``_passthrough_``.
    """
    return list(getattr(args, "_passthrough_", ()) or ())


_REPO_PYZ = (
    "--source repo does not support --mode pyz: a zipapp needs the package at "
    "the archive root, which a src/-layout repo copy does not have. Use --mode "
    "dir, whose launcher can PYTHONPATH into src/lib/vendor directly."
)


def validate_args(args: Args) -> None:
    """Refuse what the arguments alone show cannot work, before any target runs.

    Raises :class:`duho.UsageError` (exit status 2, reported once rather than
    once per target).
    """
    from duho import UsageError

    if args.source == "repo" and args.mode == "pyz":
        raise UsageError(_REPO_PYZ)
    if not args.path.startswith("/"):
        raise UsageError(f"--path must be absolute on the target: {args.path!r}")


def run(client: TrueNASClient, args: Args, logger: Logger):
    from hostctl import Exec
    from hostctl.deploy import deploy
    from hostctl.exceptions import BundleError

    if args.source == "repo" and args.mode == "pyz":
        # Before anything reaches the target, for a caller that runs this
        # without the CLI's validate_args.
        raise BundleError(_REPO_PYZ)
    root, package = _resolve_root(args.pkg_root or None, args.pkg_name or None)
    if root != "pytruenas":
        logger.info("Deploying %s (running %s)", root, package)
    source = _source(args)
    if args.source == "repo":
        _log_declared(source, args, logger)

    deployment = deploy(
        client,
        _ty.cast(_ty.Any, source),
        _target(args),
        mode=args.mode,
        package=package,
        extras=tuple(args.extras or ()),
        skip=tuple(args.skip or ()),
        force=bool(args.force),
        python=REMOTE_PYTHON,
    )
    logger.info(
        "%s at %s", "Deployed" if deployment.written else "Verified", deployment.path
    )

    extra = _passthrough(args)
    if not extra:
        return 0
    command = [*deployment.command, *extra]
    # The deployed command may name another host with its password; the log
    # line shows it without, and the command itself is run as given.
    shown = " ".join(shlex.quote(redact(part)) for part in command)
    logger.info("Running: %s", shown)
    return client.run(Exec(*command), check=False).returncode
