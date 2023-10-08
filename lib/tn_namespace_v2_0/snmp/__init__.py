
from pytruenas import Namespace
class Snmp(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'snmp')

