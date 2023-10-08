
from pytruenas import Namespace
class Dns(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'dns')

