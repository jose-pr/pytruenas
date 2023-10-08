
from pytruenas import Namespace
class Alert(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'alert')

