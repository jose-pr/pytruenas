
from pytruenas import Namespace
class Privilege(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'privilege')

