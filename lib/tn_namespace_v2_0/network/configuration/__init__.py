
from pytruenas import Namespace
class NetworkConfiguration(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'network.configuration')

