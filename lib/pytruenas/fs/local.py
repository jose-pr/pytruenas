import os as _os
import typing as _ty
from pathlib import Path as _LocalPath

if _ty.TYPE_CHECKING:
    from . import Path

import sys as _sys

FORCE_LOCAL = False


def _make_proxy(func: _ty.Callable):
    def _proxy(path: "Path", *args, _force_local=False, **kwargs):
        if not FORCE_LOCAL and not path._client._api.is_local and not _force_local:
            raise NotImplementedError()
        return func(_LocalPath(path._path), *args, **kwargs)

    return _proxy


for _attr in dir(_LocalPath):
    _method = getattr(_LocalPath, _attr)
    if callable(_method) and not _attr.startswith("_"):
        setattr(_sys.modules[__name__], _attr, _make_proxy(_method))


def chown(path: "Path", uid: int, gid: int, *, follow_symlinks: bool = True):
    return _os.chown(path._path, uid, gid, follow_symlinks=follow_symlinks)


def iterdir(path: "Path"):
    for file in _LocalPath(path).iterdir():
        yield path._with_path(file)
