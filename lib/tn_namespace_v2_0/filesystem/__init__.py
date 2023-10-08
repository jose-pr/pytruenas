
from pytruenas import Namespace
class Filesystem(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'filesystem')

