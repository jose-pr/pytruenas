from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class FailoverReboot(_NS):
    
    def info(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> FailoverRebootInfo:
        """"""
        ...
    def other_node(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Reboot the other node and wait for it to come back online.

NOTE: This makes very few checks on HA systems. You need to know what you're doing before calling this."""
        ...
FailoverRebootInfo = _ty.TypedDict('FailoverRebootInfo', {
    'this_node': _jsonschema.JsonValue,
    'other_node': _jsonschema.JsonValue|None, 
})