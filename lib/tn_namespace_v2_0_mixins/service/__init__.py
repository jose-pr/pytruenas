
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class Service(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'service')

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
    ServiceEntry = typing.TypedDict('ServiceEntry', {
            'id':'int',
            'service':'str',
            'enable':'bool',
            'state':'str',
            'pids':'list[int]',
    })
    ServiceEntry_ = typing.TypedDict('ServiceEntry_', {
            'id':'int',
            'service':'str',
            'enable':'bool',
            'state':'str',
            'pids':'list[int]',
    })
    ServiceEntry__ = typing.TypedDict('ServiceEntry__', {
            'id':'int',
            'service':'str',
            'enable':'bool',
            'state':'str',
            'pids':'list[int]',
    })
    ServiceControl = typing.TypedDict('ServiceControl', {
            'ha_propagate':'bool',
            'silent':'bool',
    })
    ServiceUpdate = typing.TypedDict('ServiceUpdate', {
            'enable':'bool',
    })
