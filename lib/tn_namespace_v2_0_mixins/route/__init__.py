
from pytruenas.base import Namespace

import typing
class Route(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'route')

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
    SystemRoute = typing.TypedDict('SystemRoute', {
            'network':'str',
            'netmask':'str',
            'gateway':'typing.Optional[str]',
            'interface':'str',
            'flags':'list',
            'table_id':'int',
            'scope':'int',
            'preferred_source':'typing.Optional[str]',
    })
    SystemRoute_ = typing.TypedDict('SystemRoute_', {
            'network':'str',
            'netmask':'str',
            'gateway':'typing.Optional[str]',
            'interface':'str',
            'flags':'list',
            'table_id':'int',
            'scope':'int',
            'preferred_source':'typing.Optional[str]',
    })
