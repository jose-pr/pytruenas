from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Acltemplate(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[AcltemplateCreate],
    ) -> CreateReturn:
        """"""
        ...
    def _get(self,
        __id_or_filter:int|_ty.Sequence[str]|None=None,
        **fields:_ty.Unpack[Get],
    ) -> GetInstanceReturn|None:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[AcltemplateUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[AcltemplateUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def by_path(self,
        filesystem_acl:ByPathFilesystemAcl,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ByPathAclTemplateEntry]:
        """Retrieve list of available ACL templates for a given `path`.

Supports `query-filters` and `query-options`. `format-options` gives additional options to alter the results of the template query:

`canonicalize` - place ACL entries for NFSv4 ACLs in Microsoft canonical order. `ensure_builtins` - ensure all results contain entries for `builtin_users` and `builtin_administrators` groups. `resolve_names` - convert ids in ACL entries into names."""
        ...
    def create(self,
        acltemplate_create:CreateAcltemplateCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
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
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryAclTemplateQueryResultItem]|QueryAclTemplateQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        acltemplate_update:UpdateAcltemplateUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """update filesystem ACL template with `id`."""
        ...
AcltemplateCreate = _ty.TypedDict('AcltemplateCreate', {
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})
Get = _ty.TypedDict('Get', {
    'id': _ty.NotRequired[int],
    'builtin': _ty.NotRequired[bool],
    'name': _ty.NotRequired[str],
    'acltype': _ty.NotRequired[str],
    'acl': _ty.NotRequired[_jsonschema.JsonArray|_jsonschema.JsonArray],
    'comment': _ty.NotRequired[str], 
})
AcltemplateUpdate = _ty.TypedDict('AcltemplateUpdate', {
    'name': _ty.NotRequired[str],
    'acltype': _ty.NotRequired[str],
    'acl': _ty.NotRequired[_jsonschema.JsonArray|_jsonschema.JsonArray],
    'comment': _ty.NotRequired[str], 
})
ByPathFilesystemAcl = _ty.TypedDict('ByPathFilesystemAcl', {
    'path': _ty.NotRequired[str],
    'query-filters': _ty.NotRequired[_jsonschema.JsonArray],
    'query-options': _ty.NotRequired[_jsonschema.JsonValue],
    'format-options': _ty.NotRequired[_jsonschema.JsonValue], 
})
ByPathAclTemplateEntry = _ty.TypedDict('ByPathAclTemplateEntry', {
    'id': int,
    'builtin': bool,
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})
CreateAcltemplateCreate = _ty.TypedDict('CreateAcltemplateCreate', {
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'builtin': bool,
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
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
    'builtin': bool,
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
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
QueryAclTemplateQueryResultItem = _ty.TypedDict('QueryAclTemplateQueryResultItem', {
    'id': _ty.NotRequired[int],
    'builtin': _ty.NotRequired[bool],
    'name': _ty.NotRequired[str],
    'acltype': _ty.NotRequired[str],
    'acl': _ty.NotRequired[_jsonschema.JsonArray|_jsonschema.JsonArray],
    'comment': _ty.NotRequired[str], 
})
UpdateAcltemplateUpdate = _ty.TypedDict('UpdateAcltemplateUpdate', {
    'name': _ty.NotRequired[str],
    'acltype': _ty.NotRequired[str],
    'acl': _ty.NotRequired[_jsonschema.JsonArray|_jsonschema.JsonArray],
    'comment': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'builtin': bool,
    'name': str,
    'acltype': str,
    'acl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})