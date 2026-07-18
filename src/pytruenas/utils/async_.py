"""Run an awaitable to completion from synchronous code.

``asyncssh`` is fully async, but ``pytruenas`` presents a synchronous API, so
each SSH/SFTP operation is driven to completion here. ``nest_asyncio`` (pulled
in by the optional ``ssh`` extra) is applied when available so this works even
when called from inside an already-running event loop; without it, the plain
``run_until_complete`` path still works for the common (no running loop) case.
"""

import asyncio
import typing as _ty

try:
    import nest_asyncio as _nest_asyncio

    _nest_asyncio.apply()
except ImportError:
    _nest_asyncio = None

_T = _ty.TypeVar("_T")


def async_to_sync(awaitable: "_ty.Awaitable[_T]") -> "_T":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(awaitable)
