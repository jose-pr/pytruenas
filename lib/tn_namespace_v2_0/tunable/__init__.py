
from pytruenas.base import Namespace

import typing
class Tunable(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'tunable')

    TunableCreate = typing.TypedDict('TunableCreate', {
            'type':'str',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
    })
    TunableCreateReturns = typing.TypedDict('TunableCreateReturns', {
            'type':'str',
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
            'type':'str',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
            'id':'int',
    })
    TunableTypeChoices = typing.TypedDict('TunableTypeChoices', {
            'SYSCTL':'str',
            'UDEV':'str',
            'ZFS':'str',
    })
    TunableUpdate = typing.TypedDict('TunableUpdate', {
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
    })
    TunableUpdateReturns = typing.TypedDict('TunableUpdateReturns', {
            'type':'str',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
            'id':'int',
    })
