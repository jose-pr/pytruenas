
from pytruenas import Namespace
class Kmip(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'kmip')

