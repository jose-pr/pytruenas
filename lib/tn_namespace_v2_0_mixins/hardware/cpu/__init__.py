
from pytruenas.base import Namespace

import typing
class HardwareCpu(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'hardware.cpu')

