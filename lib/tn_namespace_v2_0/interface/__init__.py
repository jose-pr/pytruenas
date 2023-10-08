
from pytruenas import Namespace
class Interface(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'interface')

