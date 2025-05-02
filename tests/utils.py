import argparse
import typing

from pytruenas.utils import text
from pytruenas.utils.cmd import PyTrueNASArgs


class TestArgs(PyTrueNASArgs):
    """Test Argument Parser"""

    untyped = None
    test_opt_arg: typing.Optional[str]
    number_or_string: int | str
    """\\--test,-t\\"""


for arg in TestArgs._getargs_():
    print(arg)

parser = TestArgs.build_parser()
args = parser.parse_args()
print(args)
pass
