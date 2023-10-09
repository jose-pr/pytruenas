
from pytruenas.base import Namespace

import typing
class IpmiChassis(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ipmi.chassis')

