
from pytruenas import Namespace
import typing
class Group(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'group')

    GroupCreate = typing.TypedDict('GroupCreate', {
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
    GetGroupObj = typing.TypedDict('GetGroupObj', {
            'groupname':'str',
            'gid':'int',
    })
    GroupInfo = typing.TypedDict('GroupInfo', {
            'gr_name':'str',
            'gr_gid':'int',
            'gr_mem':'list',
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
    GroupEntry_ = typing.TypedDict('GroupEntry_', {
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
    GroupEntry__ = typing.TypedDict('GroupEntry__', {
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
    GroupUpdate = typing.TypedDict('GroupUpdate', {
            'gid':'int',
            'name':'str',
            'smb':'bool',
            'sudo_commands':'list[str]',
            'sudo_commands_nopasswd':'list[str]',
            'allow_duplicate_gid':'bool',
            'users':'list[int]',
    })
