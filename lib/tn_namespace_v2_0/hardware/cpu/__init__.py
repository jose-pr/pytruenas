
from pytruenas import Namespace
class HardwareCpu(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'hardware.cpu')

