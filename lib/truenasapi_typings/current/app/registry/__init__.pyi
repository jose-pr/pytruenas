from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Registry(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[AppRegistryCreate],
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
        app_registry_create:CreateAppRegistryCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
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
    ) -> list[QueryAppRegistryQueryResultItem]|QueryAppRegistryQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        data:UpdateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update an app registry entry."""
        ...
AppRegistryCreate = _ty.TypedDict('AppRegistryCreate', {
    'name': str,
    'description': _ty.NotRequired[str|None],
    'username': str,
    'password': str,
    'uri': _ty.NotRequired[str], 
})
Data = _ty.TypedDict('Data', {
    'name': _ty.NotRequired[str],
    'description': _ty.NotRequired[str|None],
    'username': _ty.NotRequired[str],
    'password': _ty.NotRequired[str],
    'uri': _ty.NotRequired[str], 
})
CreateAppRegistryCreate = _ty.TypedDict('CreateAppRegistryCreate', {
    'name': str,
    'description': _ty.NotRequired[str|None],
    'username': str,
    'password': str,
    'uri': _ty.NotRequired[str], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'name': str,
    'description': _ty.NotRequired[str|None],
    'username': str,
    'password': str,
    'uri': str, 
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
    'name': str,
    'description': _ty.NotRequired[str|None],
    'username': str,
    'password': str,
    'uri': str, 
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
QueryAppRegistryQueryResultItem = _ty.TypedDict('QueryAppRegistryQueryResultItem', {
    'id': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'description': _ty.NotRequired[str|None],
    'username': _ty.NotRequired[str],
    'password': _ty.NotRequired[str],
    'uri': _ty.NotRequired[str], 
})
UpdateData = _ty.TypedDict('UpdateData', {
    'name': _ty.NotRequired[str],
    'description': _ty.NotRequired[str|None],
    'username': _ty.NotRequired[str],
    'password': _ty.NotRequired[str],
    'uri': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'name': str,
    'description': _ty.NotRequired[str|None],
    'username': str,
    'password': str,
    'uri': str, 
})