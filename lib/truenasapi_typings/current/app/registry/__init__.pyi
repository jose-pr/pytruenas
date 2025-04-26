from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class AppRegistry(_NS):
    
    def create(self,
        app_registry_create:app_registry_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRegistryCreate:
        """Create an app registry entry."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Delete an app registry entry."""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRegistryGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AppRegistryQueryResultItem]|AppRegistryQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRegistryUpdate:
        """Update an app registry entry."""
        ...
app_registry_create = _ty.TypedDict('app_registry_create', {
    'name': str,
    'description': _ty.NotRequired[str|None],
    'username': str,
    'password': str,
    'uri': _ty.NotRequired[str], 
})
AppRegistryCreate = _ty.TypedDict('AppRegistryCreate', {
    'id': int,
    'name': str,
    'description': _ty.NotRequired[str|None],
    'username': str,
    'password': str,
    'uri': str, 
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
AppRegistryGet_instance = _ty.TypedDict('AppRegistryGet_instance', {
    'id': int,
    'name': str,
    'description': _ty.NotRequired[str|None],
    'username': str,
    'password': str,
    'uri': str, 
})
AppRegistryQueryResultItem = _ty.TypedDict('AppRegistryQueryResultItem', {
    'id': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'description': _ty.NotRequired[str|None],
    'username': _ty.NotRequired[str],
    'password': _ty.NotRequired[str],
    'uri': _ty.NotRequired[str], 
})
data = _ty.TypedDict('data', {
    'name': _ty.NotRequired[str],
    'description': _ty.NotRequired[str|None],
    'username': _ty.NotRequired[str],
    'password': _ty.NotRequired[str],
    'uri': _ty.NotRequired[str], 
})
AppRegistryUpdate = _ty.TypedDict('AppRegistryUpdate', {
    'id': int,
    'name': str,
    'description': _ty.NotRequired[str|None],
    'username': str,
    'password': str,
    'uri': str, 
})