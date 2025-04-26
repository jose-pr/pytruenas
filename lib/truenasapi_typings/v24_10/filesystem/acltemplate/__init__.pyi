from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class FilesystemAcltemplate(_NS):
    
    def by_path(self,
        filesystem_acl:filesystem_acl,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AclTemplateEntry]:
        """Retrieve list of available ACL templates for a given `path`.

Supports `query-filters` and `query-options`. `format-options` gives additional options to alter the results of the template query:

`canonicalize` - place ACL entries for NFSv4 ACLs in Microsoft canonical order. `ensure_builtins` - ensure all results contain entries for `builtin_users` and `builtin_administrators` groups. `resolve_names` - convert ids in ACL entries into names."""
        ...
    def create(self,
        acltemplate_create:acltemplate_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> FilesystemAcltemplateCreate:
        """Create a new filesystem ACL template."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """"""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> FilesystemAcltemplateGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AclTemplateQueryResultItem]|AclTemplateQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        acltemplate_update:acltemplate_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> FilesystemAcltemplateUpdate:
        """update filesystem ACL template with `id`."""
        ...
filesystem_acl = _ty.TypedDict('filesystem_acl', {
    'path': _ty.NotRequired[str],
    'query-filters': _ty.NotRequired[_jsonschema.JsonArray],
    'query-options': _ty.NotRequired[_jsonschema.JsonValue],
    'format-options': _ty.NotRequired[_jsonschema.JsonValue], 
})
AclTemplateEntry = _ty.TypedDict('AclTemplateEntry', {
    'id': int,
    'builtin': bool,
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})
acltemplate_create = _ty.TypedDict('acltemplate_create', {
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})
FilesystemAcltemplateCreate = _ty.TypedDict('FilesystemAcltemplateCreate', {
    'id': int,
    'builtin': bool,
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
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
FilesystemAcltemplateGet_instance = _ty.TypedDict('FilesystemAcltemplateGet_instance', {
    'id': int,
    'builtin': bool,
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})
AclTemplateQueryResultItem = _ty.TypedDict('AclTemplateQueryResultItem', {
    'id': _ty.NotRequired[int],
    'builtin': _ty.NotRequired[bool],
    'name': _ty.NotRequired[str],
    'acltype': _ty.NotRequired[str],
    'acl': _ty.NotRequired[_jsonschema.JsonArray|_jsonschema.JsonArray],
    'comment': _ty.NotRequired[str], 
})
acltemplate_update = _ty.TypedDict('acltemplate_update', {
    'name': _ty.NotRequired[str],
    'acltype': _ty.NotRequired[str],
    'acl': _ty.NotRequired[_jsonschema.JsonArray|_jsonschema.JsonArray],
    'comment': _ty.NotRequired[str], 
})
FilesystemAcltemplateUpdate = _ty.TypedDict('FilesystemAcltemplateUpdate', {
    'id': int,
    'builtin': bool,
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})