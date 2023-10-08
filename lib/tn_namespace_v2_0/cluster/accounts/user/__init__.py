
from pytruenas import Namespace
class ClusterAccountsUser(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cluster.accounts.user')

