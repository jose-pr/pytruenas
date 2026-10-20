"""The ``pytruenas`` command-line application.

Thin driver over :func:`duho.run` (which calls :func:`duho.app`): ``app`` owns
command discovery, parser build, per-command ``register``, config/env layering,
parsing and logging setup; the one piece it hands off is *dispatch*, which
pytruenas overrides to run the selected
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
import sys as _sys
import typing as _ty
from pathlib import Path

import duho.runpath as _runpath
from duho import AUTO, Cli, UsageError, command_name, parse_globals, run
from duho import logging as _logging
from duho.discovery import ModuleCommand, discover_commands
from duho.fanout import current_target, run_targets
from duho.runpath import RunPathCmd
from duho.runtime import accepts_positional
from hostctl.exceptions import MissingExtraError as _MissingExtraError

from ..host import TrueNASConfig
from ..host import TrueNASClient
from .._utils.env import ENV
from ._args import PyTrueNASArgs, with_targets
from .runpath import PyTrueNASRunPathArgs, step_adapter as _step_adapter
from ..target import redact as _redact

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
#
# ``step_adapter`` additionally lets a step be written with the MODULE command
# signature -- ``(client, args, logger)``, the same shape command modules use --
# with no decorator in the step file. Only unambiguous 3-arg steps are adapted
# automatically; see ``runpath.step_adapter``.
_runpath.register(base=PyTrueNASRunPathArgs, step_adapter=_step_adapter)

#: Third-party loggers to quiet by default (chatty at INFO/DEBUG).
DEFAULT_LOGLEVELS = {
    "requests": _pylogging.WARNING,
    "urllib3": _pylogging.WARNING,
    "websocket": _pylogging.WARNING,
    "asyncssh": _pylogging.WARNING,
}

#: Package import path to the built-in command modules.
_BUILTIN_COMMANDS = "pytruenas.cli.commands"


class PyTrueNAS(PyTrueNASArgs, Cli):
    """Utility tool to manage and configure TrueNAS systems."""

    # The command's own name. Without it the name fell back to the class name,
    # so `-v`/`-q` set the level on a `PyTrueNAS` logger nothing logs to,
    # instead of the package's `pytruenas` logger.
    _parsername_ = "pytruenas"

    # Resolve --version from the installed package metadata (single source of
    # truth: pyproject's version), rather than duplicating the literal here.
    _version_ = AUTO
    _distribution_ = "pytruenas"

    #: The shared args root every command inherits, and what :func:`main` uses
    #: when no ``args=`` is passed. Declared here rather than as a `main`
    #: default so a derived tool can set it ONCE by subclassing::
    #:
    #:     class MyApp(PyTrueNAS):
    #:         _ARGS_ = MyArgs
    #:
    #:     main(root=MyApp)          # picks up MyArgs with no second argument
    #:
    #: `main(args=...)` still overrides it for a caller who would rather not
    #: subclass. Kept dunder-ish (`_NAME_`) to match duho's own class-level
    #: knobs (`_version_`, `_distribution_`, `_parsername_`) and to stay clear
    #: of the field namespace -- a plain `ARGS` would be parsed as a CLI field.
    _ARGS_: "type[PyTrueNASArgs]" = PyTrueNASArgs


def _config_sources(value: object, config_path: object) -> "list[str]":
    """The config file's ``cmdspath``, normalized.

    A string is ONE source: `list("mycmds")` made it six single-letter ones.
    A relative entry resolves against the config file's own directory, since
    that is what the author was looking at -- not the process's CWD.
    """
    if value is None:
        return []
    if isinstance(value, str):
        entries = [value]
    elif isinstance(value, (list, tuple)):
        entries = [str(entry) for entry in value]
    else:
        _pylogging.getLogger("pytruenas").warning(
            "ignoring config cmdspath: expected a string or a list, got %s",
            type(value).__name__,
        )
        return []
    base = getattr(config_path, "parent", None)
    resolved = []
    for entry in entries:
        path = Path(entry)
        # Only an entry that EXISTS beside the config file is rewritten. A
        # dotted package name (`mytool.commands`) looks like a file with a
        # suffix, so testing the name's shape resolved it into a path that
        # cannot exist; testing the filesystem cannot make that mistake.
        if base is not None and not path.is_absolute() and (base / path).exists():
            resolved.append(str(base / path))
        else:
            resolved.append(entry)
    return resolved


def _commands_from_source(source: str) -> "list":
    """The commands one source contributes, RunPath directories included.

    ``providers=True`` offers the source directory, and each of its child
    directories, to the RunPath provider: a RunPath directory is one command,
    and its numbered ``NN-name.py`` steps are not read as loose module commands.

    A source that is neither an existing directory nor an importable package (a
    stray ``--cmdspath`` token, a config path that is not present) is skipped
    with a warning rather than stopping the app.
    """
    try:
        return list(discover_commands(source, providers=True))
    except (ImportError, NotImplementedError, TypeError, ValueError) as exc:
        _pylogging.getLogger("pytruenas").warning(
            "skipping command source %r: %s", source, exc
        )
        return []


def _with_targets(command: object) -> object:
    """Make ``targets`` the trailing positional of a module command, centrally.

    Every pytruenas command takes the same trailing ``TARGET...`` positionals, so
    no command should have to opt in. The command's ``Args`` (or
    :class:`PyTrueNASArgs`) is replaced by :func:`~pytruenas.cli.with_targets`
    of it, which declares ``targets`` after the command's own
    fields: argparse binds positionals in that order (``query <namespace>
    <host>...``), and duho publishes a declared field in the command's MCP tool
    schema, where a positional added by a ``register`` hook is missing.

    duho adds declared fields before the module's ``register`` hook runs, so a
    hook that adds positionals is wrapped and :func:`_targets_last` moves the
    hosts behind them; a hook that adds its own ``targets`` keeps it. Class
    commands (RunPath) declare the field on
    :class:`pytruenas.cli.runpath.PyTrueNASRunPathArgs` and are returned
    untouched.
    """
    if not isinstance(command, ModuleCommand):
        return command

    command.args_cls = with_targets(command.args_cls)
    inner = getattr(command.module, "register", None)
    if not callable(inner):
        return command
    # duho calls a `register` hook with 2 or 3 positionals by what it accepts;
    # this wrapper calls the module's hook itself, so it has to do the same.
    wants_logger = accepts_positional(inner, 3)

    def register(parser, args, logger=None):
        if wants_logger:
            inner(parser, args, logger)
        else:
            inner(parser, args)
        _targets_last(parser)

    command.register = register
    return command


def _targets_last(parser: "_ty.Any") -> None:
    """Move the declared ``targets`` positional behind any a hook added.

    duho adds declared fields before the ``register`` hook runs, so a
    positional the hook adds would otherwise come after the hosts. A hook that
    added its own ``targets`` keeps that one.
    """
    found = [action for action in parser._actions if action.dest == "targets"]
    if not found:
        return
    declared = found[0]
    groups = [group._group_actions for group in parser._action_groups]
    for container in [parser._actions, *groups]:
        if declared in container:
            container.remove(declared)
            if len(found) == 1:
                container.append(declared)


def _discover(
    argv: "_ty.Sequence[str] | None", root: "type[PyTrueNAS] | None" = None
) -> "list":
    """Resolve the command set: built-ins, then env/CLI/config-provided paths.

    Uses :func:`duho.parse_globals` to read the config-file / ``--cmdspath`` /
    ``PYTRUENAS_PATH`` globals *before* the full subcommand parser is built. Later
    sources win on a name clash (a user command shadows a built-in), then the list
    is de-duplicated by subcommand name preserving that precedence.

    Each source is resolved through :func:`_commands_from_source`, so RunPath
    directories are found as well as module commands.
    """
    # The resolved root, not the default one: a derived tool's own global
    # options (and its `_ARGS_`) are part of what has to be parsed here, and
    # reading them off `PyTrueNAS` silently ignored them.
    globals_ = parse_globals(root or PyTrueNAS, argv)
    config = globals_._config_dict_()
    sources: "list[str]" = [_BUILTIN_COMMANDS]
    # `ENV.paths` splits on os.pathsep and yields [] for a missing/empty value,
    # so neither the presence check nor the manual split is needed here.
    sources += ENV.paths("PATH")
    sources += list(globals_.cmdspath or [])
    # The config file is the user's own (named, or in their config
    # directory), never one found in the working directory.
    sources += _config_sources(config.get("cmdspath"), globals_._config_path_()[0])

    by_name: "dict[str, object]" = {}
    for source in sources:
        if not source:
            continue
        for command in _commands_from_source(source):
            name = command_name(command)
            if name and _is_runnable(command, name):
                by_name[name] = command  # later source wins
    return [_with_targets(command) for command in by_name.values()]


def _is_runnable(command: object, name: str) -> bool:
    """Whether a discovered module command can actually run a target.

    A module without a ``run`` (one whose entrypoint is ``main``, say) was
    offered in ``--help`` and then failed on every target with an
    ``AttributeError``. Only module commands are checked: a class/RunPath
    command has no ``run`` by design.
    """
    module = getattr(command, "module", None)
    if module is None:
        return True
    if callable(getattr(module, "run", None)):
        return True
    _pylogging.getLogger("pytruenas").warning(
        "skipping command %r: %s defines no run(client, args, logger)",
        name,
        getattr(module, "__name__", module),
    )
    return False


#: Characters Windows refuses in a filename (and ``/`` everywhere).
_ILLEGAL_IN_FILENAME = ':/\\*?"<>|'


def _logto_path(template: str, shown: str) -> str:
    """Render a ``--logto`` template into a filename that can be created.

    Both substitutions carry colons -- ``{target}`` for a non-default port
    (``nas:8443``) and ``{isodate}`` always -- which Windows rejects outright,
    so ``--logto`` failed there for exactly the targets that need it. The
    substituted VALUES are sanitized, not the template: its own directory
    separators are the caller's.
    """

    def _safe(value: str) -> str:
        return "".join("_" if ch in _ILLEGAL_IN_FILENAME else ch for ch in value)

    now = _dt.datetime.now().isoformat(timespec="seconds")
    return template.format(target=_safe(shown), isodate=_safe(now))


class _ThisTarget(_pylogging.Filter):
    """Pass the records logged while ``target`` runs, and no other target's.

    Every target's file handler sits on the same loggers, so under
    ``--parallel`` each would otherwise receive every running target's records.
    A record logged outside any target (a thread the fan-out did not start)
    cannot be attributed and is kept.
    """

    def __init__(self, target: object) -> None:
        super().__init__()
        self._target = target

    def filter(self, record: "_pylogging.LogRecord") -> bool:
        current = current_target.get()
        return current is None or current is self._target


def _attach_logto(
    logto: str, target: str, logger: "_pylogging.Logger"
) -> "_pylogging.Handler | None":
    """Attach a per-target ``--logto`` file handler, or return ``None``.

    On the ``pytruenas`` library logger as well as the command's own: the
    library's records (a transport fallback WARNING, a connection error) are
    exactly what a per-target file is wanted for, and they never pass through
    the command's logger. ``target`` is the string the fan-out runs, which
    selects the records the file receives; its label names the file.
    """
    if not logto or logto == "-":
        return None
    handler = _pylogging.FileHandler(_logto_path(logto, _target_label(target)))
    handler.setFormatter(_logging.DefaultFormatter())
    handler.addFilter(_ThisTarget(target))
    logger.addHandler(handler)
    library = _pylogging.getLogger("pytruenas")
    if library is not logger:
        library.addHandler(handler)
    return handler


def _detach_logto(
    handler: "_pylogging.Handler | None", logger: "_pylogging.Logger"
) -> None:
    """Remove a handler :func:`_attach_logto` added, from both loggers."""
    if handler is None:
        return
    logger.removeHandler(handler)
    _pylogging.getLogger("pytruenas").removeHandler(handler)
    handler.close()


def _target_label(target: str) -> str:
    """The short name to tag this target's log records with.

    The fan-out prefixes every record for a target with it, and ``--logto``
    names the target's file after it, so it is the host's short name and never
    the connection string (which may carry a password).

    Falls back to the password-free rendering of the target if it does not
    parse: an unparseable target must still run (and fail) on its own terms,
    not die here in the display path.
    """
    try:
        return TrueNASConfig.from_target(target).name
    except Exception:
        return _redact(target)


#: Exit status of a target whose command needs an optional extra that is not
#: installed (`hostctl.MissingExtraError`): the status hostctl's own CLI uses.
_MISSING_EXTRA_STATUS = 125


def _run_module_on_target(
    command: "ModuleCommand",
    args: "PyTrueNAS",
    target: str,
    logger: "_pylogging.Logger",
) -> int:
    """Run one module command against one target; return an exit code.

    Builds the client (module ``init`` if present, else the one
    :meth:`PyTrueNASArgs._client_` builds) and runs the module lifecycle ``run``
    + ``success``/``finally_``. Records are already ``[label]``-prefixed by
    ``duho.fanout``. When ``--logto`` is a path template a per-target
    :class:`~logging.FileHandler` is attached for the run (fanout tags the
    message but does not route files).
    """
    module = command.module
    init = getattr(module, "init", None)
    success = getattr(module, "success", None)
    finally_ = getattr(module, "finally_", None)

    # A per-target copy, as the RunPath branch already made: `args` was shared
    # by every concurrent target, so a command that recorded per-target state on
    # it (or read `.target`) saw another target's value. `.target` is set here
    # for the same reason -- an `init` hook had no way to know which target it
    # was building a client for.
    args = _copy.copy(args)

    args.target = target
    file_handler = _attach_logto(args.logto, target, logger)

    # The target is already on every record as the ``[name]`` prefix, so naming
    # it again here would just read "[nas1] Started: nas1".
    logger.info("Started")
    client = None
    ours = False
    result = 0
    try:
        if callable(init):
            client = init(args, logger)
        if client is None:
            client = args._client_(target)
            # Only a client this function built is closed below: one an `init`
            # hook returned belongs to the hook, which may be caching it.
            ours = True
        rc = module.run(client, args, logger)
        result = 0 if rc is None else int(rc)
        # Only on success, as duho's own lifecycle does: a command that
        # returned a non-zero exit code still ran its success hook, so a
        # "deploy succeeded" notification fired for a failed deploy.
        if result == 0 and callable(success):
            success(client, args, logger)
    except _MissingExtraError as exc:
        # A usage condition with a remedy in its message, not a crash: one
        # line, and hostctl's status for it.
        logger.error("%s", exc)
        result = _MISSING_EXTRA_STATUS
    finally:
        if callable(finally_):
            try:
                finally_(client, args, logger)
            except Exception:
                logger.error("Cleanup failed", exc_info=True)
        if ours and client is not None:
            # Without this every target leaked its websocket and reader thread
            # for the life of the process -- which under `--parallel` is every
            # target at once.
            try:
                client.close()
            except Exception:
                logger.debug("closing the client failed", exc_info=True)
        logger.info("Finished")
        _detach_logto(file_handler, logger)
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
    ``ctx`` (see :mod:`pytruenas.cli.runpath`), so each target gets its own
    isolated client/context -- the same per-target isolation guarantee
    :func:`_run_module_on_target` gives module commands.

    ``--logto`` per-target file-handler behavior mirrors
    :func:`_run_module_on_target` exactly (fanout tags the message but does not
    route files).
    """
    per_target = _copy.copy(instance)
    per_target.target = target
    file_handler = _attach_logto(instance.logto, target, logger)

    # Already on every record as the ``[name]`` prefix -- see
    # _run_module_on_target.
    logger.info("Started")
    try:
        rc = per_target()
        return 0 if rc is None else int(rc)
    finally:
        logger.info("Finished")
        _detach_logto(file_handler, logger)


def _dispatch(command: object, instance: "PyTrueNAS") -> int:
    """duho ``app`` dispatch seam: fan the selected command over the targets.

    For a module command (every built-in) OR a RunPath command (a directory of
    numbered step files, adopted from :mod:`duho.runpath`), run it once per target
    positional via :func:`duho.fanout.run_targets` (thread pool sized by
    ``--parallel``, per-target ``[target]`` log prefixing, worst exit code wins).
    duho's own dispatch would run a class command (which a ``RunPathCmd`` is)
    once, un-fanned, never touching a target. Any OTHER class command still
    falls back to duho's own single dispatch.
    """
    logger = instance._logger_
    # duho has already applied --loglevel; a logger named there keeps its level.
    named = getattr(instance, "loglevels", None) or {}
    for name, level in DEFAULT_LOGLEVELS.items():
        if name not in named:
            _pylogging.getLogger(name).setLevel(level)
    _warn_stray_passthrough(command, instance, logger)

    # A RunPath command reaches dispatch as (class, parsed-instance): ``app``
    # calls ``dispatch(type(instance), instance)`` for a class command. Check the
    # instance (and the class, defensively) BEFORE the ModuleCommand branch --
    # otherwise a RunPathCmd falls through to duho's un-fanned single dispatch.
    if isinstance(instance, RunPathCmd) or (
        isinstance(command, type) and issubclass(command, RunPathCmd)
    ):
        runpath = _ty.cast("RunPathCmd", instance)
        targets = runpath._expanded_targets_()
        logger.info("Running '%s' on %d target(s)", runpath._parsername_, len(targets))
        return run_targets(
            lambda target: _run_runpath_on_target(runpath, target, logger),
            targets,
            max_workers=max(1, instance.parallel),
            logger=logger,
            label=_target_label,
        )

    if not isinstance(command, ModuleCommand):
        from duho import run_command

        return run_command(_ty.cast(_ty.Any, command), instance)

    # Once, before any client is built: a `duho.UsageError` from here is one
    # message and exit status 2, not the same failure once per target.
    validate = getattr(command.module, "validate_args", None)
    if callable(validate):
        validate(instance)

    targets = instance._expanded_targets_()
    logger.info("Running '%s' on %d target(s)", command._parsername_, len(targets))
    return run_targets(
        lambda target: _run_module_on_target(command, instance, target, logger),
        targets,
        max_workers=max(1, instance.parallel),
        logger=logger,
        label=_target_label,
    )


def _reads_passthrough(command: object) -> bool:
    """Whether ``command`` reads the arguments after ``--`` (``_passthrough_``).

    A module command says so with a module-level ``_allow_passthrough_ = True``,
    the name duho reads on a class command. A RunPath command's steps can read
    the tail off ``cmd``, so it is taken to read it.
    """
    module = getattr(command, "module", None)
    if module is None:
        return True
    return bool(getattr(module, "_allow_passthrough_", False))


def _warn_stray_passthrough(
    command: object, instance: "PyTrueNAS", logger: "_pylogging.Logger"
) -> None:
    """Warn when a ``--`` tail cannot be used, rather than dropping it silently.

    duho captures the tail on the parsed instance as ``_passthrough_``. Two
    ways to lose it: naming a command that reads none, and putting the target
    after ``--`` (`deploy -- call x nas1`), where the target becomes part of
    the tail and the run falls back to ``localhost``.
    """
    extra = list(getattr(instance, "_passthrough_", ()) or ())
    if not extra:
        return
    if not _reads_passthrough(command):
        name = command_name(command) or str(command)
        logger.warning(
            "ignoring the %d argument(s) after '--': %s reads none", len(extra), name
        )
        return
    if not getattr(instance, "targets", None):
        logger.warning(
            "no target before '--': running on localhost "
            "(targets must precede the separator)"
        )


def _app_root(
    root: "type[PyTrueNAS]", args: "type[PyTrueNASArgs]"
) -> "type[PyTrueNAS]":
    """Return the runnable app root for ``args``.

    ``root`` is used as-is when it already carries ``args`` -- the ordinary
    case, either the default pair or a subclass that set ``_ARGS_``. Rebuilding
    an equivalent class would change the app's identity and ``__doc__`` (which
    becomes the CLI description) for no gain.

    A caller passing ``args=`` WITHOUT a matching root gets a class built here,
    combining the two. ``args`` goes first so its fields and methods win the
    MRO, matching how ``duho.runpath`` orders its own ``base``.
    """
    if issubclass(root, args):
        return root
    return _ty.cast(
        "type[PyTrueNAS]",
        type(
            args.__name__ + "Cli",
            (args, root),
            {
                # `__doc__` becomes the CLI description; prefer the args
                # class's own when it has one, else keep the root's.
                "__doc__": args.__doc__ or root.__doc__,
                "_ARGS_": args,
            },
        ),
    )


def _runpath_base(args: "type[PyTrueNASArgs]") -> type:
    """The ``duho.runpath`` base for ``args``.

    A RunPath command needs :class:`~pytruenas.cli.runpath.
    PyTrueNASRunPathArgs`'s trailing-``targets`` ``_initparser_`` override on
    top of the shared root -- without it a derived tool's RunPath commands
    silently lose their ``TARGET`` positional (it is ``SUPPRESS``-ed on a plain
    class command). So an args class that does not already derive from it is
    COMBINED with it rather than used directly.
    """
    if issubclass(args, PyTrueNASRunPathArgs):
        return args
    if issubclass(PyTrueNASRunPathArgs, args):
        # The shared root itself (or anything PyTrueNASRunPathArgs already
        # derives from): it needs nothing added, and combining the two in this
        # order is an impossible MRO.
        return PyTrueNASRunPathArgs
    return type(args.__name__ + "RunPath", (args, PyTrueNASRunPathArgs), {})


def main(
    argv: "_ty.Sequence[str] | None" = None,
    *,
    name: "str | None" = None,
    args: "type[PyTrueNASArgs] | None" = None,
    root: "type[PyTrueNAS] | None" = None,
) -> int:
    """Build the app, parse ``argv``, and run the selected command per target.

    ``root`` (default :class:`PyTrueNAS`) is the app class; ``args`` is the
    shared args root every command inherits, defaulting to that root's
    :attr:`PyTrueNAS._ARGS_`. A derived tool adds global options either way::

        class MyArgs(PyTrueNASArgs):
            region: str = "us-east"
            "Which region to operate on"
            ("--region",)  # type: ignore

        class MyApp(PyTrueNAS):
            _ARGS_ = MyArgs

        sys.exit(main(name="mytool", root=MyApp))   # or: main(args=MyArgs)

    Whichever way it arrives, the args class is applied in BOTH places a shared
    root has to reach -- which is the whole reason this is a parameter rather
    than something a caller wires up itself:

    * the app root, so module commands and the global parser see the added
      fields; and
    * ``duho.runpath``'s ``base``, so RunPath commands inherit them too --
      re-registered here rather than only at import, because duho applies a
      base when each command CLASS IS BUILT, and discovery happens below.
      Registering at import time (as this module does for the default) is too
      early to honour a per-call ``args``.
    """
    name = name or "pytruenas"
    root = root or PyTrueNAS
    args = args or root._ARGS_
    if not (isinstance(args, type) and issubclass(args, PyTrueNASArgs)):
        raise TypeError(
            "args must be a PyTrueNASArgs subclass; the fan-out reads "
            "_expanded_targets_/_config_dict_ off the parsed instance"
        )

    root = _app_root(root, args)
    # Always register, not only for a custom base: the registration is global
    # and persists, so a previous main() call with a derived base leaked into a
    # later default one (and into anything else in the process).
    _runpath.register(base=_runpath_base(args), step_adapter=_step_adapter)

    try:
        return run(
            root,
            argv,
            exit="parse",
            commands=_discover(argv, root),
            name=name,
            description=root.__doc__,
            dispatch=_dispatch,
        )
    except _MissingExtraError as exc:
        # Raised before any target runs (reading the config file): one line
        # and the status a target's missing extra gets.
        print(f"{name}: {exc}", file=_sys.stderr)
        return _MISSING_EXTRA_STATUS
    except UsageError as exc:
        # Raised by discovery, before duho's own error reporting is in place
        # (a --config file that does not exist): reported the way duho reports
        # one raised by a command.
        print(f"{name}: error: {exc}", file=_sys.stderr)
        return exc.code
