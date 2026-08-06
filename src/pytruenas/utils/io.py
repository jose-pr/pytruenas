from __future__ import annotations

# NOTE: a `STAT_FIELDS` constant used to live here, derived by stat-ing this
# very file at import time and regex-parsing the repr of the result. It was
# already dead -- the `fs/api.py` code that consumed it is gone -- and it made
# importing this module do filesystem I/O, which is why it was found: from a
# zipapp `__file__` is a path INSIDE the archive, so the stat raised
# `NotADirectoryError` and pytruenas could not be imported at all once
# deployed. If something needs the field names again, `os.stat_result` exposes
# them directly (mind that it lists the `_ns` variants and platform extras,
# which the old repr-scrape did not).


def isbytelike(obj):
    return isinstance(obj, (memoryview, bytes, bytearray))


def bytes_(txt: "bytes|str") -> bytes:
    if isinstance(txt, str):
        return txt.encode()
    return txt


def str_(txt: "bytes|str") -> str:
    if isinstance(txt, str):
        return txt
    return txt.decode()


#: Types JSON already handles directly, plus the containers it walks itself.
#: None of these may be reduced: stringifying a dict or list would send a
#: Python repr (``"{'a': 1}"``) where the API expects a real structure.
_JSON_NATIVE = (str, int, float, bool, type(None), dict, list, tuple)


def _is_scalar_wrapper(obj) -> bool:
    """Whether ``obj`` looks like a thin wrapper around a scalar.

    The test is that the type defines its own ``__str__``. That is what
    separates ``IPv4Address("10.0.0.1")`` -> ``"10.0.0.1"`` from an arbitrary
    object whose ``str()`` is the default
    ``<module.Thing object at 0x...>`` -- a repr masquerading as data, which
    must NOT be sent to the API and must raise instead.
    """
    return type(obj).__str__ is not object.__str__


def json_scalar(obj, default=None):
    """Reduce a wrapper object to the scalar the API expects.

    The middleware takes plain JSON, but the natural way to hold a value in
    Python is often a small wrapper -- ``IPv4Address``, a MAC type, a
    ``PurePath``, a domain object around a string or number. Passing one
    straight through raises ``TypeError: not JSON serializable``, which is a
    poor answer when the object knows perfectly well what it is.

    Resolution order:

    1. ``__json__()`` if the object defines one -- the explicit opt-in, and the
       only hook that lets a type choose a NON-string form (a dict, a list, a
       number). Checked on the TYPE, not the instance, so a stray ``__json__``
       key on a mapping is not mistaken for the protocol.
    2. ``str(obj)`` when the type defines its own ``__str__`` -- right for the
       wrapper-around-a-scalar case that motivates this (an address, a MAC, a
       path all stringify to exactly what the API wants).

    Anything else -- a JSON-native value, a container, or an object with the
    DEFAULT ``__str__`` -- goes to ``default``. That last exclusion is the load
    -bearing one: without it every unserializable object would quietly become
    ``"<module.Thing object at 0x...>"``, a repr masquerading as data, and the
    ``TypeError`` that should have surfaced the bug never fires. Containers are
    excluded for the same reason: stringifying a dict sends ``"{'a': 1}"``
    where the API expects a structure.

    `_EJSONEncoder` passes its ``super()`` as ``default``, so those cases still
    raise the normal ``TypeError``.

    A ``__json__`` that raises is deliberately NOT swallowed: it is an explicit
    declaration that the type can serialize itself, so a failure there is a bug
    in that type, and hiding it behind ``str()`` would send a ``repr``-ish
    string to the API instead.
    """
    hook = getattr(type(obj), "__json__", None)
    if hook is not None:
        return hook(obj)
    if not isinstance(obj, _JSON_NATIVE) and _is_scalar_wrapper(obj):
        return str(obj)
    if default is not None:
        return default(obj)
    return obj
