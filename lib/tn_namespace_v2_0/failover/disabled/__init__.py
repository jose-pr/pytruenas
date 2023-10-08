
from pytruenas import Namespace
class FailoverDisabled(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'failover.disabled')

