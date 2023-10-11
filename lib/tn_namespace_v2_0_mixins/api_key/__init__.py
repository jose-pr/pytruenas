
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Api_key(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'api_key')

    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'Method',
            'resource':'str',
    })
    ApiKeyCreate = typing.TypedDict('ApiKeyCreate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
    })
    ApiKeyUpdate = typing.TypedDict('ApiKeyUpdate', {
            'name':'str',
            'allowlist':'list[AllowlistItem]',
            'reset':'bool',
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
