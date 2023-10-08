
from pytruenas import Namespace
class InterfaceCapabilities(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'interface.capabilities')

