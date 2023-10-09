
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class CtdbPrivateIps(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ctdb.private.ips')

    PrivateCreate = typing.TypedDict('PrivateCreate', {
            'ip':'str',
            'node_uuid':'str',
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
    PrivateUpdate = typing.TypedDict('PrivateUpdate', {
            'enable':'bool',
            'node_uuid':'str',
    })
