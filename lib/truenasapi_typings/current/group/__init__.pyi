from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Group(_NS):
    
    def create(self,
        group_create:group_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Create a new group."""
        ...
    def delete(self,
        id:int,
        options:options={'delete_users': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Delete group `id`.

The `delete_users` option deletes all users that have this group as their primary group."""
        ...
    def get_group_obj(self,
        get_group_obj:get_group_obj,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GroupGet_group_obj:
        """Returns dictionary containing information from struct grp for the group specified by either the `groupname` or `gid`.

If `sid_info` is specified then addition SMB / domain information is returned for the group."""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GroupGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def get_next_gid(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Get the next available/free gid."""
        ...
    def has_password_enabled_user(self,
        gids:list[int],
        exclude_user_ids:list[int]=[],
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Checks whether at least one local user with a password is a member of any of the `group_ids`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[GroupQueryResultItem]|GroupQueryResultItem|int:
        """Query groups with `query-filters` and `query-options`."""
        ...
    def update(self,
        id:int,
        group_update:group_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Update attributes of an existing group."""
        ...
group_create = _ty.TypedDict('group_create', {
    'gid': _ty.NotRequired[int|None],
    'name': str,
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'users': _ty.NotRequired[list[int]], 
})
options = _ty.TypedDict('options', {
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
get_group_obj = _ty.TypedDict('get_group_obj', {
    'groupname': _ty.NotRequired[str|None],
    'gid': _ty.NotRequired[int|None],
    'sid_info': _ty.NotRequired[bool], 
})
GroupGet_group_obj = _ty.TypedDict('GroupGet_group_obj', {
    'gr_name': str,
    'gr_gid': int,
    'gr_mem': list[str],
    'sid': _ty.NotRequired[str|None],
    'source': str,
    'local': bool, 
})
GroupGet_instance = _ty.TypedDict('GroupGet_instance', {
    'id': int,
    'gid': int,
    'name': str,
    'builtin': bool,
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'group': str,
    'id_type_both': bool,
    'local': bool,
    'sid': str|None,
    'roles': list[str],
    'users': _ty.NotRequired[list[int]], 
})
GroupQueryResultItem = _ty.TypedDict('GroupQueryResultItem', {
    'id': _ty.NotRequired[int],
    'gid': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'builtin': _ty.NotRequired[bool],
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'group': _ty.NotRequired[str],
    'id_type_both': _ty.NotRequired[bool],
    'local': _ty.NotRequired[bool],
    'sid': _ty.NotRequired[str|None],
    'roles': _ty.NotRequired[list[str]],
    'users': _ty.NotRequired[list[int]], 
})
group_update = _ty.TypedDict('group_update', {
    'name': _ty.NotRequired[str],
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'users': _ty.NotRequired[list[int]], 
})