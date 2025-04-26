from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Privilege(_NS):
    
    def create(self,
        privilege_create:privilege_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PrivilegeCreate:
        """Creates a privilege.

`name` is a name for privilege (must be unique).

`local_groups` is a list of local user account group GIDs that gain this privilege.

`ds_groups` is list of Directory Service group GIDs that will gain this privilege.

`roles` is a list of roles to be assigned to the privilege

`web_shell` controls whether users with this privilege are allowed to log in to the Web UI."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete the privilege `id`."""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PrivilegeGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[PrivilegeQueryResultItem]|PrivilegeQueryResultItem|int:
        """"""
        ...
    def roles(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[PrivilegeRoleQueryResultItem]|PrivilegeRoleQueryResultItem|int:
        """Get all available roles.

Each entry contains the following keys:

`name` - the internal name of the role

`includes` - list of other roles that this role includes. When user is granted this role, they will also receive permissions granted by all the included roles.

`builtin` - role exists for internal backend purposes for access control."""
        ...
    def update(self,
        id:int,
        privilege_update:privilege_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PrivilegeUpdate:
        """Update the privilege `id`."""
        ...
privilege_create = _ty.TypedDict('privilege_create', {
    'name': str,
    'local_groups': _ty.NotRequired[list[int]],
    'ds_groups': _ty.NotRequired[list[int|str]],
    'roles': _ty.NotRequired[list[str]],
    'web_shell': bool, 
})
PrivilegeCreate = _ty.TypedDict('PrivilegeCreate', {
    'id': int,
    'builtin_name': str|None,
    'name': str,
    'local_groups': list[_jsonschema.JsonValue|_jsonschema.JsonValue],
    'ds_groups': list[_jsonschema.JsonValue|_jsonschema.JsonValue],
    'roles': _ty.NotRequired[list[str]],
    'web_shell': bool, 
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
PrivilegeGet_instance = _ty.TypedDict('PrivilegeGet_instance', {
    'id': int,
    'builtin_name': str|None,
    'name': str,
    'local_groups': list[_jsonschema.JsonValue|_jsonschema.JsonValue],
    'ds_groups': list[_jsonschema.JsonValue|_jsonschema.JsonValue],
    'roles': _ty.NotRequired[list[str]],
    'web_shell': bool, 
})
PrivilegeQueryResultItem = _ty.TypedDict('PrivilegeQueryResultItem', {
    'id': _ty.NotRequired[int],
    'builtin_name': _ty.NotRequired[str|None],
    'name': _ty.NotRequired[str],
    'local_groups': _ty.NotRequired[list[_jsonschema.JsonValue|_jsonschema.JsonValue]],
    'ds_groups': _ty.NotRequired[list[_jsonschema.JsonValue|_jsonschema.JsonValue]],
    'roles': _ty.NotRequired[list[str]],
    'web_shell': _ty.NotRequired[bool], 
})
PrivilegeRoleQueryResultItem = _ty.TypedDict('PrivilegeRoleQueryResultItem', {
    'name': _ty.NotRequired[str],
    'title': _ty.NotRequired[str],
    'includes': _ty.NotRequired[list[str]],
    'builtin': _ty.NotRequired[bool],
    'stig': _ty.NotRequired[_jsonschema.JsonValue|None], 
})
privilege_update = _ty.TypedDict('privilege_update', {
    'name': _ty.NotRequired[str],
    'local_groups': _ty.NotRequired[list[int]],
    'ds_groups': _ty.NotRequired[list[int|str]],
    'roles': _ty.NotRequired[list[str]],
    'web_shell': _ty.NotRequired[bool], 
})
PrivilegeUpdate = _ty.TypedDict('PrivilegeUpdate', {
    'id': int,
    'builtin_name': str|None,
    'name': str,
    'local_groups': list[_jsonschema.JsonValue|_jsonschema.JsonValue],
    'ds_groups': list[_jsonschema.JsonValue|_jsonschema.JsonValue],
    'roles': _ty.NotRequired[list[str]],
    'web_shell': bool, 
})