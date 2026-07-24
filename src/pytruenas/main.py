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

import copy as _copy
import datetime as _dt
import logging as _pylogging
import os as _os
import typing as _ty

import duho.runpath as _runpath
from duho import AUTO, Cli, app, parse_globals
from duho import logging as _logging
from duho.discovery import CmdBuilder, ModuleCommand, discover_commands
from duho.fanout import run_targets
from duho.runpath import RunPathCmd, is_runpath_dir

from .client import TrueNASClient
from .utils.cmd import PyTrueNASArgs, register_targets
from .utils.runpath import PyTrueNASRunPathArgs
from .utils.target import redact as _redact

# ``import duho.runpath`` auto-registers the RunPath command provider with its
# default base (``duho.LoggingArgs``). Re-register with pytruenas's own shared
# root so every RunPath command built from here inherits PyTrueNASArgs's OWN
# methods (``_expanded_targets_``, ``_config_dict_``, the target fields) as real
# members, not just argparse ``parents=`` data-field copies -- the parsed
# RunPathCmd instance that reaches ``_dispatch`` must be able to answer
# ``_expanded_targets_()`` to drive the per-target fan-out below. The
# PyTrueNASRunPathArgs subclass additionally registers the trailing ``targets``
# positional (SUPPRESS-ed on a plain class command), so ``pytruenas <flow>
# <host>...`` grammar matches the module commands. Re-registering with a new
# base on an already-active provider is documented as supported (it updates the
# base for commands built from then on).
_runpath.register(base=PyTrueNASRunPathArgs)

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


def _commands_from_source(source: str) -> "list":
    """Yield the commands one source contributes, RunPath directories included.

    ``duho.discover_commands`` resolves a package name or a directory of loose
    ``*.py`` command files, but it does NOT consult the RunPath command provider
    for a *directory* shape -- it only globs ``*.py`` files, so a RunPath
    directory (numbered ``NN-name.py`` steps, no ``__init__.py``) handed to it is
    mis-parsed step-by-step into loose module commands, and a RunPath directory
    nested inside a source directory is never inspected at all. Restoring the
    predecessor's RunPath support therefore needs this discovery-side seam, not
    only the ``_dispatch`` fan-out branch:

    * a source that IS a RunPath directory -> build it as ONE RunPath command via
      :class:`duho.discovery.CmdBuilder` (which consults the provider), NOT
      ``discover_commands`` (which would mis-parse its steps);
    * a source directory whose immediate children include RunPath directories ->
      build each such child as its own RunPath command, and still run
      ``discover_commands`` on the parent for any ordinary loose command files
      beside them;
    * anything else (a dotted package, a directory of loose command files) ->
      plain ``discover_commands``, unchanged.

    A source that resolves to neither an existing directory nor an importable
    package (a stray ``--cmdspath`` token, a config path that isn't present) is
    skipped with a warning rather than crashing the whole app -- mirroring
    ``duho.discover_commands``'s own resilience toward an individual bad command.
    """
    from pathlib import Path as _Path

    path = _Path(source)
    if path.is_dir() and is_runpath_dir(path):
        return [CmdBuilder(path.name.replace("_", "-"), path).command]

    try:
        commands: "list" = list(discover_commands(source))
    except (ImportError, NotImplementedError) as exc:
        _pylogging.getLogger("pytruenas").warning(
            "skipping command source %r: %s", source, exc
        )
        commands = []
    if path.is_dir():
        for child in sorted(path.iterdir()):
            if child.is_dir() and is_runpath_dir(child):
                commands.append(
                    CmdBuilder(child.name.replace("_", "-"), child).command
                )
    return commands


def _wants_logger(hook: "_ty.Callable[..., object]") -> bool:
    """True if a module ``register`` hook accepts a 3rd ``logger`` positional.

    Mirrors duho's own arity tolerance for the ``register`` hook (2-arg
    ``(parser, args)`` or 3-arg ``(parser, args, logger)``), which
    :func:`_with_targets` must reproduce because it calls the module's hook
    itself. Duplicated rather than imported: duho's version is private
    (``duho.runtime._wants_logger_arg``, absent from its ``__all__``). A
    ``*args`` hook can absorb the logger; a signature ``inspect`` refuses falls
    back to the 2-arg call, which never over-supplies an argument.
    """
    import inspect as _inspect

    try:
        params = _inspect.signature(hook).parameters
    except (TypeError, ValueError):  # pragma: no cover - builtins/C callables
        return False
    positional = 0
    for param in params.values():
        if param.kind is _inspect.Parameter.VAR_POSITIONAL:
            return True
        if param.kind in (
            _inspect.Parameter.POSITIONAL_ONLY,
            _inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            positional += 1
    return positional >= 3


def _with_targets(command: object) -> object:
    """Make ``targets`` the trailing positional of a module command, centrally.

    Every pytruenas command takes the same trailing ``TARGET...`` positionals, so
    no command should have to opt in. duho reads a module command's ``register``
    hook off the :class:`~duho.discovery.ModuleCommand` wrapper, which lets us
    wrap it here: run the module's own hook first (adding ITS positionals), then
    add ``targets`` -- argparse binds positionals in registration order, so
    adding last is what keeps them trailing, e.g. ``query <namespace>
    <host>...``.

    Class commands (RunPath) get the same positional from
    :class:`pytruenas.utils.runpath.PyTrueNASRunPathArgs` and are returned
    untouched. The guard against a duplicate ``targets`` action covers a command
    module that still registers its own.

    Wrapping ``ModuleCommand.register`` is a supported seam as of duho 0.4.1,
    which gates and introspects the hook on the same object it calls -- so this
    wrapper runs even for a command that defines no ``register`` of its own
    (``dump-api``, whose only positionals are the targets). Fields a module
    declares via its own ``Args`` class are added by duho *before* the hook
    runs, so they too land ahead of the targets.
    """
    if not isinstance(command, ModuleCommand):
        return command

    inner = getattr(command.module, "register", None)
    wants_logger = callable(inner) and _wants_logger(inner)

    def register(parser, args, logger=None):
        if callable(inner):
            if wants_logger:
                inner(parser, args, logger)
            else:
                inner(parser, args)
        if not any(action.dest == "targets" for action in parser._actions):
            register_targets(parser)

    command.register = register
    return command


def _discover(argv: "_ty.Sequence[str] | None") -> "list":
    """Resolve the command set: built-ins, then env/CLI/config-provided paths.

    Uses :func:`duho.parse_globals` to read the config-file / ``--cmdspath`` /
    ``PYTRUENAS_PATH`` globals *before* the full subcommand parser is built. Later
    sources win on a name clash (a user command shadows a built-in), then the list
    is de-duplicated by subcommand name preserving that precedence.

    Each source is resolved through :func:`_commands_from_source`, which layers
    RunPath-directory discovery on top of ``duho.discover_commands`` (see there).
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
        for command in _commands_from_source(source):
            name = getattr(command, "_parsername_", None) or getattr(command, "__name__", None)
            if name:
                by_name[name] = command  # later source wins
    return [_with_targets(command) for command in by_name.values()]


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

    # Redact any password in the target before it reaches a log record or a
    # ``--logto`` filename; the real ``target`` still builds the client below.
    shown = _redact(target)
    file_handler = None
    if args.logto and args.logto != "-":
        now = _dt.datetime.now()
        file_handler = _pylogging.FileHandler(
            args.logto.format(target=shown, isodate=now.isoformat())
        )
        file_handler.setFormatter(_logging.DefaultFormatter())
        logger.addHandler(file_handler)

    logger.info("Started: %s", shown)
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
                logger.error("Cleanup failed: %s", shown, exc_info=True)
        logger.info("Finished: %s", shown)
        if file_handler is not None:
            logger.removeHandler(file_handler)
            file_handler.close()
    return result


def _run_runpath_on_target(
    instance: "RunPathCmd",
    target: str,
    logger: "_pylogging.Logger",
) -> int:
    """Run one RunPath command (a whole step directory) against one target.

    A ``RunPathCmd`` is a class command whose ``__call__`` runs the ordered step
    sequence once; ``pytruenas`` fans that whole sequence out per target. The
    parsed instance is a namespace, so :func:`copy.copy` gives each concurrent
    fan-out worker its OWN shallow copy with ``.target`` set to this iteration's
    target BEFORE calling it -- a single shared mutable ``.target`` (or per-target
    state a step writes back, e.g. ``cmd.context``) across ``run_targets``'
    thread pool would race. A RunPath directory's own ``__main__.py`` ``init(cmd,
    logger)`` then reads ``cmd.target`` to build a per-target client, threaded by
    duho's ``RunPathCmd.__call__`` into every 2-arg step (``main(cmd, ctx)``) as
    ``ctx`` (see :mod:`pytruenas.utils.runpath`), so each target gets its own
    isolated client/context -- the same per-target isolation guarantee
    :func:`_run_module_on_target` gives module commands.

    ``--logto`` per-target file-handler behavior mirrors
    :func:`_run_module_on_target` exactly (fanout tags the message but does not
    route files).
    """
    per_target = _copy.copy(instance)
    per_target.target = target

    # Redact any password in the target before it reaches a log record or a
    # ``--logto`` filename; ``per_target.target`` keeps the real value.
    shown = _redact(target)
    file_handler = None
    if instance.logto and instance.logto != "-":
        now = _dt.datetime.now()
        file_handler = _pylogging.FileHandler(
            instance.logto.format(target=shown, isodate=now.isoformat())
        )
        file_handler.setFormatter(_logging.DefaultFormatter())
        logger.addHandler(file_handler)

    logger.info("Started: %s", shown)
    try:
        rc = per_target()
        return 0 if rc is None else int(rc)
    finally:
        logger.info("Finished: %s", shown)
        if file_handler is not None:
            logger.removeHandler(file_handler)
            file_handler.close()


def _dispatch(command: object, instance: "PyTrueNAS") -> int:
    """duho ``app`` dispatch seam: fan the selected command over the targets.

    For a module command (every built-in) OR a RunPath command (a directory of
    numbered step files, adopted from :mod:`duho.runpath`), run it once per target
    positional via :func:`duho.fanout.run_targets` (thread pool sized by
    ``--parallel``, per-target ``[target]`` log prefixing, worst exit code wins).
    This restores the private predecessor's behavior, where a RunPath directory
    ran once per target with a per-target client -- current duho-based dispatch
    would otherwise fall a class command (which is exactly what a ``RunPathCmd``
    is) through to duho's plain SINGLE dispatch, un-fanned, never touching a
    target. Any OTHER class command still falls back to duho's own single
    dispatch.
    """
    logger = instance._logger_
    for name, level in DEFAULT_LOGLEVELS.items():
        _pylogging.getLogger(name).setLevel(level)

    # A RunPath command reaches dispatch as (class, parsed-instance): ``app``
    # calls ``dispatch(type(instance), instance)`` for a class command. Check the
    # instance (and the class, defensively) BEFORE the ModuleCommand branch --
    # otherwise a RunPathCmd falls through to duho's un-fanned single dispatch.
    if isinstance(instance, RunPathCmd) or (
        isinstance(command, type) and issubclass(command, RunPathCmd)
    ):
        runpath = _ty.cast("RunPathCmd", instance)
        targets = runpath._expanded_targets_()
        logger.info(
            "Running '%s' on %d target(s)", runpath._parsername_, len(targets)
        )
        return run_targets(
            lambda target: _run_runpath_on_target(runpath, target, logger),
            targets,
            max_workers=max(1, instance.parallel),
            logger=logger,
        )

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
