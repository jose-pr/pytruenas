from duho import logging as _logging  # noqa: F401  (registers the TRACE level)
from .namespace import Namespace
from .auth import *
from .client import TrueNASClient
from .jsonrpc import Event, Subscription

try:
    from importlib.metadata import version as _version, PackageNotFoundError

    __version__ = _version("pytruenas")
except PackageNotFoundError:  # not installed (e.g. running from a bare checkout)
    __version__ = "0.0.0.dev0"

__all__ = [
    "Namespace",
    "TrueNASClient",
    "Credentials",
    "Event",
    "Subscription",
    "__version__",
]
