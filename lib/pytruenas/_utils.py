
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

_Dict = dict[str, T]


def str_(txt: "bytes|str") -> str:
    if isinstance(txt, str):
        return txt
    return txt.decode()


def bytes_(txt: "bytes|str") -> bytes:
    if isinstance(txt, str):
        return txt.encode()
    return txt

def merge(*partials:_Map,**partial):
    merged = {}
    for partial in [*partials, partial]:
        if partial:
            merged.update(partial)
    return merged

class _Missing():
    ...

MISSING = _Missing

def diff(base:_Map, against:_Map):
    d = {}
    for k, v in against.items():
        if base.get(k, MISSING) != v:
            d[k] = v
    return d