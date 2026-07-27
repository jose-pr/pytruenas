from duho import logging as _logging  # noqa: F401  (registers the TRACE level)
from .namespace import Namespace
from .auth import *
from .connection import Event, Subscription, TrueNASWSConnection
from .host import TrueNASConfig, TrueNASHost
from .host import TrueNASHost as TrueNASClient

try:
    from importlib.metadata import version as _version, PackageNotFoundError

    __version__ = _version("pytruenas")
except PackageNotFoundError:  # not installed (e.g. running from a bare checkout)
    __version__ = "0.0.0.dev0"

__all__ = [
    "Namespace",
    # `TrueNASClient` and `TrueNASHost` are the same class. "Client" reads
    # better at a call site; "Host" is the name its hostctl half is documented
    # under, and what the URI registry dispatches `truenas+wss://` to.
    "TrueNASClient",
    "TrueNASHost",
    "TrueNASConfig",
    "Credentials",
    "Event",
    "Subscription",
    "TrueNASWSConnection",
    "__version__",
]
