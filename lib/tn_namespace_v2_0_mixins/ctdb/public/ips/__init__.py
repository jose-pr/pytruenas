
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class CtdbPublicIps(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ctdb.public.ips')

    PublicCreate = typing.TypedDict('PublicCreate', {
            'pnn':'int',
            'ip':'str',
            'netmask':'int',
            'interface':'str',
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
