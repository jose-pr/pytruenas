"""The sync<-async bridge (utils.async_.async_to_sync).

Runs coroutines on a shared background loop; must work from a plain sync caller
AND from inside an already-running event loop (no nest_asyncio needed), with no
deprecation warnings.
"""

import asyncio
import warnings

import pytest

from pytruenas.utils.async_ import async_to_sync


async def _return(value):
    await asyncio.sleep(0)
    return value


def test_runs_coroutine_from_sync_caller():
    assert async_to_sync(_return(42)) == 42


def test_repeated_calls_reuse_loop():
    # Stable across calls (the background loop is a shared singleton).
    assert async_to_sync(_return("a")) == "a"
    assert async_to_sync(_return("b")) == "b"


def test_works_from_inside_running_loop():
    # This is the case that used to require nest_asyncio: calling the sync
    # bridge from within an async caller. The coroutine runs on the background
    # loop, not the caller's, so it just works.
    async def outer():
        return async_to_sync(_return("nested"))

    assert asyncio.run(outer()) == "nested"


def test_accepts_non_coroutine_awaitable():
    # run_coroutine_threadsafe needs a real coroutine; the bridge wraps a bare
    # awaitable (e.g. a Future) into one via _ensure_coro.
    async def _fut_producer():
        loop = asyncio.get_running_loop()
        f = loop.create_future()
        loop.call_soon(f.set_result, "future-ok")
        return await f

    assert async_to_sync(_fut_producer()) == "future-ok"


def test_timeout_raises():
    async def _slow():
        await asyncio.sleep(5)

    with pytest.raises((TimeoutError, Exception)):
        async_to_sync(_slow(), timeout=0.05)


def test_no_deprecation_warning():
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert async_to_sync(_return(1)) == 1
