
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
class Ups(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ups')

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
            'mode':'str',
            'monpwd':'str',
            'monuser':'str',
            'options':'str',
            'optionsupsd':'str',
            'port':'str',
            'remotehost':'str',
            'shutdown':'str',
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
            'mode':'str',
            'monpwd':'str',
            'monuser':'str',
            'options':'str',
            'optionsupsd':'str',
            'port':'str',
            'remotehost':'str',
            'shutdown':'str',
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
            'mode':'str',
            'monpwd':'str',
            'monuser':'str',
            'options':'str',
            'optionsupsd':'str',
            'port':'str',
            'remotehost':'str',
            'shutdown':'str',
            'shutdowncmd':'typing.Optional[str]',
            'complete_identifier':'str',
    })
