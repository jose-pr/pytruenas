import asyncio
import typing as _ty

try:
    import nest_asyncio  # type:ignore
except ImportError:
    from ..vendor import nest_asyncio

nest_asyncio.apply()

_T = _ty.TypeVar("_T")


def async_to_sync(awaitable: _ty.Awaitable[_T]) -> _T:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(awaitable)