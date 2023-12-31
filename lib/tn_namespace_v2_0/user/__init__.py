
from pytruenas.base import Namespace

import typing
from enum import Enum

class User(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'user')

    Ec2 = typing.TypedDict('Ec2', {
            'instance_id':'str',
    })
    GetUserObj = typing.TypedDict('GetUserObj', {
            'username':'str',
            'uid':'int',
            'get_groups':'bool',
            'sid_info':'bool',
    })
    Options = typing.TypedDict('Options', {
            'delete_group':'bool',
    })
    Options_ = typing.TypedDict('Options_', {
            'ec2':'Ec2',
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
    ShellInfo = typing.TypedDict('ShellInfo', {
            'shell_path':'str',
    })
    UserCreate = typing.TypedDict('UserCreate', {
            'uid':'int',
            'username':'str',
            'group':'int',
            'group_create':'bool',
            'home':'str',
            'home_mode':'str',
            'home_create':'bool',
            'shell':'str',
            'full_name':'str',
            'email':'typing.Optional[str]',
            'password':'str',
            'password_disabled':'bool',
            'ssh_password_enabled':'bool',
            'locked':'bool',
            'smb':'bool',
            'sudo_commands':'list[str]',
            'sudo_commands_nopasswd':'list[str]',
            'sshpubkey':'typing.Optional[str]',
            'groups':'list[int]',
    })
    UserEntry = typing.TypedDict('UserEntry', {
            'uid':'int',
            'username':'str',
            'home':'str',
            'shell':'str',
            'full_name':'str',
            'email':'typing.Optional[str]',
            'password_disabled':'bool',
            'ssh_password_enabled':'bool',
            'locked':'bool',
            'smb':'bool',
            'sudo_commands':'list[str]',
            'sudo_commands_nopasswd':'list[str]',
            'sshpubkey':'typing.Optional[str]',
            'groups':'list[int]',
            'group':'dict[str]',
            'id':'int',
            'builtin':'bool',
            'id_type_both':'bool',
            'local':'bool',
            'twofactor_auth_configured':'bool',
            'unixhash':'str',
            'smbhash':'str',
            'nt_name':'typing.Optional[str]',
            'sid':'typing.Optional[str]',
    })
    UserInformation = typing.TypedDict('UserInformation', {
            'pw_name':'str',
            'pw_gecos':'str',
            'pw_dir':'str',
            'pw_shell':'str',
            'pw_uid':'int',
            'pw_gid':'int',
            'grouplist':'list',
            'sid_info':'dict[str]',
    })
    UserUpdate = typing.TypedDict('UserUpdate', {
            'uid':'int',
            'username':'str',
            'group':'int',
            'home':'str',
            'home_mode':'str',
            'home_create':'bool',
            'shell':'str',
            'full_name':'str',
            'email':'typing.Optional[str]',
            'password':'str',
            'password_disabled':'bool',
            'ssh_password_enabled':'bool',
            'locked':'bool',
            'smb':'bool',
            'sudo_commands':'list[str]',
            'sudo_commands_nopasswd':'list[str]',
            'sshpubkey':'typing.Optional[str]',
            'groups':'list[int]',
    })
    class Username(str,Enum):
        Root = 'root'
        Admin = 'admin'
        ...
