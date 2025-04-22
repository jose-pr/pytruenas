import typing as _ty
import re as _re
import pathlib as _path
from os import stat_result as _stat

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient as _Client
    from pathlib import PosixPath as _Path

_STAT_FIELDS: tuple[str] = tuple(
    _re.findall(r"(st_[^=]*)=", str(_path.Path(__file__).stat()))
)

def stat(path: "_Path", *, client: "_Client"):
    stat: dict = client.api.filesystem.stat(path.as_posix(), _ioerror=True)
    return _stat([stat.get(field.removeprefix("st_")) for field in _STAT_FIELDS])

def exists(path: "_Path", *, client: "_Client"):
    try:
        stat(path, client=client)
        return True
    except FileNotFoundError:
        return False