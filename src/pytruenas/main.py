"""The ``pytruenas`` command-line application.

Thin driver over :func:`duho.app`: ``app`` owns command discovery, parser build,
per-command ``register``, config/env layering, parsing and logging setup; the one
piece it hands off is *dispatch*, which pytruenas overrides to run the selected
command against every target positional -- concurrently, via :mod:`duho.fanout` --
giving each target its own connected :class:`~pytruenas.TrueNASClient`.

A pytruenas command module exposes ``run(client, args, logger)`` (client-first,
called once per target) plus optional ``register``/``init``/``success``/
``finally_`` hooks. That client-first contract is why dispatch calls the module's
``run`` itself rather than duho's ``run_command`` (which passes only ``args``).
"""

from __future__ import annotations

import datetime as _dt
import logging as _pylogging
import os as _os
import typing as _ty

from duho import AUTO, Cli, app, parse_globals
from duho import logging as _logging
from duho.discovery import ModuleCommand, discover_commands
from duho.fanout import run_targets

from .client import TrueNASClient
from .utils.cmd import PyTrueNASArgs

#: Third-party loggers to quiet by default (chatty at INFO/DEBUG).
DEFAULT_LOGLEVELS = {
    "requests": _pylogging.WARNING,
    "urllib3": _pylogging.WARNING,
    "websocket": _pylogging.WARNING,
    "asyncssh": _pylogging.WARNING,
}

#: Package import path to the built-in command modules.
_BUILTIN_COMMANDS = "pytruenas.cmd"


class PyTrueNAS(PyTrueNASArgs, Cli):
    """Utility tool to manage and configure TrueNAS systems."""

    # Resolve --version from the installed package metadata (single source of
    # truth: pyproject's version), rather than duplicating the literal here.
    _version_ = AUTO
    _distribution_ = "pytruenas"


def _discover(argv: "_ty.Sequence[str] | None") -> "list":
    """Resolve the command set: built-ins, then env/CLI/config-provided paths.

    Uses :func:`duho.parse_globals` to read the config-file / ``--cmdspath`` /
    ``PYTRUENAS_PATH`` globals *before* the full subcommand parser is built. Later
    sources win on a name clash (a user command shadows a built-in), then the list
    is de-duplicated by subcommand name preserving that precedence.
    """
    globals_ = parse_globals(PyTrueNAS, argv)
    config = globals_._config_dict_()
    sources: "list[str]" = [_BUILTIN_COMMANDS]
    if _os.environ.get("PYTRUENAS_PATH"):
        sources += _os.environ["PYTRUENAS_PATH"].split(_os.pathsep)
    sources += list(globals_.cmdspath or [])
    sources += list(config.get("commandspath") or [])

    by_name: "dict[str, object]" = {}
    for source in sources:
        if not source:
            continue
        for command in discover_commands(source):
            name = getattr(command, "_parsername_", None) or getattr(command, "__name__", None)
            if name:
                by_name[name] = command  # later source wins
    return list(by_name.values())


def _run_module_on_target(
    command: "ModuleCommand",
    args: "PyTrueNAS",
    target: str,
    logger: "_pylogging.Logger",
) -> int:
    """Run one module command against one target; return an exit code.

    Builds the client (module ``init`` if present, else a plain
    :class:`TrueNASClient`) and runs the module lifecycle ``run`` +
    ``success``/``finally_``. Records are already ``[target]``-prefixed by
    ``duho.fanout`` (a ``TargetPrefixFilter`` installed for the fan-out), so no
    per-target logger/handler naming is needed here. When ``--logto`` is a path
    template a per-target :class:`~logging.FileHandler` is attached for the run
    (fanout tags the message but does not route files).
    """
    module = command.module
    init = getattr(module, "init", None)
    success = getattr(module, "success", None)
    finally_ = getattr(module, "finally_", None)

    file_handler = None
    if args.logto and args.logto != "-":
        now = _dt.datetime.now()
        file_handler = _pylogging.FileHandler(
            args.logto.format(target=target, isodate=now.isoformat())
        )
        file_handler.setFormatter(_logging.DefaultFormatter())
        logger.addHandler(file_handler)

    logger.info("Started: %s", target)
    client = None
    result = 0
    try:
        if callable(init):
            client = init(args, logger)
        if client is None:
            client = TrueNASClient(target, sslverify=args.sslverify)
        rc = module.run(client, args, logger)
        result = 0 if rc is None else int(rc)
        if callable(success):
            success(client, args, logger)
    finally:
        if callable(finally_):
            try:
                finally_(client, args, logger)
            except Exception:
                logger.error("Cleanup failed: %s", target, exc_info=True)
        logger.info("Finished: %s", target)
        if file_handler is not None:
            logger.removeHandler(file_handler)
            file_handler.close()
    return result


def _dispatch(command: object, instance: "PyTrueNAS") -> int:
    """duho ``app`` dispatch seam: fan the selected command over the targets.

    For a module command (every built-in), run it once per target positional via
    :func:`duho.fanout.run_targets` (thread pool sized by ``--parallel``, per-target
    ``[target]`` log prefixing, worst exit code wins). A class command (none today)
    falls back to duho's own single dispatch.
    """
    logger = instance._logger_
    for name, level in DEFAULT_LOGLEVELS.items():
        _pylogging.getLogger(name).setLevel(level)

    if not isinstance(command, ModuleCommand):
        from duho import run_command

        return run_command(_ty.cast(_ty.Any, command), instance)

    targets = instance._expanded_targets_()
    logger.info("Running '%s' on %d target(s)", command._parsername_, len(targets))
    return run_targets(
        lambda target: _run_module_on_target(command, instance, target, logger),
        targets,
        max_workers=max(1, instance.parallel),
        logger=logger,
    )


def main(
    name: "str | None" = None,
    argv: "_ty.Sequence[str] | None" = None,
) -> int:
    """Build the app, parse ``argv``, and run the selected command per target."""
    name = name or "pytruenas"
    return app(
        PyTrueNAS,
        commands=_discover(argv),
        argv=argv,
        name=name,
        description=PyTrueNAS.__doc__,
        dispatch=_dispatch,
    )
