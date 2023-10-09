
from pytruenas import Namespace
import typing
class HardwareMemory(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'hardware.memory')

