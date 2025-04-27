from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Staticroute(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[Data],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[Data],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[Data],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        data:CreateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
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
    ) -> list[QueryStaticRouteQueryResultItem]|QueryStaticRouteQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        data:UpdateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update Static Route of `id`."""
        ...
Data = _ty.TypedDict('Data', {
    'destination': _ty.NotRequired[str],
    'gateway': _ty.NotRequired[str],
    'description': _ty.NotRequired[str], 
})
CreateData = _ty.TypedDict('CreateData', {
    'destination': str,
    'gateway': str,
    'description': _ty.NotRequired[str], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'destination': str,
    'gateway': str,
    'description': _ty.NotRequired[str],
    'id': int, 
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
    'destination': str,
    'gateway': str,
    'description': _ty.NotRequired[str],
    'id': int, 
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
QueryStaticRouteQueryResultItem = _ty.TypedDict('QueryStaticRouteQueryResultItem', {
    'destination': _ty.NotRequired[str],
    'gateway': _ty.NotRequired[str],
    'description': _ty.NotRequired[str],
    'id': _ty.NotRequired[int], 
})
UpdateData = _ty.TypedDict('UpdateData', {
    'destination': _ty.NotRequired[str],
    'gateway': _ty.NotRequired[str],
    'description': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'destination': str,
    'gateway': str,
    'description': _ty.NotRequired[str],
    'id': int, 
})