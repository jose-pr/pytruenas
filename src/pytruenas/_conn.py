"""Connection layer: re-exports the middleware client and its exceptions.

Kept as a thin indirection so the rest of the package imports ``_conn.Client``/
``_conn.ClientException`` without caring which client implementation backs it.
"""

from .jsonrpc import (
    CALL_TIMEOUT,
    DEFAULT_EVENT_QUEUE_SIZE,
    CallTimeout,
    Client,
    ClientException,
    Event,
    Subscription,
    ValidationErrors,
)

__all__ = [
    "CALL_TIMEOUT",
    "DEFAULT_EVENT_QUEUE_SIZE",
    "CallTimeout",
    "Client",
    "ClientException",
    "Event",
    "Subscription",
    "ValidationErrors",
]
