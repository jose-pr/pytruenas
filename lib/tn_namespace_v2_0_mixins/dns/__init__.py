
from pytruenas.base import Namespace

import typing
from enum import Enum

class Dns(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'dns')

    Nameserver = typing.TypedDict('Nameserver', {
            'nameserver':'str',
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
