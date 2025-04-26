from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class SystemReboot(_NS):
    
    def info(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemRebootInfo:
        """"""
        ...
SystemRebootInfo = _ty.TypedDict('SystemRebootInfo', {
    'boot_id': str,
    'reboot_required_reasons': _jsonschema.JsonArray, 
})