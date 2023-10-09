
from pytruenas.base import Namespace

import typing
from enum import Enum

class Ups(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ups')

    class Mode(str,Enum):
        MASTER = 'MASTER'
        SLAVE = 'SLAVE'
        ...
    class Shutdown(str,Enum):
        LOWBATT = 'LOWBATT'
        BATT = 'BATT'
        ...
    UpsEntry = typing.TypedDict('UpsEntry', {
            'powerdown':'bool',
            'rmonitor':'bool',
            'id':'int',
            'nocommwarntime':'typing.Optional[int]',
            'remoteport':'int',
            'shutdowntimer':'int',
            'hostsync':'int',
            'description':'str',
            'driver':'str',
            'extrausers':'str',
            'identifier':'str',
            'mode':'Mode',
            'monpwd':'str',
            'monuser':'str',
            'options':'str',
            'optionsupsd':'str',
            'port':'str',
            'remotehost':'str',
            'shutdown':'Shutdown',
            'shutdowncmd':'typing.Optional[str]',
            'complete_identifier':'str',
    })
    UpsUpdate = typing.TypedDict('UpsUpdate', {
            'powerdown':'bool',
            'rmonitor':'bool',
            'nocommwarntime':'typing.Optional[int]',
            'remoteport':'int',
            'shutdowntimer':'int',
            'hostsync':'int',
            'description':'str',
            'driver':'str',
            'extrausers':'str',
            'identifier':'str',
            'mode':'Mode',
            'monpwd':'str',
            'monuser':'str',
            'options':'str',
            'optionsupsd':'str',
            'port':'str',
            'remotehost':'str',
            'shutdown':'Shutdown',
            'shutdowncmd':'typing.Optional[str]',
    })
    UpsUpdateReturns = typing.TypedDict('UpsUpdateReturns', {
            'powerdown':'bool',
            'rmonitor':'bool',
            'id':'int',
            'nocommwarntime':'typing.Optional[int]',
            'remoteport':'int',
            'shutdowntimer':'int',
            'hostsync':'int',
            'description':'str',
            'driver':'str',
            'extrausers':'str',
            'identifier':'str',
            'mode':'Mode',
            'monpwd':'str',
            'monuser':'str',
            'options':'str',
            'optionsupsd':'str',
            'port':'str',
            'remotehost':'str',
            'shutdown':'Shutdown',
            'shutdowncmd':'typing.Optional[str]',
            'complete_identifier':'str',
    })
