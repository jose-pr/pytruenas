
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Privilege(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'privilege')

    class Method(str,Enum):
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        DELETE = 'DELETE'
        CALL = 'CALL'
        SUBSCRIBE = 'SUBSCRIBE'
        _ = '*'
        ...
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'Method',
            'resource':'str',
    })
    PrivilegeCreate = typing.TypedDict('PrivilegeCreate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeCreateReturns = typing.TypedDict('PrivilegeCreateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
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
    PrivilegeEntry = typing.TypedDict('PrivilegeEntry', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeEntry_ = typing.TypedDict('PrivilegeEntry_', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeEntry__ = typing.TypedDict('PrivilegeEntry__', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeUpdate = typing.TypedDict('PrivilegeUpdate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    PrivilegeUpdateReturns = typing.TypedDict('PrivilegeUpdateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
