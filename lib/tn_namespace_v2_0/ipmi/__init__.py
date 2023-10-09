
from pytruenas.base import Namespace

import typing
from enum import Enum

class Ipmi(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ipmi')

