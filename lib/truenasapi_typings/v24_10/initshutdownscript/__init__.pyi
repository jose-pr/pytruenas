from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Initshutdownscript(_NS):
    
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
        """Create an initshutdown script task.

`type` indicates if a command or script should be executed at `when`.

There are three choices for `when`:

1) PREINIT - This is early in the boot process before all the services have started 2) POSTINIT - This is late in the boot process when most of the services have started 3) SHUTDOWN - This is on shutdown

`timeout` is an integer value which indicates time in seconds which the system should wait for the execution of script/command. It should be noted that a hard limit for a timeout is configured by the base OS, so when a script/command is set to execute on SHUTDOWN, the hard limit configured by the base OS is changed adding the timeout specified by script/command so it can be ensured that it executes as desired and is not interrupted by the base OS's limit."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete init/shutdown task of `id`."""
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
    ) -> list[QueryInitShutdownScriptQueryResultItem]|QueryInitShutdownScriptQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        data:UpdateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update initshutdown script task of `id`."""
        ...
Data = _ty.TypedDict('Data', {
    'type': _ty.NotRequired[str],
    'command': _ty.NotRequired[str|None],
    'script': _ty.NotRequired[str|None],
    'when': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'timeout': _ty.NotRequired[int],
    'comment': _ty.NotRequired[str], 
})
CreateData = _ty.TypedDict('CreateData', {
    'type': str,
    'command': _ty.NotRequired[str|None],
    'script': _ty.NotRequired[str|None],
    'when': str,
    'enabled': _ty.NotRequired[bool],
    'timeout': _ty.NotRequired[int],
    'comment': _ty.NotRequired[str], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'type': str,
    'command': _ty.NotRequired[str|None],
    'script': _ty.NotRequired[str|None],
    'when': str,
    'enabled': _ty.NotRequired[bool],
    'timeout': _ty.NotRequired[int],
    'comment': _ty.NotRequired[str],
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
    'type': str,
    'command': _ty.NotRequired[str|None],
    'script': _ty.NotRequired[str|None],
    'when': str,
    'enabled': _ty.NotRequired[bool],
    'timeout': _ty.NotRequired[int],
    'comment': _ty.NotRequired[str],
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
QueryInitShutdownScriptQueryResultItem = _ty.TypedDict('QueryInitShutdownScriptQueryResultItem', {
    'type': _ty.NotRequired[str],
    'command': _ty.NotRequired[str|None],
    'script': _ty.NotRequired[str|None],
    'when': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'timeout': _ty.NotRequired[int],
    'comment': _ty.NotRequired[str],
    'id': _ty.NotRequired[int], 
})
UpdateData = _ty.TypedDict('UpdateData', {
    'type': _ty.NotRequired[str],
    'command': _ty.NotRequired[str|None],
    'script': _ty.NotRequired[str|None],
    'when': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'timeout': _ty.NotRequired[int],
    'comment': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'type': str,
    'command': _ty.NotRequired[str|None],
    'script': _ty.NotRequired[str|None],
    'when': str,
    'enabled': _ty.NotRequired[bool],
    'timeout': _ty.NotRequired[int],
    'comment': _ty.NotRequired[str],
    'id': int, 
})