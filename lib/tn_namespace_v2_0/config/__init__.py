
from pytruenas import Namespace
class Config(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'config')

