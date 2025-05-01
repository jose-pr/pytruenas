from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Alertservice(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[AlertServiceCreate],
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
        **fields:_ty.Unpack[AlertServiceUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[AlertServiceUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        alert_service_create:CreateAlertServiceCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Create an Alert Service of specified `type`.

If `enabled`, it sends alerts to the configured `type` of Alert Service."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete Alert Service of `id`."""
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
    ) -> list[QueryAlertServiceQueryResultItem]|QueryAlertServiceQueryResultItem|int:
        """"""
        ...
    def test(self,
        alert_service_create:TestAlertServiceCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Send a test alert using `type` of Alert Service."""
        ...
    def update(self,
        id:int,
        alert_service_update:UpdateAlertServiceUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update Alert Service of `id`."""
        ...
AlertServiceCreate = _ty.TypedDict('AlertServiceCreate', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool], 
})
Get = _ty.TypedDict('Get', {
    'name': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonObject],
    'level': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'id': _ty.NotRequired[int],
    'type__title': _ty.NotRequired[str], 
})
AlertServiceUpdate = _ty.TypedDict('AlertServiceUpdate', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool], 
})
CreateAlertServiceCreate = _ty.TypedDict('CreateAlertServiceCreate', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool],
    'id': int,
    'type__title': str, 
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
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool],
    'id': int,
    'type__title': str, 
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
QueryAlertServiceQueryResultItem = _ty.TypedDict('QueryAlertServiceQueryResultItem', {
    'name': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonObject],
    'level': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'id': _ty.NotRequired[int],
    'type__title': _ty.NotRequired[str], 
})
TestAlertServiceCreate = _ty.TypedDict('TestAlertServiceCreate', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool], 
})
UpdateAlertServiceUpdate = _ty.TypedDict('UpdateAlertServiceUpdate', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool],
    'id': int,
    'type__title': str, 
})