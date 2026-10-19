"""A client for the TrueNAS middleware API, and a hostctl host for TrueNAS.

Everything a caller needs is importable from here; see ``__all__``.
"""

from __future__ import annotations

from duho import logging as _logging  # noqa: F401  (registers the TRACE level)

from .auth import (
    ApiKeyAuth,
    BasicAuth,
    Credentials,
    LocalAuth,
    TokenAuth,
)
from .auth import redact_call_args  # noqa: F401  (importable here; not in __all__)
from .connection import Event, Subscription, TrueNASWSConnection
from .exceptions import (
    APIDumpError,
    AuthenticationError,
    CallTimeout,
    ClientException,
    ConnectError,
    ConnectionClosed,
    FieldError,
    JobFailed,
    TrueNASError,
    UnknownMethod,
    ValidationErrors,
)
from .host import TrueNASClient, TrueNASConfig
from .namespace import Namespace

try:
    from importlib.metadata import version as _version, PackageNotFoundError

    __version__ = _version("pytruenas")
except PackageNotFoundError:  # not installed (e.g. running from a bare checkout)
    __version__ = "0.0.0.dev0"

__all__ = [
    "Namespace",
    "TrueNASClient",
    "TrueNASConfig",
    "Credentials",
    "LocalAuth",
    "ApiKeyAuth",
    "TokenAuth",
    "BasicAuth",
    "Event",
    "Subscription",
    "TrueNASWSConnection",
    "__version__",
    # Errors: `TrueNASError` is the base of every one of them.
    "TrueNASError",
    "ClientException",
    "ValidationErrors",
    "CallTimeout",
    "ConnectionClosed",
    "JobFailed",
    "ConnectError",
    "AuthenticationError",
    "APIDumpError",
    "UnknownMethod",
    "FieldError",
]
