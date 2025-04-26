from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Reboot(_NS):
    
    def info(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> InfoReturn:
        """"""
        ...
InfoReturn = _ty.TypedDict('InfoReturn', {
    'boot_id': str,
    'reboot_required_reasons': _jsonschema.JsonArray, 
})