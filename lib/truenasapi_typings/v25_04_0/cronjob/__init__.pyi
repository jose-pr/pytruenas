from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Cronjob(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[Data],
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
        """Create a new cron job.

`stderr` and `stdout` are boolean values which if `true`, represent that we would like to suppress standard error / standard output respectively."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete cronjob of `id`."""
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
    ) -> list[QueryCronJobQueryResultItem]|QueryCronJobQueryResultItem|int:
        """"""
        ...
    def run(self,
        id:int,
        skip_disabled:bool=False,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Job to run cronjob task of `id`."""
        ...
    def update(self,
        id:int,
        data:UpdateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update cronjob of `id`."""
        ...
Data = _ty.TypedDict('Data', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': _ty.NotRequired[str],
    'description': _ty.NotRequired[str],
    'user': _ty.NotRequired[str], 
})
Get = _ty.TypedDict('Get', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': _ty.NotRequired[str],
    'description': _ty.NotRequired[str],
    'user': _ty.NotRequired[str],
    'id': _ty.NotRequired[int], 
})
CreateData = _ty.TypedDict('CreateData', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': str,
    'description': _ty.NotRequired[str],
    'user': str, 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': str,
    'description': _ty.NotRequired[str],
    'user': str,
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
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': str,
    'description': _ty.NotRequired[str],
    'user': str,
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
QueryCronJobQueryResultItem = _ty.TypedDict('QueryCronJobQueryResultItem', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': _ty.NotRequired[str],
    'description': _ty.NotRequired[str],
    'user': _ty.NotRequired[str],
    'id': _ty.NotRequired[int], 
})
UpdateData = _ty.TypedDict('UpdateData', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': _ty.NotRequired[str],
    'description': _ty.NotRequired[str],
    'user': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': str,
    'description': _ty.NotRequired[str],
    'user': str,
    'id': int, 
})