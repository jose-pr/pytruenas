
from pytruenas import Namespace
class Ipmi(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ipmi')

