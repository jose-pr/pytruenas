
from pytruenas import Namespace
class Group(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'group')

