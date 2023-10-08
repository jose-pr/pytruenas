
from pytruenas import Namespace
class ClusterManagement(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cluster.management')

