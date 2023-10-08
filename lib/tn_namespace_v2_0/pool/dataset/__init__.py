
from pytruenas import Namespace
class PoolDataset(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.dataset')

