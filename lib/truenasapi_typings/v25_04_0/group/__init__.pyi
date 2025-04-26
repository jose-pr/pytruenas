from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Group(_NS):
    
    def create(self,
        group_create:CreateGroupCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Create a new group."""
        ...
    def delete(self,
        id:int,
        options:DeleteOptions={'delete_users': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Delete group `id`.

The `delete_users` option deletes all users that have this group as their primary group."""
        ...
    def get_group_obj(self,
        get_group_obj:GetGroupObjGetGroupObj,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetGroupObjReturn:
        """Returns dictionary containing information from struct grp for the group specified by either the `groupname` or `gid`.

If `sid_info` is specified then addition SMB / domain information is returned for the group."""
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
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryGroupQueryResultItem]|QueryGroupQueryResultItem|int:
        """Query groups with `query-filters` and `query-options`."""
        ...
    def update(self,
        id:int,
        group_update:UpdateGroupUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Update attributes of an existing group."""
        ...
CreateGroupCreate = _ty.TypedDict('CreateGroupCreate', {
    'gid': _ty.NotRequired[int|None],
    'name': str,
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'users': _ty.NotRequired[list[int]], 
})
DeleteOptions = _ty.TypedDict('DeleteOptions', {
    'delete_users': _ty.NotRequired[bool], 
})
GetGroupObjGetGroupObj = _ty.TypedDict('GetGroupObjGetGroupObj', {
    'groupname': _ty.NotRequired[str|None],
    'gid': _ty.NotRequired[int|None],
    'sid_info': _ty.NotRequired[bool], 
})
GetGroupObjReturn = _ty.TypedDict('GetGroupObjReturn', {
    'gr_name': str,
    'gr_gid': int,
    'gr_mem': list[str],
    'sid': _ty.NotRequired[str|None],
    'source': str,
    'local': bool, 
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
QueryGroupQueryResultItem = _ty.TypedDict('QueryGroupQueryResultItem', {
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
UpdateGroupUpdate = _ty.TypedDict('UpdateGroupUpdate', {
    'name': _ty.NotRequired[str],
    'sudo_commands': _ty.NotRequired[list[str]],
    'sudo_commands_nopasswd': _ty.NotRequired[list[str]],
    'smb': _ty.NotRequired[bool],
    'userns_idmap': _ty.NotRequired[str|int|None],
    'users': _ty.NotRequired[list[int]], 
})