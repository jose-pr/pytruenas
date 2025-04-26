from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Environment(_NS):
    
    def activate(self,
        boot_environment_activate:ActivateBootEnvironmentActivate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ActivateReturn:
        """"""
        ...
    def clone(self,
        boot_environment_clone:CloneBootEnvironmentClone,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloneReturn:
        """"""
        ...
    def destroy(self,
        boot_environment_destroy:DestroyBootEnvironmentDestroy,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """"""
        ...
    def keep(self,
        boot_environment_destroy:KeepBootEnvironmentDestroy,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> KeepReturn:
        """"""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryBootEnvironmentQueryResultItem]|QueryBootEnvironmentQueryResultItem|int:
        """"""
        ...
ActivateBootEnvironmentActivate = _ty.TypedDict('ActivateBootEnvironmentActivate', {
    'id': str, 
})
ActivateReturn = _ty.TypedDict('ActivateReturn', {
    'id': str,
    'dataset': str,
    'active': bool,
    'activated': bool,
    'created': str,
    'used_bytes': int,
    'used': str,
    'keep': bool,
    'can_activate': bool, 
})
CloneBootEnvironmentClone = _ty.TypedDict('CloneBootEnvironmentClone', {
    'id': str,
    'target': str, 
})
CloneReturn = _ty.TypedDict('CloneReturn', {
    'id': str,
    'dataset': str,
    'active': bool,
    'activated': bool,
    'created': str,
    'used_bytes': int,
    'used': str,
    'keep': bool,
    'can_activate': bool, 
})
DestroyBootEnvironmentDestroy = _ty.TypedDict('DestroyBootEnvironmentDestroy', {
    'id': str, 
})
KeepBootEnvironmentDestroy = _ty.TypedDict('KeepBootEnvironmentDestroy', {
    'id': str,
    'value': bool, 
})
KeepReturn = _ty.TypedDict('KeepReturn', {
    'id': str,
    'dataset': str,
    'active': bool,
    'activated': bool,
    'created': str,
    'used_bytes': int,
    'used': str,
    'keep': bool,
    'can_activate': bool, 
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
QueryBootEnvironmentQueryResultItem = _ty.TypedDict('QueryBootEnvironmentQueryResultItem', {
    'id': _ty.NotRequired[str],
    'dataset': _ty.NotRequired[str],
    'active': _ty.NotRequired[bool],
    'activated': _ty.NotRequired[bool],
    'created': _ty.NotRequired[str],
    'used_bytes': _ty.NotRequired[int],
    'used': _ty.NotRequired[str],
    'keep': _ty.NotRequired[bool],
    'can_activate': _ty.NotRequired[bool], 
})