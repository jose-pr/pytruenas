from pytruenas.utils import text
from pytruenas.utils.cmd import PyTrueNASArgs
import argparse
import typing

for letter in text.range('a', 'f'):
    print(letter)

for letter in text.range('1', '10'):
    print(letter)


for t in text.expand("test[1-15:x].[text[c-h]]"):
    print(t)

test = argparse.ArgumentParser('test')

class TestArgs(PyTrueNASArgs):
    test_opt_arg: typing.Optional[str]
TestArgs._args_(test)

print(isinstance(typing.Optional[str], type(typing.Optional)))
pass