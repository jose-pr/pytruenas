import argparse as _argparse
from pathlib import Path as _Path
from .import_ import import_from_path
from .qualname import PythonName as _PyName
from ..client import TrueNASClient as _Client
from logging import Logger as _Logger, getLogger as _getlogger
from types import ModuleType as _Module
from importlib import import_module as _import
import typing as _ty
import sys as _sys


class PyTrueNASArgs(_argparse.Namespace):
    config: _Path
    cmd: "Cmd"
    targets: list[str]
    command_name: str
    sslverify: bool
    verbose: int


class CmdProtocol(_ty.Protocol):
    def run(self, client: _Client, args: PyTrueNASArgs, logger: _Logger): ...


class _CmdModule(_Module, CmdProtocol):
    def register(self, parser: _argparse.ArgumentParser):
        pass


class RunPathStep(_Module, CmdProtocol):
    PRIORITY: int


class RunPathCmd(_CmdModule):

    def __init__(self, path: _Path, qualname: _PyName) -> None:
        super().__init__(str(qualname), doc="")
        self.qualname = qualname
        main = path / "__main__.py"
        if main.exists():
            exec(main.read_bytes(), self.__dict__)

        self.steps: list[RunPathStep] = []

        maxpriority = 0

        for path in sorted(path.iterdir()):
            name = path.name
            if name.startswith("__"):
                continue
            if path.suffix != ".py" and path.is_file():
                continue
            name = path.stem
            if "." in name:
                continue
            parts = name.split("-")
            if len(parts) == 1:
                priority = maxpriority + 1
                name = parts[0]
            else:
                priority = int(parts[0])
                name = parts[1]
            maxpriority = max(priority, maxpriority)
            step = _ty.cast(RunPathStep, import_from_path(self.qualname / name, path))
            step.PRIORITY = priority
            self.steps.append(step)
        self.steps = sorted(self.steps, key=lambda s: s.PRIORITY)

    def run(self, client: _Client, args: PyTrueNASArgs, logger: _Logger):
        for step in self.steps:
            step.run(client, args, _getlogger(step.__name__))

    def register(self, parser: _argparse.ArgumentParser):
        parser.add_argument('-s', '--steps', help='Filter Steps', default='*')


class Cmd:
    def __init__(
        self, qualname: _PyName, module: _Path | None | _CmdModule = None
    ) -> None:
        self.qualname = qualname
        if isinstance(module, _Path):
            if module.is_dir():
                self.module = RunPathCmd(module, qualname)

            else:
                self.module = _ty.cast(
                    _CmdModule, import_from_path(self.qualname, module)
                )
        elif not module:
            self.module = _ty.cast(_CmdModule, _import(str(qualname)))
        else:
            self.module = module

        if self.module.__name__ != str(qualname):
            _sys.modules[str(qualname)] = self.module

    def run(self, client: _Client, args: PyTrueNASArgs):
        self.module.run(client, args, self.logger)

    def register(
        self, parser: _argparse.ArgumentParser, shared: _ty.Sequence[_argparse.Action]
    ):
        if hasattr(self.module, 'register'):
            self.module.register(parser)
        for action in shared:
            parser._add_action(action)
        parser.set_defaults(cmd=self)

    @property
    def description(self):
        return (self.module.__doc__ or "").strip()

    @property
    def help(self):
        return (self.description.splitlines() or [""])[0]

    @property
    def logger(self):
        return _getlogger(str(self.qualname))
