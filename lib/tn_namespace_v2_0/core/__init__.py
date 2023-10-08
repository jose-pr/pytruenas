
from pytruenas import Namespace
class Core(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'core')

