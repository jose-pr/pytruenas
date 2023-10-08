
from pytruenas import Namespace
class Rsynctask(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'rsynctask')

