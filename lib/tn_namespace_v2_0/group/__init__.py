
from pytruenas.base import Namespace

import typing
from enum import Enum

class Group(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'group')

    GetGroupObj = typing.TypedDict('GetGroupObj', {
            'groupname':'str',
            'gid':'int',
    })
    GroupCreate = typing.TypedDict('GroupCreate', {
            'gid':'int',
            'name':'str',
            'smb':'bool',
            'sudo_commands':'list[str]',
            'sudo_commands_nopasswd':'list[str]',
            'allow_duplicate_gid':'bool',
            'users':'list[int]',
    })
    GroupEntry = typing.TypedDict('GroupEntry', {
            'gid':'int',
            'name':'str',
            'smb':'bool',
            'sudo_commands':'list[str]',
            'sudo_commands_nopasswd':'list[str]',
            'users':'list[int]',
            'id':'int',
            'group':'str',
            'builtin':'bool',
            'id_type_both':'bool',
            'local':'bool',
            'nt_name':'typing.Optional[str]',
            'sid':'typing.Optional[str]',
    })
    GroupInfo = typing.TypedDict('GroupInfo', {
            'gr_name':'str',
            'gr_gid':'int',
            'gr_mem':'list',
    })
    GroupUpdate = typing.TypedDict('GroupUpdate', {
            'gid':'int',
            'name':'str',
            'smb':'bool',
            'sudo_commands':'list[str]',
            'sudo_commands_nopasswd':'list[str]',
            'allow_duplicate_gid':'bool',
            'users':'list[int]',
    })
    Options = typing.TypedDict('Options', {
            'delete_users':'bool',
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
