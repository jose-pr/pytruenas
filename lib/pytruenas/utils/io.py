import pathlib as _path
import re as _re
import typing as _ty

STAT_FIELDS: tuple[str] = tuple(
    _re.findall(r"(st_[^=]*)=", str(_path.Path(__file__).stat()))
)

FileHandle = None | int | _ty.IO


def isbytelike(obj) -> _ty.TypeGuard[bytes]:
    return isinstance(obj, (memoryview, bytes, bytearray))


def bytes_(txt: "bytes|str") -> bytes:
    if isinstance(txt, str):
        return txt.encode()
    return txt
