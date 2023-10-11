
from pytruenas.base import Namespace

import typing
from enum import Enum

class Privilege(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'privilege')

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
    PrivilegeCreate = typing.TypedDict('PrivilegeCreate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[int]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeCreateReturns = typing.TypedDict('PrivilegeCreateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[int]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeEntry = typing.TypedDict('PrivilegeEntry', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[int]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeUpdate = typing.TypedDict('PrivilegeUpdate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[int]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeUpdateReturns = typing.TypedDict('PrivilegeUpdateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[int]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
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
