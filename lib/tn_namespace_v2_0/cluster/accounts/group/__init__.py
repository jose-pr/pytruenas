
from pytruenas import Namespace
class ClusterAccountsGroup(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cluster.accounts.group')

