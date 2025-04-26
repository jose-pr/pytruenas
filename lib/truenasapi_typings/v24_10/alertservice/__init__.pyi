from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Alertservice(_NS):
    
    def create(self,
        alert_service_create:alert_service_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertserviceCreate:
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
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertserviceGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AlertServiceQueryResultItem]|AlertServiceQueryResultItem|int:
        """"""
        ...
    def test(self,
        alert_service_create:alert_service_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Send a test alert using `type` of Alert Service."""
        ...
    def update(self,
        id:int,
        alert_service_update:alert_service_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertserviceUpdate:
        """Update Alert Service of `id`."""
        ...
alert_service_create = _ty.TypedDict('alert_service_create', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool], 
})
AlertserviceCreate = _ty.TypedDict('AlertserviceCreate', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool],
    'id': int,
    'type__title': str, 
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
AlertserviceGet_instance = _ty.TypedDict('AlertserviceGet_instance', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool],
    'id': int,
    'type__title': str, 
})
AlertServiceQueryResultItem = _ty.TypedDict('AlertServiceQueryResultItem', {
    'name': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'attributes': _ty.NotRequired[_jsonschema.JsonObject],
    'level': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'id': _ty.NotRequired[int],
    'type__title': _ty.NotRequired[str], 
})
alert_service_update = _ty.TypedDict('alert_service_update', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool], 
})
AlertserviceUpdate = _ty.TypedDict('AlertserviceUpdate', {
    'name': str,
    'type': str,
    'attributes': _jsonschema.JsonObject,
    'level': str,
    'enabled': _ty.NotRequired[bool],
    'id': int,
    'type__title': str, 
})