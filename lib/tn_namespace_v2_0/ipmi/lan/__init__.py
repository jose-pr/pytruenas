
from pytruenas import Namespace
class IpmiLan(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ipmi.lan')

