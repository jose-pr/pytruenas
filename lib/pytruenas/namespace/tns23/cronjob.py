from enum import Enum as _Enum
from typing import (
    TYPE_CHECKING as _TYPING,
    TypedDict as _Dict,
)
from ...exts import MapExtended as _NSMap


class CronjobEntry(_Dict):
    ...


_NS = _NSMap[CronjobEntry]
if _TYPING:

    class _NS(_NSMap[CronjobEntry]):
        ...


class Cronjob(_NS):
    ...
