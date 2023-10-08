
from pytruenas import Namespace
class PoolSnapshottask(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.snapshottask')

