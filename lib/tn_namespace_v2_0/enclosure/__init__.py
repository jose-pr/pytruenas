
from pytruenas import Namespace
class Enclosure(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'enclosure')

