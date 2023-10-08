
from pytruenas import Namespace
class NetworkGeneral(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'network.general')

