
from pytruenas import Namespace
class Vm(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'vm')

