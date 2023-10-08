
from pytruenas import Namespace
class Smart(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'smart')

