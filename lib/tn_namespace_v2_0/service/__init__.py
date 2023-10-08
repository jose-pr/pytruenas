
from pytruenas import Namespace
class Service(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'service')

