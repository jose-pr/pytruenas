import typing as _ty
from pathlib import Path as _Path

from ..utils import logging as _logging
from ..utils.qualname import PythonName as _PyName
from . import utils
from .cmd import Cmd, PyTrueNASArgs
from .utils import *

DEFAULT_LOGLEVELS = {
    "requests": _logging.WARNING,
    "urllib3": _logging.WARNING,
    "websocket": _logging.WARNING,
    "httpx": _logging.WARNING,
    "asyncssh": _logging.WARNING,
}
MODULE = _PyName(_Path(__file__).parent.parent.name)


def main(
    name: _PyName | str | None = None,
    description: str | None = None,
    pretty_name=None,
    default_loglevels=DEFAULT_LOGLEVELS,
    base_commands_qualname: _PyName | None = None,
    argv: _ty.Sequence[str] | None = None,
):
    import importlib.util as _import

    import urllib3

    from ..utils.text import expand

    name = _PyName(name or MODULE)
    logger = _logging.getLogger(name)
    base_commands_qualname = name / "cmd"

    #
    # Build argument parser
    #
    baseparser = PyTrueNASArgs.build_parser(None, add_help=True)
    parser = PyTrueNASArgs.build_parser(
        name=pretty_name or name,
        add_help=False,
        description=description,
        parents=(baseparser,),
    )
    cmdaction = parser.add_subparsers(title="command", dest="cmd", required=True)
    order = {k.dest: i for i, k in enumerate(parser._actions)}
    order["targets"] = len(order)
    parser._actions.sort(key=lambda x: order[x.dest])

    # Do a dry run with no error for missing command, pick up a custom command if it exists
    args = _ty.cast(PyTrueNASArgs, utils.prerun_parse(parser, argv))

    #
    # Configuring logs and warnings
    #
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    for name, level in utils.LoggingArgs.set_loglevels(args).items():
        logger.debug(
            f"Logging level for '{name}' set at: {', '.join(_logging.VERBOSE_LEVELS[level])}"
        )

    config = args.config
    config["default_loglevels"] = default_loglevels

    #
    #  Load Commands either from a path or from python modules
    #
    cmds_paths: list[str] = args.cmdspath + (config.get("commandspath") or [])
    _searched = []
    for path in cmds_paths:
        paths: list[_Path] = []
        if "/" not in path:
            try:
                spec = _import.find_spec(path)
                if not spec:
                    continue
                submodules = spec.submodule_search_locations
                if submodules:
                    for path in submodules:
                        paths.extend(_Path(path).iterdir())
            except:
                logger.debug(f"Could not load commands from {path}")
                continue
        else:
            path = _Path(path)
            if path.exists() and path.is_dir():
                paths.extend(path.iterdir())

        for path in paths:
            if path in _searched:
                continue
            else:
                _searched.append(path)
            name = path.stem

            if name.startswith("__"):
                continue
            cmd = Cmd(base_commands_qualname / name, path)
            cmd_parser = cmdaction.add_parser(
                name.replace("_", "-"),
                help=cmd.help,
                description=cmd.description,
                parents=(baseparser,),
                add_help=False,
                conflict_handler="resolve",
            )
            cmd.register(cmd_parser, args)
    cmdpaths: dict[str, str] = {args.cmd: args.cmd}  # type:ignore
    cmdpaths.update(config.get("commandpaths") or {})
    for cmdname, path in cmdpaths.items():

        if not path or not cmdname or cmdname in cmdaction.choices:
            continue

        if "/" in path:
            module = _Path(path)
            qualname = base_commands_qualname / module.stem
        else:
            qualname = _PyName(path)
            module = None

        try:
            cmd = Cmd(qualname, module)
            cmd_parser = cmdaction.add_parser(
                cmdname,
                help=cmd.help,
                description=cmd.description,
                parents=(baseparser,),
                add_help=False,
            )
            cmd.register(cmd_parser, args)

        except ImportError as e:
            logger.error(f"Could not load {cmdname}")

    args = _ty.cast(PyTrueNASArgs, parser.parse_args(argv))
    args.config = config
    targets: list[str] = []
    for template in args.targets:
        targets.extend(expand(template))

    logger.info(f"Running {args.cmd} on {targets}")
    args.cmd = args._cmd
    args.loglevels = utils.LoggingArgs.set_loglevels(args)
    del args._cmd  # type:ignore

    for target in targets:
        args.target = target
        args.cmd.run(args)
