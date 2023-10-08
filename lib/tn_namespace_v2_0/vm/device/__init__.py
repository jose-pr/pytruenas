
from pytruenas import Namespace
class VmDevice(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'vm.device')

