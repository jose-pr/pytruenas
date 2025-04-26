from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class BootEnvironment(_NS):
    
    def activate(self,
        boot_environment_activate:boot_environment_activate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> BootEnvironmentActivate:
        """"""
        ...
    def clone(self,
        boot_environment_clone:boot_environment_clone,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> BootEnvironmentClone:
        """"""
        ...
    def destroy(self,
        boot_environment_destroy:boot_environment_destroy,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """"""
        ...
    def keep(self,
        boot_environment_destroy:boot_environment_destroy,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> BootEnvironmentKeep:
        """"""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[BootEnvironmentQueryResultItem]|BootEnvironmentQueryResultItem|int:
        """"""
        ...
boot_environment_activate = _ty.TypedDict('boot_environment_activate', {
    'id': str, 
})
BootEnvironmentActivate = _ty.TypedDict('BootEnvironmentActivate', {
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
boot_environment_clone = _ty.TypedDict('boot_environment_clone', {
    'id': str,
    'target': str, 
})
BootEnvironmentClone = _ty.TypedDict('BootEnvironmentClone', {
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
boot_environment_destroy = _ty.TypedDict('boot_environment_destroy', {
    'id': str,
    'value': bool, 
})
BootEnvironmentKeep = _ty.TypedDict('BootEnvironmentKeep', {
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
BootEnvironmentQueryResultItem = _ty.TypedDict('BootEnvironmentQueryResultItem', {
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