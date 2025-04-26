from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class User(_NS):
    
    def create(self,
        user_create:CreateUserCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Create a new user."""
        ...
    def delete(self,
        id:int,
        options:DeleteOptions={'delete_group': True},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Delete user `id`.

The `delete_group` option deletes the user primary group if it is not being used by any other user."""
        ...
    def get_instance(self,
        id:int,
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def get_next_uid(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Get the next available/free uid."""
        ...
    def get_user_obj(self,
        get_user_obj:GetUserObjGetUserObj,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetUserObjReturn:
        """Returns dictionary containing information from struct passwd for the user specified by either the username or uid. Bypasses user cache.

NOTE: results will not include nested groups for Active Directory users."""
        ...
    def has_local_administrator_set_up(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Return whether a local administrator with a valid password exists.

This is used when the system is installed without a password and must be set on first use/login."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryUserQueryResultItem]|QueryUserQueryResultItem|int:
        """Query users with `query-filters` and `query-options`.

If users provided by Active Directory or LDAP are not desired, then "local", "=", True should be added to filters."""
        ...
    def renew_2fa_secret(self,
        username:str,
        twofactor_options:Renew2faSecretTwofactorOptions,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Renew2faSecretReturn:
        """Renew `username` user's two-factor authentication secret.

NOTE: This username must match the authenticated username unless authenticated credentials have FULL_ADMIN role."""
        ...
    def set_password(self,
        set_password_data:SetPasswordSetPasswordData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Set the password of the specified `username` to the `new_password` specified in payload.

ValidationErrors will be raised in the following situations: * username does not exist * account is not local to the NAS (Active Directory, LDAP, etc) * account has password authentication disabled * account is locked

NOTE: when authenticated session has less than FULL_ADMIN role, password changes will be rejected if the payload does not match the currently-authenticated user.

NOTE: users authenticated with a one-time password will be able to change the password without submitting a second time."""
        ...
    def setup_local_administrator(self,
        username:str,
        password:str,
        options:SetupLocalAdministratorOptions={'ec2': None},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Set up local administrator (this method does not require authentication if local administrator is not already set up)."""
        ...
    def shell_choices(self,
        group_ids:list[int]=[],
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Return the available shell choices to be used in `user.create` and `user.update`.

`group_ids` is a list of local group IDs for the user."""
        ...
    def unset_2fa_secret(self,
        username:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Unset two-factor authentication secret for `username`."""
        ...
    def update(self,
        id:int,
        user_update:UpdateUserUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update attributes of an existing user."""
        ...
CreateUserCreate = _ty.TypedDict('CreateUserCreate', {
    'uid': _ty.NotRequired[int|None],
    'username': str|str,
    'home': _ty.NotRequired[str],
    'shell': _ty.NotRequired[str],
    'full_name': str,
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'group': _ty.NotRequired[int|None],
    'groups': _ty.NotRequired[list[int]],
    'password_disabled': _ty.NotRequired[bool],
    'ssh_password_enabled': _ty.NotRequired[bool],
    'sshpubkey': _ty.NotRequired[str|None],
    'locked': _ty.NotRequired[bool],
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'email': _ty.NotRequired[str|None],
    'group_create': _ty.NotRequired[bool],
    'home_create': _ty.NotRequired[bool],
    'home_mode': _ty.NotRequired[str],
    'password': _ty.NotRequired[str|None],
    'random_password': _ty.NotRequired[bool], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'uid': int,
    'username': str|str,
    'unixhash': str|None,
    'smbhash': str|None,
    'home': _ty.NotRequired[str],
    'shell': _ty.NotRequired[str],
    'full_name': str,
    'builtin': bool,
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'group': _jsonschema.JsonObject,
    'groups': _ty.NotRequired[list[int]],
    'password_disabled': _ty.NotRequired[bool],
    'ssh_password_enabled': _ty.NotRequired[bool],
    'sshpubkey': _ty.NotRequired[str|None],
    'locked': _ty.NotRequired[bool],
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'email': _ty.NotRequired[str|None],
    'id_type_both': bool,
    'local': bool,
    'immutable': bool,
    'twofactor_auth_configured': bool,
    'sid': str|None,
    'roles': list[str],
    'api_keys': list[int],
    'password': str|None, 
})
DeleteOptions = _ty.TypedDict('DeleteOptions', {
    'delete_group': _ty.NotRequired[bool], 
})
GetInstanceOptions = _ty.TypedDict('GetInstanceOptions', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
GetInstanceReturn = _ty.TypedDict('GetInstanceReturn', {
    'id': int,
    'uid': int,
    'username': str|str,
    'unixhash': str|None,
    'smbhash': str|None,
    'home': _ty.NotRequired[str],
    'shell': _ty.NotRequired[str],
    'full_name': str,
    'builtin': bool,
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'group': _jsonschema.JsonObject,
    'groups': _ty.NotRequired[list[int]],
    'password_disabled': _ty.NotRequired[bool],
    'ssh_password_enabled': _ty.NotRequired[bool],
    'sshpubkey': _ty.NotRequired[str|None],
    'locked': _ty.NotRequired[bool],
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'email': _ty.NotRequired[str|None],
    'id_type_both': bool,
    'local': bool,
    'immutable': bool,
    'twofactor_auth_configured': bool,
    'sid': str|None,
    'roles': list[str],
    'api_keys': list[int], 
})
GetUserObjGetUserObj = _ty.TypedDict('GetUserObjGetUserObj', {
    'username': _ty.NotRequired[str|None],
    'uid': _ty.NotRequired[int|None],
    'get_groups': _ty.NotRequired[bool],
    'sid_info': _ty.NotRequired[bool], 
})
GetUserObjReturn = _ty.TypedDict('GetUserObjReturn', {
    'pw_name': str,
    'pw_gecos': str,
    'pw_dir': str,
    'pw_shell': str,
    'pw_uid': int,
    'pw_gid': int,
    'grouplist': list[int]|None,
    'sid': str|None,
    'source': str,
    'local': bool, 
})
QueryOptions = _ty.TypedDict('QueryOptions', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
QueryUserQueryResultItem = _ty.TypedDict('QueryUserQueryResultItem', {
    'id': _ty.NotRequired[int],
    'uid': _ty.NotRequired[int],
    'username': _ty.NotRequired[str|str],
    'unixhash': _ty.NotRequired[str|None],
    'smbhash': _ty.NotRequired[str|None],
    'home': _ty.NotRequired[str],
    'shell': _ty.NotRequired[str],
    'full_name': _ty.NotRequired[str],
    'builtin': _ty.NotRequired[bool],
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'group': _ty.NotRequired[_jsonschema.JsonObject],
    'groups': _ty.NotRequired[list[int]],
    'password_disabled': _ty.NotRequired[bool],
    'ssh_password_enabled': _ty.NotRequired[bool],
    'sshpubkey': _ty.NotRequired[str|None],
    'locked': _ty.NotRequired[bool],
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'email': _ty.NotRequired[str|None],
    'id_type_both': _ty.NotRequired[bool],
    'local': _ty.NotRequired[bool],
    'immutable': _ty.NotRequired[bool],
    'twofactor_auth_configured': _ty.NotRequired[bool],
    'sid': _ty.NotRequired[str|None],
    'roles': _ty.NotRequired[list[str]],
    'api_keys': _ty.NotRequired[list[int]], 
})
Renew2faSecretTwofactorOptions = _ty.TypedDict('Renew2faSecretTwofactorOptions', {
    'otp_digits': _ty.NotRequired[int],
    'interval': _ty.NotRequired[int], 
})
Renew2faSecretReturn = _ty.TypedDict('Renew2faSecretReturn', {
    'id': int,
    'uid': int,
    'username': str|str,
    'unixhash': str|None,
    'smbhash': str|None,
    'home': _ty.NotRequired[str],
    'shell': _ty.NotRequired[str],
    'full_name': str,
    'builtin': bool,
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'group': _jsonschema.JsonObject,
    'groups': _ty.NotRequired[list[int]],
    'password_disabled': _ty.NotRequired[bool],
    'ssh_password_enabled': _ty.NotRequired[bool],
    'sshpubkey': _ty.NotRequired[str|None],
    'locked': _ty.NotRequired[bool],
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'email': _ty.NotRequired[str|None],
    'id_type_both': bool,
    'local': bool,
    'immutable': bool,
    'twofactor_auth_configured': bool,
    'sid': str|None,
    'roles': list[str],
    'api_keys': list[int],
    'twofactor_config': _jsonschema.JsonValue, 
})
SetPasswordSetPasswordData = _ty.TypedDict('SetPasswordSetPasswordData', {
    'username': str,
    'old_password': _ty.NotRequired[str|None],
    'new_password': str, 
})
SetupLocalAdministratorOptions = _ty.TypedDict('SetupLocalAdministratorOptions', {
    'ec2': _ty.NotRequired[_jsonschema.JsonValue|None], 
})
UpdateUserUpdate = _ty.TypedDict('UpdateUserUpdate', {
    'username': _ty.NotRequired[str|str],
    'home': _ty.NotRequired[str],
    'shell': _ty.NotRequired[str],
    'full_name': _ty.NotRequired[str],
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'group': _ty.NotRequired[int|None],
    'groups': _ty.NotRequired[list[int]],
    'password_disabled': _ty.NotRequired[bool],
    'ssh_password_enabled': _ty.NotRequired[bool],
    'sshpubkey': _ty.NotRequired[str|None],
    'locked': _ty.NotRequired[bool],
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'email': _ty.NotRequired[str|None],
    'home_create': _ty.NotRequired[bool],
    'home_mode': _ty.NotRequired[str],
    'password': _ty.NotRequired[str|None],
    'random_password': _ty.NotRequired[bool], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'uid': int,
    'username': str|str,
    'unixhash': str|None,
    'smbhash': str|None,
    'home': _ty.NotRequired[str],
    'shell': _ty.NotRequired[str],
    'full_name': str,
    'builtin': bool,
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'group': _jsonschema.JsonObject,
    'groups': _ty.NotRequired[list[int]],
    'password_disabled': _ty.NotRequired[bool],
    'ssh_password_enabled': _ty.NotRequired[bool],
    'sshpubkey': _ty.NotRequired[str|None],
    'locked': _ty.NotRequired[bool],
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'email': _ty.NotRequired[str|None],
    'id_type_both': bool,
    'local': bool,
    'immutable': bool,
    'twofactor_auth_configured': bool,
    'sid': str|None,
    'roles': list[str],
    'api_keys': list[int],
    'password': str|None, 
})