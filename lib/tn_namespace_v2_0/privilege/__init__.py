
from pytruenas import Namespace
import typing
class Privilege(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'privilege')

    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
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
    AllowlistItem_ = typing.TypedDict('AllowlistItem_', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreateReturns = typing.TypedDict('PrivilegeCreateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_]',
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
    AllowlistItem__ = typing.TypedDict('AllowlistItem__', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry = typing.TypedDict('PrivilegeEntry', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem__]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem___ = typing.TypedDict('AllowlistItem___', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry_ = typing.TypedDict('PrivilegeEntry_', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem___]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem____ = typing.TypedDict('AllowlistItem____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry__ = typing.TypedDict('PrivilegeEntry__', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_____ = typing.TypedDict('AllowlistItem_____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdate = typing.TypedDict('PrivilegeUpdate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem______ = typing.TypedDict('AllowlistItem______', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdateReturns = typing.TypedDict('PrivilegeUpdateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem______]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
