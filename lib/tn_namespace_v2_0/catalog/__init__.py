
from pytruenas import Namespace
class Catalog(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'catalog')

