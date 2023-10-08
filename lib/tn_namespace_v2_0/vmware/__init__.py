
from pytruenas import Namespace
class Vmware(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'vmware')

