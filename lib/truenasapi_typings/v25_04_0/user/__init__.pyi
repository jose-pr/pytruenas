from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class User(_NS):
    
    def create(self,
        user_create:user_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserCreate:
        """Create a new user."""
        ...
    def delete(self,
        id:int,
        options:options={'delete_group': True},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Delete user `id`.

The `delete_group` option deletes the user primary group if it is not being used by any other user."""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserGet_instance:
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
        get_user_obj:get_user_obj,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserGet_user_obj:
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
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[UserQueryResultItem]|UserQueryResultItem|int:
        """Query users with `query-filters` and `query-options`.

If users provided by Active Directory or LDAP are not desired, then "local", "=", True should be added to filters."""
        ...
    def renew_2fa_secret(self,
        username:str,
        twofactor_options:twofactor_options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserRenew_2fa_secret:
        """Renew `username` user's two-factor authentication secret.

NOTE: This username must match the authenticated username unless authenticated credentials have FULL_ADMIN role."""
        ...
    def set_password(self,
        set_password_data:set_password_data,
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
        options:options={'ec2': None},
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
        user_update:user_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UserUpdate:
        """Update attributes of an existing user."""
        ...
user_create = _ty.TypedDict('user_create', {
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
UserCreate = _ty.TypedDict('UserCreate', {
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
options = _ty.TypedDict('options', {
    'ec2': _ty.NotRequired[_jsonschema.JsonValue|None], 
})
UserGet_instance = _ty.TypedDict('UserGet_instance', {
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
get_user_obj = _ty.TypedDict('get_user_obj', {
    'username': _ty.NotRequired[str|None],
    'uid': _ty.NotRequired[int|None],
    'get_groups': _ty.NotRequired[bool],
    'sid_info': _ty.NotRequired[bool], 
})
UserGet_user_obj = _ty.TypedDict('UserGet_user_obj', {
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
UserQueryResultItem = _ty.TypedDict('UserQueryResultItem', {
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
twofactor_options = _ty.TypedDict('twofactor_options', {
    'otp_digits': _ty.NotRequired[int],
    'interval': _ty.NotRequired[int], 
})
UserRenew_2fa_secret = _ty.TypedDict('UserRenew_2fa_secret', {
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
set_password_data = _ty.TypedDict('set_password_data', {
    'username': str,
    'old_password': _ty.NotRequired[str|None],
    'new_password': str, 
})
user_update = _ty.TypedDict('user_update', {
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
UserUpdate = _ty.TypedDict('UserUpdate', {
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