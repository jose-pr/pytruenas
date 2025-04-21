import logging as _logging
from . import _utils

_utils.add_logging_level("trace", _logging.DEBUG - 5)
from .client import TrueNASClient
from .namespace import Namespace
from .auth import *
