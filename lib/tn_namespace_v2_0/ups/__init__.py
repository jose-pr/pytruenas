
from pytruenas import Namespace
class Ups(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ups')

