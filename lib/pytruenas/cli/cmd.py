import argparse as _argparse
import fnmatch as _fnmatch
import importlib.util as _importutils
import os as _os
import sys as _sys
import typing as _ty
from importlib import import_module as _import
from pathlib import Path as _Path
from types import ModuleType as _Module

from ..client import TrueNASClient as _Client
from ..utils import logging as _logging
from ..utils import text as _text
from ..utils.import_ import import_from_path
from ..utils.qualname import PythonName as _PyName
from . import utils as _cli


class PyTrueNASArgs(_cli.LoggingArgs):
    "Utility tool to manage and configure TrueNAS systems"

    config: _cli.Arg[
        dict,
        _cli.NS(
            type=_Path,
            default=_os.environ.get("PYTRUENAS_CFG") or "./pytruenas.yaml",
        ),
    ]
    "Config file to use"
    ["--config", "-c"]

    cmdspath: _cli.Arg[list[str], _cli.Extend(":")] = (
        _os.environ.get("PYTRUENAS_PATH", None) or "pytruenas.cmd"
    ).split(":")

    target: _cli.Arg[str, _argparse.SUPPRESS]

    targets: _cli.Arg[list[str], _cli.Extend(_text.expand, nargs="*")]
    ("targets",)

    sslverify: bool

    def __init__(self, *, config: _Path, targets: list[str], **kwargs) -> None:
        import yaml

        if isinstance(config, _Path):
            if config.exists():
                _config: dict = yaml.safe_load(config.read_text())
            else:
                _config = {}
        else:
            _config = config or {}
        targets = targets or ["localhost"]
        super().__init__(config=_config, targets=targets, **kwargs)


_A = _ty.TypeVar("_A", bound=PyTrueNASArgs)
_C = _ty.TypeVar("_C", bound=_Client)


class CmdProtocol(_ty.Protocol, _ty.Generic[_A, _C]):  # type:ignore
    def run(self, client: _C, args: _A, logger: _logging.Logger): ...


class _CmdModule(_Module, CmdProtocol[_A, _C]):
    def init(self, args: _A, loggen: _logging.Logger) -> _C: ...
    def success(self, client: _C, args: _A, logger: _logging.Logger): ...
    def finally_(self, client: _C, args: _A, logger: _logging.Logger): ...

    def register(
        self,
        parser: _argparse.ArgumentParser,
        args: PyTrueNASArgs,
        logger: _logging.Logger,
    ):
        pass


class RunPathArgs(PyTrueNASArgs):
    rcopts: _cli.Arg[list[str], _cli.Extend(",")]
    "Options for runpath steps, example: !*,step1 -> Disable all except step1"


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

    @classmethod
    def from_matchstring(cls, text: str):
        text = text.strip()
        disable = text.startswith("!")
        strict = not text.endswith("?")
        if not strict:
            text = text[:-1] + ":!strict"
        if disable:
            text = text[1:] + ":!enable"
        text, *opts = text.split(":")
        opts = cls.parse(opts)
        return text, opts


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

            name, opts = RcOptions.from_matchstring(name)

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

    def run(self, client: _C, args: _RA, logger: _logging.Logger):
        rcopts: list[tuple[str, RcOptions]] = []
        for pattern in args.rcopts:
            pattern, opts = RcOptions.from_matchstring(pattern)
            logger.debug(f"Fi1ter pattern:{pattern} opts :{opts}")
            rcopts.append((pattern, opts))

        done = []

        def run(step: RunPathStep, force: bool):
            qualname = _PyName(step.__name__)
            rcopt = RcOptions(enabled=True, strict=True)
            rcopt.update(step.RCOPTS)
            for pattern, opts in rcopts:
                if _fnmatch.fnmatchcase(
                    qualname if "." in pattern else qualname.name, pattern
                ):
                    rcopt.update(opts)

            if rcopt.enabled or force:
                for dep in step.REQUIRED:
                    if dep not in done:
                        run(
                            next(
                                filter(
                                    lambda s: s.__name__ == self.qualname / dep,
                                    self.steps,
                                )
                            ),
                            True,
                        )

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

        for step in self.steps:
            if step.__name__ in done:
                continue
            run(step, False)

    def register(
        self,
        parser: _argparse.ArgumentParser,
        args: PyTrueNASArgs,
        logger: _logging.Logger,
    ):
        RunPathArgs.initparser(parser)


class Cmd:
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

    def run(self, args: PyTrueNASArgs):
        client = None
        logger = self.logger
        try:
            client = self.module.init(args, logger)
            self.module.run(client, args, logger)
            self.module.success(client, args, logger)
        finally:
            self.module.finally_(client, args, logger)

    def register(self, parser: _argparse.ArgumentParser, args: PyTrueNASArgs):
        logger = self.logger
        if hasattr(self.module, "register"):
            self.module.register(parser, args, logger)
        order = {k.dest: i for i, k in enumerate(parser._actions)}
        order["targets"] = len(order)
        parser._actions.sort(key=lambda x: order[x.dest])
        parser.set_defaults(_cmd=self)

    @property
    def description(self):
        return (self.module.__doc__ or "").strip()

    @property
    def help(self):
        return (self.description.splitlines() or [""])[0]

    @property
    def logger(self):
        return _logging.getLogger(self.qualname)
