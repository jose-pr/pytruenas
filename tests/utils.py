from pytruenas.cli import PyTrueNASArgs
from pytruenas.utils import logging

logging.init_stderr_logging(level=logging.DEBUG)


parser = PyTrueNASArgs.build_parser()
args = parser.parse_args()
print(args)
loglevels = args.set_loglevels()
pass
