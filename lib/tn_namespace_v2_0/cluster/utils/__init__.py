
from pytruenas import Namespace
import typing
class ClusterUtils(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cluster.utils')

