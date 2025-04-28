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


class _CmdModule(_Module):
    def run(self, client: _Client, args: PyTrueNASArgs, logger: _Logger): ...


class Cmd:
    def __init__(
        self, qualname: _PyName, module: _Path | None | _CmdModule = None
    ) -> None:
        self.qualname = qualname
        if isinstance(module, _Path):
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

    def register(self, parser: _argparse.ArgumentParser, shared: _ty.Sequence[_argparse.Action]):
        for action in shared:
            parser._add_action(action)
        parser.set_defaults(cmd=self)


    @property
    def description(self):
        return (self.module.__doc__ or "").strip()

    @property
    def help(self):
        return self.description.splitlines()[0]

    @property
    def logger(self):
        return _getlogger(str(self.qualname))
