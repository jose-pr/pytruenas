
from pytruenas.base import Namespace

import typing
from enum import Enum

class Tunable(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'tunable')

    TunableCreate = typing.TypedDict('TunableCreate', {
            'type':'Type',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
    })
    class Type(str,Enum):
        SYSCTL = 'SYSCTL'
        UDEV = 'UDEV'
        ZFS = 'ZFS'
        ...
    TunableCreateReturns = typing.TypedDict('TunableCreateReturns', {
            'type':'Type',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
            'id':'int',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    TunableEntry = typing.TypedDict('TunableEntry', {
            'type':'Type',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
            'id':'int',
    })
    TunableTypeChoices = typing.TypedDict('TunableTypeChoices', {
            'SYSCTL':'SYSCTL',
            'UDEV':'UDEV',
            'ZFS':'ZFS',
    })
    class SYSCTL(str,Enum):
        SYSCTL = 'SYSCTL'
        ...
    class UDEV(str,Enum):
        UDEV = 'UDEV'
        ...
    class ZFS(str,Enum):
        ZFS = 'ZFS'
        ...
    TunableUpdate = typing.TypedDict('TunableUpdate', {
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
    })
    TunableUpdateReturns = typing.TypedDict('TunableUpdateReturns', {
            'type':'Type',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
            'id':'int',
    })
