
from pytruenas import Namespace
class Pool(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool')

