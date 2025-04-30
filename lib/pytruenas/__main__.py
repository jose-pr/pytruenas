import argparse
from pathlib import Path
import typing
from pytruenas.utils import cli
from pytruenas.utils.text import expand
from pytruenas.utils.cmd import Cmd, PyTrueNASArgs
from pytruenas.utils.qualname import PythonName
from pytruenas.utils import logging
import sys
import os
import importlib.util as _import
import yaml
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

for pkg in ["requests", "urllib3", "websocket", "httpx"]:
    logging.getLogger(pkg).setLevel(logging.WARNING)

logging.init_stderr_logging()


MODULE = PythonName(Path(__file__).parent.name)
CMDS_MODULE = MODULE / "cmd"

logger = logging.getLogger(MODULE)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "PyTrueNAS",
        "Utility tool to manage and configure TrueNAS systems",
        add_help=False,
        conflict_handler="resolve",
    )
    cli.add_logging_args(parser)
    parser.add_argument("--configpath", "-c", help="Config file to use", type=Path)
    parser.add_argument(
        "--cmdspath",
        help="paths to search for commands",
        default=[],
        type=lambda x: x.split(":"),
        action="extend",
    )

    cmdaction = parser.add_subparsers(
        title="command", dest="command_name", required=False
    )

    args = typing.cast(PyTrueNASArgs, cli.prerun_parse(parser))

    cli.add_help_argument(parser)

    for name, level in cli.LoggingArgs.set_loglevels(args).items():
        logger.debug(
            f"Logging level for '{name}' set at: {', '.join(logging.VERBOSE_LEVELS[level])}"
        )

    configpath = Path(
        args.configpath or os.environ.get("PYTRUENAS_CFG") or "./pytruenas.yaml"
    )
    if configpath.exists():
        config: dict = yaml.safe_load(configpath.read_text())
    else:
        config = {}
    args.config = config

    cmds_paths: list[str] = [
        *(os.environ.get("PYTRUENAS_PATH", None) or "pytruenas.cmd").split(":"),
        *args.cmdspath,
    ] + (config.get("cmdpaths") or [])

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
            name = path.stem

            if name.startswith("__"):
                continue
            cmd = Cmd(CMDS_MODULE / name, path)
            cmd_parser = cmdaction.add_parser(
                name.replace("_", "-"), help=cmd.help, description=cmd.description
            )
            cmd.register(cmd_parser, args)
    if args.command_name:
        cmdname = args.command_name
        try:
            if "/" in cmdname:
                path = Path(cmdname)
                name = path.stem
                cmd = Cmd(CMDS_MODULE / name, path)
                cmd_parser = cmdaction.add_parser(
                    cmdname, help=cmd.help, description=cmd.description
                )
                cmd.register(cmd_parser, args)

            elif "." in cmdname:
                qualname = PythonName(cmdname)
                cmd = Cmd(qualname, None)
                cmd_parser = cmdaction.add_parser(
                    cmdname, help=cmd.help, description=cmd.description
                )
                cmd.register(cmd_parser, args)
        except ImportError as e:
            logger.error(f"Could not load {cmdname}")

    args = typing.cast(PyTrueNASArgs, parser.parse_args())
    args.config = config
    targets: list[str] = []
    for template in args.targets:
        targets.extend(expand(template))

    logger.info(f"Running {args.command_name} on {targets}")

    for target in targets:
        args.cmd.run(target, args)
