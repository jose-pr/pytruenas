
from pytruenas.base import Namespace

import typing
from enum import Enum

class IpmiChassis(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ipmi.chassis')

    class Verb(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        ...
