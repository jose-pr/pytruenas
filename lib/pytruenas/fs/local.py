import typing as _ty
import pathlib as _pathlib

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient as _Client
    from pathlib import PosixPath as _Path

_SAMPLE = _pathlib.Path(__file__)


def __getattr__(name: str):
    getattr(_SAMPLE, name)

    def attr(path: "_Path", *args, client: "_Client", _force_local=False, **kwargs):
        if not client._api.is_local and not _force_local:
            raise NotImplementedError()
        return getattr(_pathlib.Path(path), name)(*args, **kwargs)

    return attr
