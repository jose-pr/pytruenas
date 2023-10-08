
from pytruenas import Namespace
class PoolScrub(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.scrub')

