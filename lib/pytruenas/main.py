import importlib.util as _import
import sys as _sys
import typing as _ty
from pathlib import Path

import urllib3

from .utils import cli, logging
from .utils.cmd import Cmd, PyTrueNASArgs
from .utils.qualname import PythonName
from .utils.text import expand

DEFAULT_LOGLEVELS = {
    "requests": logging.WARNING,
    "urllib3": logging.WARNING,
    "websocket": logging.WARNING,
    "httpx": logging.WARNING,
    "asyncssh": logging.WARNING,
}


MODULE = PythonName(Path(__file__).parent.name)


def main(
    name: PythonName | str | None = None,
    description: str | None = None,
    pretty_name=None,
    default_loglevels=DEFAULT_LOGLEVELS,
    base_commands_qualname: PythonName | None = None,
    argv: _ty.Sequence[str] | None = None,
):
    name = PythonName(name or MODULE)
    logger = logging.getLogger(name)
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
    action = parser._actions.pop(
        parser._actions.index(PyTrueNASArgs._action_targets)  # type:ignore
    )
    cmdaction = parser.add_subparsers(title="command", dest="cmd", required=True)
    parser._actions.append(action)

    # Do a dry run with no error for missing command, pick up a custom command if it exists
    args = _ty.cast(PyTrueNASArgs, cli.prerun_parse(parser, argv))

    #
    # Configuring logs and warnings
    #
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    for name, level in cli.LoggingArgs.set_loglevels(args).items():
        logger.debug(
            f"Logging level for '{name}' set at: {', '.join(logging.VERBOSE_LEVELS[level])}"
        )

    config = args.config
    config["default_loglevels"] = default_loglevels

    #
    #  Load Commands either from a path or from python modules
    #
    cmds_paths: list[str] = args.cmdspath + (config.get("commandspath") or [])
    _searched = []
    for path in cmds_paths:
        paths: list[Path] = []
        if "/" not in path:
            try:
                spec = _import.find_spec(path)
                if not spec:
                    continue
                submodules = spec.submodule_search_locations
                if submodules:
                    for path in submodules:
                        paths.extend(Path(path).iterdir())
            except:
                logger.debug(f"Could not load commands from {path}")
                continue
        else:
            path = Path(path)
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
            module = Path(path)
            qualname = base_commands_qualname / module.stem
        else:
            qualname = PythonName(path)
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
    args.loglevels = cli.LoggingArgs.set_loglevels(args)
    del args._cmd  # type:ignore

    for target in targets:
        args.target = target
        args.cmd.run(args)
