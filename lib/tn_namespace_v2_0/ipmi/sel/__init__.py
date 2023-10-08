
from pytruenas import Namespace
class IpmiSel(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ipmi.sel')

