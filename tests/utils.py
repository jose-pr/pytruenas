import argparse
import typing

from pytruenas.utils import logging, text
from pytruenas.utils.cmd import PyTrueNASArgs

logging.init_stderr_logging(level=logging.DEBUG)


parser = PyTrueNASArgs.build_parser()
args = parser.parse_args()
print(args)
loglevels = args.set_loglevels()
pass
