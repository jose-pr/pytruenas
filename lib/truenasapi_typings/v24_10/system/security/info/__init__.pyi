from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class SystemSecurityInfo(_NS):
    
    def fips_available(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Returns a boolean identifying whether or not FIPS mode may be toggled on this system"""
        ...
    def fips_enabled(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Returns a boolean identifying whether or not FIPS mode has been enabled on this system"""
        ...