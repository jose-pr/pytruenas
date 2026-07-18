from pathlib import Path
import typing as _ty
from .utils.cmd import Cmd, PyTrueNAS
from .utils.qualname import PythonName
from coquilib import logging
import os
import importlib.util as _import
import urllib3

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
    parser = PyTrueNAS._parser(name=pretty_name or name, add_help=False)
    parser.add_argument("#cmd", nargs="?")

    # Do a dry run with no error for missing command, pick up a custom command if it exists
    pytruenas = parser.dryrun(argv)

    #
    # Load base configuration that may affect where to load commands from and other settings
    #
    pytruenas.config["default_loglevels"] = default_loglevels

    #
    # Configuring logs and warnings
    #
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    pytruenas()

    #
    # Build cli parser from options
    #
    parser = PyTrueNAS._parser(
        name=pretty_name or name, description=description, add_help=True
    )
    cmdaction = parser.add_subparsers(title="command", required=True)

    #
    #  Load Commands either from a path or from python modules
    #
    cmds_paths: list[str] = [
        *(os.environ.get("PYTRUENAS_PATH", None) or "pytruenas.cmd").split(":"),
        *pytruenas.cmdspath,
    ] + (pytruenas.config.get("commandspath") or [])
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
            cmd = Cmd(base_commands_qualname / name, path)
            cmd_parser = cmdaction.add_parser(
                name.replace("_", "-"),
                help=cmd.help,
                description=cmd.description,
                add_help=True,
            )
            cmd.register(cmd_parser, pytruenas)
    _cmd = pytruenas.__dict__.get("#cmd")
    cmdpaths: dict[str, str] = {_cmd: _cmd}  # type:ignore
    cmdpaths.update(pytruenas.config.get("commandpaths") or {})
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
                add_help=True,
            )
            cmd.register(cmd_parser, pytruenas)
        except ImportError as e:
            logger.error(f"Could not load {cmdname}")

    cmd = parser.parse_args(argv)
    cmd.config = pytruenas.config
    logger.info(repr(cmd))
    cmd()
