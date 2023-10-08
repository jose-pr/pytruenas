
from pytruenas import Namespace
class IpmiMc(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ipmi.mc')

