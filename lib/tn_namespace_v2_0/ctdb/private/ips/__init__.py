
from pytruenas.base import Namespace

import typing
from enum import Enum

class CtdbPrivateIps(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ctdb.private.ips')

    PrivateCreate = typing.TypedDict('PrivateCreate', {
            'ip':'str',
            'node_uuid':'str',
    })
    PrivateUpdate = typing.TypedDict('PrivateUpdate', {
            'enable':'bool',
            'node_uuid':'str',
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
