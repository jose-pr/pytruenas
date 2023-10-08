
from pytruenas import Namespace
class PoolDatasetUserprop(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.dataset.userprop')

