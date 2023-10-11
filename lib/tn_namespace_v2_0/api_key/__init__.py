
from pytruenas.base import Namespace

import typing
from enum import Enum

class Api_key(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'api_key')

    ApiKeyCreate = typing.TypedDict('ApiKeyCreate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
    })
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'Method',
            'resource':'str',
    })
    class Method(str,Enum):
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        DELETE = 'DELETE'
        CALL = 'CALL'
        SUBSCRIBE = 'SUBSCRIBE'
        All = '*'
        ...
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
