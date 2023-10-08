
from pytruenas import Namespace
class Idmap(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'idmap')

