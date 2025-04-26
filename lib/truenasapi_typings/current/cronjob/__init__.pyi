from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Cronjob(_NS):
    
    def create(self,
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CronjobCreate:
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
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CronjobGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[CronJobQueryResultItem]|CronJobQueryResultItem|int:
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
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CronjobUpdate:
        """Update cronjob of `id`."""
        ...
data = _ty.TypedDict('data', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': _ty.NotRequired[str],
    'description': _ty.NotRequired[str],
    'user': _ty.NotRequired[str], 
})
CronjobCreate = _ty.TypedDict('CronjobCreate', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': str,
    'description': _ty.NotRequired[str],
    'user': str,
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
CronjobGet_instance = _ty.TypedDict('CronjobGet_instance', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': str,
    'description': _ty.NotRequired[str],
    'user': str,
    'id': int, 
})
CronJobQueryResultItem = _ty.TypedDict('CronJobQueryResultItem', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': _ty.NotRequired[str],
    'description': _ty.NotRequired[str],
    'user': _ty.NotRequired[str],
    'id': _ty.NotRequired[int], 
})
CronjobUpdate = _ty.TypedDict('CronjobUpdate', {
    'enabled': _ty.NotRequired[bool],
    'stderr': _ty.NotRequired[bool],
    'stdout': _ty.NotRequired[bool],
    'schedule': _ty.NotRequired[_jsonschema.JsonValue],
    'command': str,
    'description': _ty.NotRequired[str],
    'user': str,
    'id': int, 
})