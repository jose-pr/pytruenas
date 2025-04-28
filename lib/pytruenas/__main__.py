import argparse
from pathlib import Path
import typing
from pytruenas import TrueNASClient, _utils
from pytruenas.utils.text import gettext, expand
from pytruenas.utils.cmd import Cmd, PyTrueNASArgs
from pytruenas.utils.qualname import PythonName
import logging
import sys

_utils.add_logging_level("trace", logging.DEBUG - 5)
handler = logging.StreamHandler(sys.stderr)
logging.getLogger().addHandler(handler)

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


MODULE = PythonName(Path(__file__).parent.name)
CMDS_MODULE = MODULE / "cmd"

VERBOSE_LEVELS = {}

for name, level in logging.getLevelNamesMapping().items():
    if not level:
        continue
    aliases: list[str] = VERBOSE_LEVELS.setdefault(level, [])
    if name not in aliases:
        aliases.append(name)

VERBOSE_LEVELS = dict(sorted(VERBOSE_LEVELS.items(), key=lambda l: l[0], reverse=True))

verbosehelp = ", ".join([aliases[0] for aliases in VERBOSE_LEVELS.values()])


logger = logging.getLogger(str(MODULE))

parser = argparse.ArgumentParser(
    "PyTrueNAS", "Utility tool to manage and configure TrueNAS systems", add_help=False
)
parser.add_argument("--config", "-c", help="Config file to use", type=Path)
shared_actions = []
shared_actions.extend(
    [
        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help=verbosehelp,
        ),
        parser.add_argument("--sslverify", action="store_true"),
        parser.add_argument("targets", nargs="*", default=["localhost"]),
    ]
)

if __name__ == "__main__":
    args, argv = typing.cast(tuple[PyTrueNASArgs, list[str]], parser.parse_known_args())
    parser.add_help = True
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help=gettext("show this help message and exit"),
    )

    level = min(
        args.verbose or list(VERBOSE_LEVELS.keys()).index(logging.INFO),
        len(VERBOSE_LEVELS) - 1,
    )
    level = list(VERBOSE_LEVELS.keys())[level]
    logger.setLevel(level)
    logger.debug(f"Logging level set at: {', '.join(VERBOSE_LEVELS[level])}")

    config = args.config or "./pytruenas.yaml"
    cmds_paths = [Path(__file__).parent / "cmd"]
    action = parser.add_subparsers(title="command", dest="command_name", required=True)

    for path in cmds_paths:
        for path in path.iterdir():
            name = path.stem

            if name.startswith("__"):
                continue
            cmd = Cmd(CMDS_MODULE / name, path)
            cmd_parser = action.add_parser(
                name.replace("_", "-"), help=cmd.help, description=cmd.description
            )
            cmd.register(cmd_parser, shared_actions)

    if argv and argv[0]:
        cmdname = argv[0]
        if "/" in cmdname:
            path = Path(cmdname)
            name = path.stem
            cmd = Cmd(CMDS_MODULE / name, path)
            cmd_parser = action.add_parser(
                cmdname, help=cmd.help, description=cmd.description
            )
            cmd.register(cmd_parser, shared_actions)

        elif "." in cmdname:
            qualname = PythonName(cmdname)
            cmd = Cmd(qualname, None)
            cmd_parser = action.add_parser(
                cmdname, help=cmd.help, description=cmd.description
            )
            cmd.register(cmd_parser, shared_actions)

    args = typing.cast(PyTrueNASArgs, parser.parse_args())
    targets = []
    for template in args.targets:
        targets.extend(expand(template))

    logger.info(f"Running {args.command_name} on {targets}")

    for target in targets:
        client = TrueNASClient(target, sslverify=args.sslverify)
        args.cmd.run(client, args)
