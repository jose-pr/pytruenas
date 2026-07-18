"""Run an awaitable to completion from synchronous code.

``asyncssh`` is fully async, but ``pytruenas`` presents a synchronous API, so
each SSH/SFTP operation is driven to completion here. ``nest_asyncio`` (pulled
in by the optional ``ssh`` extra) is applied when available so this works even
when called from inside an already-running event loop; without it, the plain
``run_until_complete`` path still works for the common (no running loop) case.
"""

import asyncio
import typing as _ty

_T = _ty.TypeVar("_T")

#: Whether ``nest_asyncio.apply()`` has been run. Deferred until a nested run is
#: actually needed: ``apply()`` eagerly patches ``asyncio`` (incl. the event-loop
#: policy, whose accessor is deprecated and slated for removal in 3.16), so doing
#: it at import time emits a DeprecationWarning on every import even when no
#: nested run ever happens. Applying it lazily keeps the common no-nesting path
#: warning-free.
_nest_asyncio_applied = False


def _ensure_nest_asyncio() -> bool:
    """Apply ``nest_asyncio`` on first need; return True if it is available."""
    global _nest_asyncio_applied
    try:
        import nest_asyncio
    except ImportError:
        return False
    if not _nest_asyncio_applied:
        nest_asyncio.apply()
        _nest_asyncio_applied = True
    return True


#: Reused loop for the common "no loop running in this thread" path, created
#: lazily. Avoids ``asyncio.get_event_loop()`` (deprecated when there is no
#: current loop; the underlying policy API is slated for removal in 3.16).
_LOOP: "asyncio.AbstractEventLoop | None" = None


def async_to_sync(awaitable: "_ty.Awaitable[_T]") -> "_T":
    """Drive ``awaitable`` to completion from synchronous code.

    If a loop is already running in this thread, reuse it (``nest_asyncio``, when
    installed, makes ``run_until_complete`` re-entrant so this works from inside
    an ``async`` caller). Otherwise run on a lazily-created, thread-owned loop --
    without ``asyncio.get_event_loop()`` (deprecated; policy API slated for
    removal in Python 3.16).
    """
    global _LOOP
    try:
        running = asyncio.get_running_loop()
    except RuntimeError:
        running = None

    if running is not None:
        # A loop is already running in this thread; a nested run_until_complete
        # needs nest_asyncio (the ssh extra). Apply it lazily now -- only here,
        # so the common no-nesting path never triggers its deprecated policy
        # patch. Without nest_asyncio installed, run_until_complete raises the
        # usual "This event loop is already running", same as before.
        _ensure_nest_asyncio()
        return running.run_until_complete(awaitable)

    if _LOOP is None or _LOOP.is_closed():
        _LOOP = asyncio.new_event_loop()
    return _LOOP.run_until_complete(awaitable)
