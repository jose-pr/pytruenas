from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Staticroute(_NS):
    
    def create(self,
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> StaticrouteCreate:
        """Create a Static Route.

Address families of `gateway` and `destination` should match when creating a static route.

`description` is an optional attribute for any notes regarding the static route."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete Static Route of `id`."""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> StaticrouteGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[StaticRouteQueryResultItem]|StaticRouteQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> StaticrouteUpdate:
        """Update Static Route of `id`."""
        ...
data = _ty.TypedDict('data', {
    'destination': _ty.NotRequired[str],
    'gateway': _ty.NotRequired[str],
    'description': _ty.NotRequired[str], 
})
StaticrouteCreate = _ty.TypedDict('StaticrouteCreate', {
    'destination': str,
    'gateway': str,
    'description': _ty.NotRequired[str],
    'id': int, 
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
StaticrouteGet_instance = _ty.TypedDict('StaticrouteGet_instance', {
    'destination': str,
    'gateway': str,
    'description': _ty.NotRequired[str],
    'id': int, 
})
StaticRouteQueryResultItem = _ty.TypedDict('StaticRouteQueryResultItem', {
    'destination': _ty.NotRequired[str],
    'gateway': _ty.NotRequired[str],
    'description': _ty.NotRequired[str],
    'id': _ty.NotRequired[int], 
})
StaticrouteUpdate = _ty.TypedDict('StaticrouteUpdate', {
    'destination': str,
    'gateway': str,
    'description': _ty.NotRequired[str],
    'id': int, 
})