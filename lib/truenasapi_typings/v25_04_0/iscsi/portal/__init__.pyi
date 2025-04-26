from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class IscsiPortal(_NS):
    
    def create(self,
        iscsi_portal_create:iscsi_portal_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiPortalCreate:
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
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiPortalGet_instance:
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
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[IscsiPortalQueryResultItem]|IscsiPortalQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        iscsi_portal_update:iscsi_portal_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiPortalUpdate:
        """Update iSCSI Portal `id`."""
        ...
iscsi_portal_create = _ty.TypedDict('iscsi_portal_create', {
    'listen': _jsonschema.JsonArray,
    'comment': _ty.NotRequired[str], 
})
IscsiPortalCreate = _ty.TypedDict('IscsiPortalCreate', {
    'id': int,
    'listen': _jsonschema.JsonArray,
    'tag': int,
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
IscsiPortalGet_instance = _ty.TypedDict('IscsiPortalGet_instance', {
    'id': int,
    'listen': _jsonschema.JsonArray,
    'tag': int,
    'comment': _ty.NotRequired[str], 
})
IscsiPortalQueryResultItem = _ty.TypedDict('IscsiPortalQueryResultItem', {
    'id': _ty.NotRequired[int],
    'listen': _ty.NotRequired[_jsonschema.JsonArray],
    'tag': _ty.NotRequired[int],
    'comment': _ty.NotRequired[str], 
})
iscsi_portal_update = _ty.TypedDict('iscsi_portal_update', {
    'listen': _ty.NotRequired[_jsonschema.JsonArray],
    'comment': _ty.NotRequired[str], 
})
IscsiPortalUpdate = _ty.TypedDict('IscsiPortalUpdate', {
    'id': int,
    'listen': _jsonschema.JsonArray,
    'tag': int,
    'comment': _ty.NotRequired[str], 
})