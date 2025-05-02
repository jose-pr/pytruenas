import importlib.util as _import
import os as _os
import sys as _sys
from pathlib import Path as _Path

from .qualname import PythonName as _PyName


def import_from_path(qualname: _PyName, path: _Path):
    spec = _import.spec_from_file_location(qualname, path)
    if spec is None:
        raise ImportError(name=qualname, path=_os.fspath(path))
    module = _import.module_from_spec(spec)
    _sys.modules[qualname] = module
    spec.loader.exec_module(module)  # type:ignore
    return module
