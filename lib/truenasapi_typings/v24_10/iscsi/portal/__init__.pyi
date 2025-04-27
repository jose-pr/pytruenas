from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Portal(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[IscsiPortalCreate],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[IscsiPortalUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[IscsiPortalUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        iscsi_portal_create:CreateIscsiPortalCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Create a new iSCSI Portal."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete iSCSI Portal `id`."""
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
    def listen_ip_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns possible choices for `listen.ip` attribute of portal create and update."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryIscsiPortalQueryResultItem]|QueryIscsiPortalQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        iscsi_portal_update:UpdateIscsiPortalUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update iSCSI Portal `id`."""
        ...
IscsiPortalCreate = _ty.TypedDict('IscsiPortalCreate', {
    'listen': _jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})
IscsiPortalUpdate = _ty.TypedDict('IscsiPortalUpdate', {
    'listen': _ty.NotRequired[_jsonschema.JsonArray],
    'comment': _ty.NotRequired[str], 
})
CreateIscsiPortalCreate = _ty.TypedDict('CreateIscsiPortalCreate', {
    'listen': _jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'listen': _jsonschema.JsonArray,
    'tag': int,
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
    'listen': _jsonschema.JsonArray,
    'tag': int,
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
QueryIscsiPortalQueryResultItem = _ty.TypedDict('QueryIscsiPortalQueryResultItem', {
    'id': _ty.NotRequired[int],
    'listen': _ty.NotRequired[_jsonschema.JsonArray],
    'tag': _ty.NotRequired[int],
    'comment': _ty.NotRequired[str], 
})
UpdateIscsiPortalUpdate = _ty.TypedDict('UpdateIscsiPortalUpdate', {
    'listen': _ty.NotRequired[_jsonschema.JsonArray],
    'comment': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'listen': _jsonschema.JsonArray,
    'tag': int,
    'comment': _ty.NotRequired[str], 
})