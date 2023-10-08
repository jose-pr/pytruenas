
from pytruenas import Namespace
class PoolResilver(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.resilver')

