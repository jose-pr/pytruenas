
from pytruenas import Namespace
class Nfs(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'nfs')

