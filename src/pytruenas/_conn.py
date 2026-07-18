"""Connection layer: re-exports the middleware client and its exceptions.

Kept as a thin indirection so the rest of the package imports ``_conn.Client``/
``_conn.ClientException`` without caring which client implementation backs it.
"""

from .jsonrpc import (
    CALL_TIMEOUT,
    CallTimeout,
    Client,
    ClientException,
    ValidationErrors,
)

__all__ = [
    "CALL_TIMEOUT",
    "CallTimeout",
    "Client",
    "ClientException",
    "ValidationErrors",
]
