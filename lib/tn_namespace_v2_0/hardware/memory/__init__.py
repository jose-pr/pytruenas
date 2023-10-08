
from pytruenas import Namespace
class HardwareMemory(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'hardware.memory')

