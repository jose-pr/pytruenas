
from pytruenas import Namespace
class Tunable(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'tunable')

