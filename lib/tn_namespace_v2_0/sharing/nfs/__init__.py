
from pytruenas import Namespace
class SharingNfs(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'sharing.nfs')

