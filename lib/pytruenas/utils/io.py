import pathlib as _path
import re as _re

STAT_FIELDS: tuple[str] = tuple(
    _re.findall(r"(st_[^=]*)=", str(_path.Path(__file__).stat()))
)


def isbytelike(obj):
    return isinstance(obj, (memoryview, bytes, bytearray))


def bytes_(txt: "bytes|str") -> bytes:
    if isinstance(txt, str):
        return txt.encode()
    return txt
