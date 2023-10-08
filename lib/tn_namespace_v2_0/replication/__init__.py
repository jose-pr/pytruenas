
from pytruenas import Namespace
class Replication(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'replication')

