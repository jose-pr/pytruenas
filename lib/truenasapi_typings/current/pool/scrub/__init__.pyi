from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Scrub(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[Data],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:_jsonschema.JsonValue=None,
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
        """Create a scrub task for a pool.

`threshold` refers to the minimum amount of time in days has to be passed before a scrub can run again."""
        ...
    def delete(self,
        id_:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete scrub task of `id`."""
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
    ) -> list[QueryPoolScrubQueryResultItem]|QueryPoolScrubQueryResultItem|int:
        """"""
        ...
    def run(self,
        name:str,
        threshold:int=35,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Initiate a scrub of a pool `name` if last scrub was performed more than `threshold` days before."""
        ...
    def scrub(self,
        name:str,
        action:str=START,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Start/Stop/Pause a scrub on pool `name`."""
        ...
    def update(self,
        id_:int,
        data:UpdateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update scrub task of `id`."""
        ...
Data = _ty.TypedDict('Data', {
    'pool': _ty.NotRequired[int],
    'threshold': _ty.NotRequired[int],
    'description': _ty.NotRequired[str],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'enabled': _ty.NotRequired[bool], 
})
CreateData = _ty.TypedDict('CreateData', {
    'pool': int,
    'threshold': _ty.NotRequired[int],
    'description': _ty.NotRequired[str],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'enabled': _ty.NotRequired[bool], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'pool': int,
    'threshold': _ty.NotRequired[int],
    'description': _ty.NotRequired[str],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'enabled': _ty.NotRequired[bool],
    'id': int,
    'pool_name': str, 
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
    'pool': int,
    'threshold': _ty.NotRequired[int],
    'description': _ty.NotRequired[str],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'enabled': _ty.NotRequired[bool],
    'id': int,
    'pool_name': str, 
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
QueryPoolScrubQueryResultItem = _ty.TypedDict('QueryPoolScrubQueryResultItem', {
    'pool': _ty.NotRequired[int],
    'threshold': _ty.NotRequired[int],
    'description': _ty.NotRequired[str],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'enabled': _ty.NotRequired[bool],
    'id': _ty.NotRequired[int],
    'pool_name': _ty.NotRequired[str], 
})
UpdateData = _ty.TypedDict('UpdateData', {
    'pool': _ty.NotRequired[int],
    'threshold': _ty.NotRequired[int],
    'description': _ty.NotRequired[str],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'enabled': _ty.NotRequired[bool], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'pool': int,
    'threshold': _ty.NotRequired[int],
    'description': _ty.NotRequired[str],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'enabled': _ty.NotRequired[bool],
    'id': int,
    'pool_name': str, 
})