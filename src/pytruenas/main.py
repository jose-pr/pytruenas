"""The ``pytruenas`` command-line application.

Builds a subcommand app from discovered command modules, parses global options
into :class:`~pytruenas.utils.cmd.PyTrueNASArgs`, then runs the selected command
against every target -- optionally several targets concurrently -- giving each
run its own connected :class:`~pytruenas.TrueNASClient` and a per-target logger.

Argument parsing and command discovery come from :mod:`duho`; the multi-target
fan-out and the client/logger threading are ``pytruenas``-specific.
"""

from __future__ import annotations

import argparse as _argparse
import datetime as _dt
import logging as _pylogging
import os as _os
import socket as _socket
import sys as _sys
import typing as _ty
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path as _Path

from duho import Cli
from duho import logging as _logging
from duho.discovery import ModuleCommand, discover_commands

from .client import TrueNASClient
from .utils.cmd import PyTrueNASArgs

#: Third-party loggers to quiet by default (chatty at INFO/DEBUG).
DEFAULT_LOGLEVELS = {
    "requests": _pylogging.WARNING,
    "urllib3": _pylogging.WARNING,
    "websocket": _pylogging.WARNING,
    "asyncssh": _pylogging.WARNING,
}

#: Package-relative import path to the built-in command modules.
_BUILTIN_COMMANDS = "pytruenas.cmd"


class PyTrueNAS(PyTrueNASArgs, Cli):
    """Utility tool to manage and configure TrueNAS systems."""

    _version_ = "0.1.0"


def _command_modules(extra_paths: "_ty.Sequence[str]") -> "dict[str, ModuleCommand]":
    """Discover command modules (built-ins first, then configured paths).

    Later sources override earlier ones on a name clash so a user command can
    shadow a built-in of the same name.
    """
    sources: "list[str]" = [
        _BUILTIN_COMMANDS,
        *(_os.environ.get("PYTRUENAS_PATH", "").split(_os.pathsep) if _os.environ.get("PYTRUENAS_PATH") else []),
        *extra_paths,
    ]
    commands: "dict[str, ModuleCommand]" = {}
    for source in sources:
        if not source:
            continue
        for command in discover_commands(source):
            if isinstance(command, ModuleCommand):
                commands[command._parsername_] = command
    return commands


def _target_label(target: str) -> str:
    """A short '<host>|local|remote' label for per-target logger names."""
    host = target.split("@", 1)[1] if "@" in target else target
    host = host.split("/", 1)[0] or "localhost"
    if host in ("localhost", "127.0.0.1", ""):
        return f"{_socket.gethostname()}|local"
    return f"{host}|remote"


def _run_one_target(
    command: "ModuleCommand",
    args: "PyTrueNAS",
    target: str,
    root_logger: "_pylogging.Logger",
) -> None:
    """Run ``command`` against a single ``target`` with its own client + logger."""
    label = _target_label(target)
    logger = _pylogging.getLogger(f"{root_logger.name} [{label}]")
    logger.setLevel(root_logger.level)

    if args.logto and args.logto != "-":
        now = _dt.datetime.now()
        handler: _pylogging.Handler = _pylogging.FileHandler(
            args.logto.format(target=target, isodate=now.isoformat())
        )
    else:
        handler = _pylogging.StreamHandler(_sys.stderr)
    handler.setFormatter(_logging.DefaultFormatter())
    logger.addHandler(handler)

    module = command.module
    init = getattr(module, "init", None)
    success = getattr(module, "success", None)
    finally_ = getattr(module, "finally_", None)

    logger.info("Started: %s", target)
    client = None
    try:
        if callable(init):
            client = init(args, logger)
        if client is None:
            client = TrueNASClient(target, sslverify=args.sslverify)
        module.run(client, args, logger)
        if callable(success):
            success(client, args, logger)
    except Exception:
        logger.error("Failed: %s", target, exc_info=True)
    finally:
        if callable(finally_):
            try:
                finally_(client, args, logger)
            except Exception:
                logger.error("Cleanup failed: %s", target, exc_info=True)
        logger.info("Finished: %s", target)
        logger.removeHandler(handler)


def main(
    name: "str | None" = None,
    argv: "_ty.Sequence[str] | None" = None,
) -> int:
    """Build the app, parse ``argv``, and run the selected command per target."""
    name = name or "pytruenas"
    root_logger = _pylogging.getLogger(name)
    if not _pylogging.getLogger().handlers:
        _logging.init_stderr_logging()

    # A pre-parse of just the global options resolves config-driven command
    # search paths before the full subcommand parser is built.
    pre_parser = PyTrueNAS._parser_(add_help=False)
    pre_parser.add_argument("_command", nargs="?")
    pre_args, _ = pre_parser.parse_known_args(argv)
    config = pre_args._config_dict_()
    extra_paths = list(pre_args.cmdspath or []) + list(config.get("commandspath") or [])

    commands = _command_modules(extra_paths)

    parser = PyTrueNAS._parser_(name=name, description=PyTrueNAS.__doc__)
    subparsers = parser.add_subparsers(title="command", dest="_command", required=True)
    for cmd_name, command in sorted(commands.items()):
        sub = subparsers.add_parser(
            cmd_name.replace("_", "-"),
            help=command.help,
            description=command.description,
            add_help=True,
        )
        register = getattr(command.module, "register", None)
        if callable(register):
            register(sub, pre_args, root_logger)

    args = parser.parse_args(argv)
    args._set_loglevels_()
    for logger_name, level in DEFAULT_LOGLEVELS.items():
        _pylogging.getLogger(logger_name).setLevel(level)

    selected = getattr(args, "_command", None)
    command = commands.get(selected) or commands.get((selected or "").replace("-", "_"))
    if command is None:
        parser.error(f"unknown command: {selected}")
        return 2

    targets = args._expanded_targets_()
    root_logger.info("Running '%s' on %d target(s)", selected, len(targets))

    parallel = max(1, args.parallel)
    if parallel == 1 or len(targets) == 1:
        for target in targets:
            _run_one_target(command, args, target, root_logger)
    else:
        with ThreadPoolExecutor(max_workers=parallel) as pool:
            for target in targets:
                pool.submit(_run_one_target, command, args, target, root_logger)
    return 0
