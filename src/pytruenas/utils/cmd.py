"""CLI argument classes and the command-module contract.

``pytruenas`` commands are plain modules that expose:

* ``run(client, args, logger)`` -- required; the command body, called once per
  target with a connected :class:`~pytruenas.TrueNASClient`.
* ``register(parser, args, logger)`` -- optional; add argparse arguments.
* ``init(args, logger) -> client`` / ``success(client, args, logger)`` /
  ``finally_(client, args, logger)`` -- optional lifecycle hooks.

The app (see :mod:`pytruenas.main`) parses global options into
:class:`PyTrueNASArgs`, then for each target fans out and invokes the selected
command's ``run`` with a per-target client and logger. Argument parsing and
command discovery are provided by :mod:`duho`; the per-target fan-out and the
client/logger threading are ``pytruenas``-specific and live here + in
:mod:`pytruenas.main`.
"""

from __future__ import annotations

import os as _os
import typing as _ty
from logging import Logger as _Logger
from pathlib import Path as _Path

from argparse import SUPPRESS as _SUPPRESS

from duho import Arg, Extend, LoggingArgs, NS

from . import io as _ioutils  # noqa: F401

if _ty.TYPE_CHECKING:
    from ..client import TrueNASClient


def _load_config(path: "_Path") -> dict:
    """Load a YAML config file, or return ``{}`` if it does not exist.

    YAML support is optional (the ``config`` extra); a missing ``pyyaml`` with a
    present config file is a clear, actionable error rather than a silent skip.
    """
    if not path.exists():
        return {}
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - only without the extra
        raise ImportError(
            "reading a config file requires the 'config' extra: "
            "pip install pytruenas[config]"
        ) from exc
    return yaml.safe_load(path.read_text()) or {}


def register_targets(parser) -> None:
    """Add the trailing ``targets`` positional to a command parser.

    Applied centrally -- a command module never calls this itself.
    :func:`pytruenas.main._with_targets` wraps every module command's
    ``register`` hook and calls this *after* it, so the target host(s) are the
    trailing positionals (``pytruenas query <namespace> <host>...``) whatever
    positionals the command added; :class:`~pytruenas.utils.runpath.
    PyTrueNASRunPathArgs` does the same for class/RunPath commands. Targets
    support comma-separated lists and ``[A-Z]``/``[0-9]`` range patterns,
    expanded by ``PyTrueNASArgs._expanded_targets_`` (empty -> ``localhost``).
    """
    parser.add_argument(
        "targets",
        nargs="*",
        metavar="TARGET",
        help="Target host(s) as trailing arguments; comma-separated and "
        "[A-Z]/[0-9] range patterns supported. Defaults to localhost.",
    )


class PyTrueNASArgs(LoggingArgs):
    """Global options shared by every ``pytruenas`` command.

    A data mixin (``LoggingArgs``): it carries the global fields and config
    loading; :class:`pytruenas.main.PyTrueNAS` combines it with ``duho.Cli`` to
    make the runnable app root.
    """

    config: "Arg[dict, NS(type=_Path)]" = _Path(
        _os.environ.get("PYTRUENAS_CFG") or "./pytruenas.yaml"
    )
    "Config file to use"
    ("--config", "-c")  # type: ignore

    cmdspath: "Arg[list[str], Extend(':')]" = []
    "Extra directories/packages to search for commands"
    ("--cmdspath",)  # type: ignore

    sslverify: bool = False
    "Verify the server's TLS certificate"
    ("--sslverify",)  # type: ignore

    # Targets are supplied as the TRAILING POSITIONAL arguments of the command
    # (after any command-specific positionals), not a -t/--target flag. The
    # positional is added centrally, after each command's own register() hook
    # (main._with_targets), so argparse can split e.g. `query <namespace>
    # <host>...` without the command taking part. SUPPRESS keeps duho from
    # auto-registering this field as a `--targets` option; it only holds the
    # parsed value + default, populated by the imperative positional.
    targets: "Arg[list[str], _SUPPRESS]" = []

    parallel: int = 1
    "Number of targets to operate on concurrently"

    logto: str = "-"
    "Where to log: '-' for stderr, or a path template (supports {target}, {isodate})"

    def _config_dict_(self) -> dict:
        """Return the loaded config mapping (empty when the file is absent)."""
        config = self.config
        if isinstance(config, _Path):
            return _load_config(config)
        return config or {}

    def _expanded_targets_(self) -> "list[str]":
        """Return the target list with commas split and range patterns expanded.

        Targets arrive as the trailing positionals (a flat ``list[str]``); each
        item may itself be a comma-separated list (``nas1,nas2``) and/or carry a
        ``[A-Z]``/``[0-9]`` range pattern. An empty list defaults to
        ``localhost``. Flattens defensively in case a nested list slips through.
        """
        from duho import expand

        def _flatten(values):
            for value in values:
                if isinstance(value, (list, tuple)):
                    yield from _flatten(value)
                else:
                    yield value

        items = list(_flatten(self.targets)) or ["localhost"]
        # A single positional may still be a comma-list (nas1,nas2).
        raw = [part for item in items for part in str(item).split(",") if part]
        expanded: "list[str]" = []
        for target in raw:
            expanded.extend(expand(target))
        return expanded


class CommandModule(_ty.Protocol):
    """The attributes the app expects from a command module."""

    def run(self, client: "TrueNASClient", args: PyTrueNASArgs, logger: _Logger) -> object: ...


__all__ = ["PyTrueNASArgs", "CommandModule"]
