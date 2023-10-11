
from pytruenas.base import Namespace

import typing
from enum import Enum

class Systemdataset(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'systemdataset')

    SysdatasetUpdate = typing.TypedDict('SysdatasetUpdate', {
            'pool':'typing.Optional[str]',
            'pool_exclude':'typing.Optional[str]',
            'syslog':'bool',
    })
    SystemdatasetEntry = typing.TypedDict('SystemdatasetEntry', {
            'id':'int',
            'pool':'str',
            'pool_set':'bool',
            'uuid':'str',
            'uuid_b':'typing.Optional[str]',
            'basename':'str',
            'uuid_a':'str',
            'syslog':'bool',
            'path':'typing.Optional[str]',
    })
    SystemdatasetUpdateReturns = typing.TypedDict('SystemdatasetUpdateReturns', {
            'id':'int',
            'pool':'str',
            'pool_set':'bool',
            'uuid':'str',
            'uuid_b':'typing.Optional[str]',
            'basename':'str',
            'uuid_a':'str',
            'syslog':'bool',
            'path':'typing.Optional[str]',
    })
