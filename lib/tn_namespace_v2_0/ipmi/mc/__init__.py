
from pytruenas import Namespace
import typing
class IpmiMc(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ipmi.mc')

