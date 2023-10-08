
from pytruenas import Namespace
class Staticroute(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'staticroute')

