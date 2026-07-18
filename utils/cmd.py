import argparse as _argparse
from pathlib import Path as _Path
from .import_ import import_from_path
from .qualname import PythonName as _PyName
from ..client import TrueNASClient as _Client
from logging import Logger as _Logger, getLogger as _getlogger
from types import ModuleType as _Module
from importlib import import_module as _import
import importlib.util as _importutils
import typing as _ty
import sys as _sys
import fnmatch as _fnmatch

import os as _os
import datetime as _dt

from ..utils import text as _text

from coquilib import logging as _logging, cli as _cli
from coquilib.cli import CliParser as CmdParser
import yaml as _yaml


class PyTrueNAS(_cli.NS, _cli.LoggingArgs):

    config: _cli.Arg[dict, _cli.NS(type=_Path)] = _Path(
        _os.environ.get("PYTRUENAS_CFG") or "./pytruenas.yaml"
    )
    "Config file to use"
    ("--config", "-c")
    cmdspath: _cli.Arg[list[str], _cli.Extend(":")]
    "paths to search for commands"

    def __init__(self, **kwargs):
        config = kwargs.pop("config")
        if isinstance(config, _Path):
            if config.exists():
                config: dict = _yaml.safe_load(config.read_text())
            else:
                config = {}
        super().__init__(**kwargs, config=config)


class PyTrueNASCmd(PyTrueNAS):
    "Utility tool to manage and configure TrueNAS systems"

    sslverify: bool
    ("--sslverify",)
    target: _cli.Arg[str, _argparse.SUPPRESS]
    targets: _cli.Arg[list[str], _cli.Extend(",")] = []
    ("targets",)
    parallel: int = 1
    logto: str = ""

    def __init__(self, **kwargs):
        targets = []
        _targets = kwargs.pop("targets", []) or ["localhost"]
        for target in _targets:
            targets.extend(_text.expand(target))
        super().__init__(**kwargs, targets=targets)

    def _run(self):
        raise NotImplementedError()

    def _call(cmd):
        formatter = _logging.DefaultFormatter()
        now = _dt.datetime.now()
        origcmd = cmd._origcmd_()

        if not cmd.logto:
            cmd.logto = "-"
        target = cmd.target.split('@')[1] if '@' in cmd.target else cmd.target
        if target == 'localhost':
            import socket
            target = f"{socket.gethostname()}|local"
        else:
            target = f"{target}|remote"

        cmd.logger = _logging.Logger(origcmd.logger.name +  f" [{target}]", origcmd.logger.level)
        if cmd.logto == "-":
            handler = _logging.StreamHandler(_sys.stderr)
        else:
            handler = _logging.FileHandler(
                cmd.logto.format(target=cmd.target, isodate=now.isoformat())
            )
        handler.formatter = formatter
        cmd.logger.addHandler(handler)
        cmd._run()
            

    def __call__(self):
        self._origcmd_ = lambda: self
        logger = self.logger
        from multiprocessing.pool import ThreadPool as Pool
        pool= Pool(self.parallel)
        if not self.logto:
            self.logto = "-"
        for target in self.targets:
            cmd = self.__class__(**self.__dict__)
            cmd.target = target
            def call(cmd:PyTrueNASCmd):
                logger.info(f"Started: {cmd.target}")
                try:
                    cmd._call()
                except Exception as e:
                    logger.error(f"Failed: {target}",exc_info=True)
                logger.info(f"Finished: {cmd.target}")
            pool.apply_async(call, (cmd,))
        pool.close()
        pool.join()
        return


_A = _ty.TypeVar("_A", bound=PyTrueNASCmd)
_C = _ty.TypeVar("_C", bound=_Client)


class CmdProtocol(_ty.Protocol, _ty.Generic[_A, _C]):  # type:ignore
    def run(self, client: _C, args: _A, logger: _Logger): ...


class _CmdModule(_Module, CmdProtocol[_A, _C]):
    def init(self, args: _A, loggen: _Logger) -> _C: ...
    def success(self, client: _C, args: _A, logger: _Logger): ...
    def finally_(self, client: _C, args: _A, logger: _Logger): ...

    def register(self, parser: _cli.CliParser, args: PyTrueNAS, logger: _Logger):
        pass


class RunPathArgs(PyTrueNASCmd):
    rcopts: _cli.Arg[list[str], _cli.Extend(",")]
    "Options for runpath steps, example: !*,step1 -> Disable all except step1"
    ("-O", "--rcopts")


_RA = _ty.TypeVar("_RA", bound=RunPathArgs)


class RcOptions(_argparse.Namespace):
    enabled: bool | None
    strict: bool | None

    @classmethod
    def parse(cls, opts: _ty.Sequence[str]):
        parsed: dict[str, None | bool] = {"enabled": None, "strict": None}
        for opt in opts:
            opt = opt.strip()
            parsed[opt.removeprefix("!")] = not opt.startswith("!")
        return cls(**parsed)

    def update(self, rcopt: "RcOptions"):
        for attr in ["enabled", "strict"]:
            val = getattr(rcopt, attr, None)
            if val is not None:
                setattr(self, attr, val)


class RunPathStep(_Module, CmdProtocol[_RA, _C]):
    RCOPTS: "RcOptions"
    PRIORITY: int
    REQUIRED: list[_PyName]


class RunPathCmd(_CmdModule[_RA, _C]):

    def __init__(self, path: _Path, qualname: _PyName) -> None:
        self.qualname = qualname
        main = path / "__main__.py"
        self.__file__ = str(main.resolve())
        self.__name__ = qualname
        super().__init__(qualname, doc="")

        if main.exists():
            exec(main.read_bytes(), self.__dict__)

        self.steps: list[RunPathStep] = []

        nextpri = 1_000

        for path in sorted(path.iterdir()):
            name = path.name
            if name.startswith("__"):
                continue
            if path.suffix != ".py" and path.is_file():
                continue
            name = path.stem
            if "." in name:
                continue

            disable = name.startswith("!")
            if disable:
                name = name[1:] + ":!enable"

            name, *opts = name.split(":")
            opts = RcOptions.parse(opts)
            parts = name.split("-", maxsplit=1)

            if len(parts) == 1:
                priority = nextpri
                name = parts[0]
            else:
                priority = int(parts[0])
                name = parts[1]

            nextpri = max(priority, nextpri + 1)
            step = _ty.cast(RunPathStep, import_from_path(self.qualname / name, path))
            step.RCOPTS = opts
            step.PRIORITY = priority
            step.REQUIRED = getattr(step, "REQUIRED", None) or []
            self.steps.append(step)
        self.steps = sorted(self.steps, key=lambda s: s.PRIORITY)

    def run(self, client: _C, args: _RA, logger: _Logger):
        rcopts: list[tuple[str, RcOptions]] = []
        for pattern in args.rcopts:
            disable = pattern.startswith("!")
            if disable:
                pattern = pattern[1:] + ":!enabled"
            elif ":" not in pattern:
                pattern += ":enabled"
            pattern, *opts = pattern.split(":")
            opts = RcOptions.parse(opts)
            logger.debug(f"Fi1ter pattern:{pattern} opts :{opts}")
            rcopts.append((pattern, opts))

        done = []
        for step in self.steps:
            if step.__name__ in done:
                continue
            qualname = _PyName(step.__name__)
            rcopt = RcOptions(enabled=True, strict=True)
            rcopt.update(step.RCOPTS)
            for pattern, opts in rcopts:
                if _fnmatch.fnmatchcase(
                    qualname if "." in pattern else qualname.name, pattern
                ):
                    rcopt.update(opts)

            if rcopt.enabled:
                logger.info(f"Running step {step.__name__}")
                try:
                    step.run(client, args, logger)
                except Exception as e:
                    logger.error(
                        f"Encountered an error while running: {step.__name__}\n{e}"
                    )
                    if rcopt.strict:
                        raise e from None
                done.append(step.__name__)

    def register(self, parser: CmdParser, args: PyTrueNAS, logger: _Logger):
        parser.add_args(RunPathArgs)


class Cmd(_cli.args.Cmd):
    def __init__(
        self, qualname: _PyName, module: _Path | None | _CmdModule = None
    ) -> None:
        self.qualname = qualname
        if isinstance(module, _Path):
            while qualname in _sys.modules:
                qualname = qualname.parent / (qualname.name + "_")
            if module.is_dir() and not (module / "__init__.py").exists():
                self.module = RunPathCmd(module, qualname)
            else:
                self.module = _ty.cast(
                    _CmdModule, import_from_path(self.qualname, module)
                )
        elif not module:
            spec = _importutils.find_spec(qualname)
            if not spec:
                raise ImportError(name=qualname)
            if not spec.origin and spec.submodule_search_locations:
                self.module = RunPathCmd(
                    _Path(spec.submodule_search_locations[0]), qualname
                )
            else:
                self.module = _ty.cast(_CmdModule, _import(qualname))
        else:
            self.module = module

        if self.module.__name__ != qualname:
            _sys.modules[qualname] = self.module

        if not getattr(self.module, "init", None):
            self.module.init = lambda a, l: _Client(  # type:ignore
                a.target, sslverify=a.sslverify
            )

        if not getattr(self.module, "success", None):
            self.module.success = lambda c, a, l: ...  # type:ignore

        if not getattr(self.module, "finally_", None):
            self.module.finally_ = lambda c, a, l: ...  # type:ignore

    def run(self, args: PyTrueNASCmd):
        client = None
        logger = args.logger
        try:
            client = self.module.init(args, logger)
            self.module.run(client, args, logger)
            self.module.success(client, args, logger)
        finally:
            self.module.finally_(client, args, logger)

    def register(self, parser: _cli.CliParser, args: PyTrueNAS):
        logger = self.logger
        cmd = self
        if hasattr(self.module, "register"):
            self.module.register(parser, args, logger)

        class CmdAction(PyTrueNASCmd):
            logger = cmd.logger

            def _run(self, *args, **kwds):
                cmd.run(self)

        parser.user_parent_namepace = True
        parser.add_args(CmdAction, True)
        setattr(parser, "__issubparser", True)

    @property
    def description(self):
        return (self.module.__doc__ or "").strip()

    @property
    def help(self):
        return (self.description.splitlines() or [""])[0]

    @property
    def logger(self):
        return _getlogger(self.qualname)
