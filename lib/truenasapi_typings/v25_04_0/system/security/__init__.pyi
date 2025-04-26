from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .info import Info 
class Security(_NS):
    
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ConfigReturn:
        """"""
        ...
    def update(self,
        system_security_update:UpdateSystemSecurityUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update System Security Service Configuration.

`enable_fips` when set, enables FIPS mode. `enable_gpos_stig` when set, enables compatibility with the General Purpose Operating System STIG."""
        ...
    info: Info
ConfigReturn = _ty.TypedDict('ConfigReturn', {
    'id': int,
    'enable_fips': bool,
    'enable_gpos_stig': bool, 
})
UpdateSystemSecurityUpdate = _ty.TypedDict('UpdateSystemSecurityUpdate', {
    'enable_fips': _ty.NotRequired[bool],
    'enable_gpos_stig': _ty.NotRequired[bool], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'enable_fips': bool,
    'enable_gpos_stig': bool, 
})