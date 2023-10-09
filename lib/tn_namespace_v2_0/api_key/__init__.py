
from pytruenas.base import Namespace

import typing
class Api_key(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'api_key')

    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
            'resource':'str',
    })
    ApiKeyCreate = typing.TypedDict('ApiKeyCreate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
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
    ApiKeyUpdate = typing.TypedDict('ApiKeyUpdate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
            'reset':'bool',
    })
