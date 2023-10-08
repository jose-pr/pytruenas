
from pytruenas import Namespace
class Keychaincredential(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'keychaincredential')

