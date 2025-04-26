from typing import (
    TypedDict as _Dict,
    TypeVar as _TypeVar,
    NamedTuple as _NT,
    Sequence as _Sequence,
    Mapping as _Map,
    Generic as _Generic,
)
import typing as _ty

T = _ty.TypeVar("T")

import re as _re
import pathlib as _path

STAT_FIELDS: tuple[str] = tuple(
    _re.findall(r"(st_[^=]*)=", str(_path.Path(__file__).stat()))
)

def classname(name: "str") -> str:
    std = _re.sub(r"[-\s_]+", "_", name)
    std = std.replace("+", "Plus").replace("!", "Not").replace("*", "All")
    std = _re.sub(r"\W|^(?=\d)", "_", std)
    if std == "":
        std = "_"
    std = std[0].upper() + _re.sub(
        "_[a-z]", lambda m: m.group(0)[1:].upper(), std[1:]
    ).replace("_", "")
    return std


def propname(name: str) -> str:
    std = _re.sub(r"[-\s_]+", "_", name)
    std = _re.sub(r"\W|^(?=\d)", "_", std)
    std = std[0].lower() + _re.sub("[A-Z]", lambda m: m.group(0)[1:].lower(), std[1:])
    return std


def str_(txt: "bytes|str") -> str:
    if isinstance(txt, str):
        return txt
    return _ty.cast(bytes, txt).decode()


def bytes_(txt: "bytes|str") -> bytes:
    if isinstance(txt, str):
        return txt.encode()
    return txt


def merge(*partials: _Map, **partial):
    merged = {}
    for partial in [*partials, partial]:
        if partial:
            merged.update(partial)
    return merged


class _Missing: ...


MISSING = _Missing


def diff(base: _Map, against: _Map):
    d = {}
    for k, v in against.items():
        if base.get(k, MISSING) != v:
            d[k] = v
    return d


import logging

def add_logging_level(name:str, level:int, force=False):
    name = name.upper()
    if hasattr(logging, name) and not force:
        return
    setattr(logging, name, level)
    logging.addLevelName(level, name)

    def log_logger(self: logging.Logger, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    name = name.lower()
    setattr(logging.getLoggerClass(), name, log_logger)

    def log_root(msg, *args, **kwargs):
        logging.log(level, msg, *args, **kwargs)

    setattr(logging, name, log_root)

import asyncio

try:
    import nest_asyncio #type:ignore
except ImportError:
    from .vendor import nest_asyncio

nest_asyncio.apply()

_T = _ty.TypeVar('_T')


def async_to_sync(awaitable: _ty.Awaitable[_T])->_T:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(awaitable)

def isbytelike(obj):
    return  isinstance(obj, (memoryview, bytes, bytearray))