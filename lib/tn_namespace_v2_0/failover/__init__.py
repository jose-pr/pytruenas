
from pytruenas import Namespace
class Failover(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'failover')

