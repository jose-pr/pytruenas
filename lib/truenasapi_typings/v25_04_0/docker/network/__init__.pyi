from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class DockerNetwork(_NS):
    
    def get_instance(self,
        id:str|None,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerNetworkGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[DockerNetworkQueryResultItem]|DockerNetworkQueryResultItem|int:
        """Query all docker networks"""
        ...
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
DockerNetworkGet_instance = _ty.TypedDict('DockerNetworkGet_instance', {
    'ipam': _jsonschema.JsonObject|None,
    'labels': _jsonschema.JsonObject|None,
    'created': str|None,
    'driver': str|None,
    'id': str|None,
    'name': str|None,
    'scope': str|None,
    'short_id': str|None, 
})
DockerNetworkQueryResultItem = _ty.TypedDict('DockerNetworkQueryResultItem', {
    'ipam': _ty.NotRequired[_jsonschema.JsonObject|None],
    'labels': _ty.NotRequired[_jsonschema.JsonObject|None],
    'created': _ty.NotRequired[str|None],
    'driver': _ty.NotRequired[str|None],
    'id': _ty.NotRequired[str|None],
    'name': _ty.NotRequired[str|None],
    'scope': _ty.NotRequired[str|None],
    'short_id': _ty.NotRequired[str|None], 
})