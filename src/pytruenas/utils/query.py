from __future__ import annotations

import typing as _ty

from .io import json_scalar as _json_scalar


class _Exclude: ...


EXCLUDE = _Exclude()


class QueryFilter:

    def __init__(self, operator: str, rhs):
        self._queryfilter_ = (operator, rhs)

    @classmethod
    def filter(cls, lhs: str, filter: object):
        sqlfilter = getattr(filter, "_queryfilter_", None)
        if not sqlfilter:
            sqlfilter = EQ(filter)._queryfilter_
        return sqlfilter(lhs) if callable(sqlfilter) else (lhs, *sqlfilter)


class EQ(QueryFilter):
    def __init__(self, rhs):
        super().__init__("=", rhs)


class NE(QueryFilter):
    def __init__(self, rhs):
        super().__init__("!=", rhs)


class RE(QueryFilter):
    def __init__(self, rhs):
        super().__init__("~", rhs)


class GT(QueryFilter):
    def __init__(self, rhs):
        super().__init__(">", rhs)


class GE(QueryFilter):
    def __init__(self, rhs):
        super().__init__(">=", rhs)


class LT(QueryFilter):
    def __init__(self, rhs):
        super().__init__("<", rhs)


class LE(QueryFilter):
    def __init__(self, rhs):
        super().__init__("<=", rhs)


class IN(QueryFilter):
    def __init__(self, rhs):
        super().__init__("in", rhs)


class NIN(QueryFilter):
    def __init__(self, rhs):
        super().__init__("nin", rhs)


def filter_from_kwargs(**kwargs):
    return [
        QueryFilter.filter(name, filter)
        for name, filter in kwargs.items()
        if filter is not EXCLUDE
    ]


class Option:
    def __init__(self, name: str, value):
        self.name = name
        self.value = value

    def _options_(self, dict: dict):
        dict[self.name] = self.value

    @classmethod
    def options(cls, *opts: "Option|object"):
        opts_ = {}
        for opt in opts:
            if hasattr(opt, "_options_"):
                _ty.cast(Option, opt)._options_(opts_)
            elif isinstance(opt, _ty.Mapping):
                opts_.update(opt)
            elif isinstance(opt, (list, tuple)):
                name, val = opt
                opts_[name] = val
            else:
                raise ValueError(opt)
        return opts_


def merge(*partials: _ty.Mapping, **partial):
    merged = {}
    for partial in [*partials, partial]:
        if partial:
            merged.update(partial)
    return merged


class _Missing: ...


MISSING = _Missing


def diff(base: _ty.Mapping, against: _ty.Mapping):
    """Fields in ``against`` that differ from ``base``, normalized for compare.

    ``base`` is what the API just reported (plain JSON scalars); ``against`` is
    what the caller wants. A caller holding a value as a wrapper object --
    ``IPv4Address("1.2.3.4")``, a MAC type, a ``PurePath`` -- is comparing an
    object against the string the API returned, and those are never equal. The
    field then looks changed on EVERY call, so an upsert rewrites it forever
    and reports a change that did not happen.

    Comparison is on the normalized form; the value STORED is the caller's
    original, so whatever the encoder does with it on the way out is unchanged.
    """
    d = {}
    for k, v in against.items():
        current = base.get(k, MISSING)
        if current is MISSING or not _same(current, v):
            d[k] = v
    return d


def _same(current, wanted) -> bool:
    """Whether an API-reported value already matches what the caller wants.

    Tries the plain comparison first -- it is correct for the overwhelmingly
    common all-scalars case and avoids normalizing on every field. Only when
    that says "different" is the wrapper case considered, so this can turn a
    false difference into equality but never the reverse.
    """
    if current == wanted:
        return True
    try:
        return _json_scalar(current) == _json_scalar(wanted)
    except Exception:
        # A __json__ that raises, or an un-stringifiable value: fall back to
        # "different". Reporting a spurious change is recoverable; silently
        # skipping a real one is not.
        return False
