
from pytruenas.base import Namespace

import typing
class Ipmi(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ipmi')

