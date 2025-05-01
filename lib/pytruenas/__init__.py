from .utils import logging as _logging

_logging.add_logging_level("trace", _logging.DEBUG - 5, color=_logging._asicode(36))
from .client import TrueNASClient
from .namespace import Namespace
from .auth import *
