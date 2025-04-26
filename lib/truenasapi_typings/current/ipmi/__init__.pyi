from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Ipmi(_NS):
    
    def is_loaded(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Returns a boolean value indicating if /dev/ipmi0 is loaded."""
        ...