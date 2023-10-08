
from pytruenas import Namespace
class ReplicationConfig(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'replication.config')

