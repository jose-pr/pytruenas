
from pytruenas import Namespace
class Stats(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'stats')

