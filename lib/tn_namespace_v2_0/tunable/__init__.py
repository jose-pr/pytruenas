
from pytruenas.base import Namespace

import typing
from enum import Enum

class Tunable(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'tunable')

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
    TunableCreate = typing.TypedDict('TunableCreate', {
            'type':'Type',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
    })
    TunableCreateReturns = typing.TypedDict('TunableCreateReturns', {
            'type':'Type',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
            'id':'int',
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
            'SYSCTL':'typing.Literal["SYSCTL"]',
            'UDEV':'typing.Literal["UDEV"]',
            'ZFS':'typing.Literal["ZFS"]',
    })
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
    class Type(str,Enum):
        SYSCTL = 'SYSCTL'
        UDEV = 'UDEV'
        ZFS = 'ZFS'
        ...
