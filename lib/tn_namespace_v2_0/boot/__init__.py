
from pytruenas import Namespace
class Boot(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'boot')

