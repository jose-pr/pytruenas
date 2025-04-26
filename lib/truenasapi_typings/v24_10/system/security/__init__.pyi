from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .info import SystemSecurityInfo 
class SystemSecurity(_NS):
    
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemSecurityConfig:
        """"""
        ...
    def update(self,
        system_security_update:system_security_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemSecurityUpdate:
        """Update System Security Service Configuration.

`enable_fips` when set, enables FIPS mode. `enable_gpos_stig` when set, enables compatibility with the General Purpose Operating System STIG."""
        ...
    info: SystemSecurityInfo
SystemSecurityConfig = _ty.TypedDict('SystemSecurityConfig', {
    'id': int,
    'enable_fips': bool,
    'enable_gpos_stig': bool, 
})
system_security_update = _ty.TypedDict('system_security_update', {
    'enable_fips': _ty.NotRequired[bool],
    'enable_gpos_stig': _ty.NotRequired[bool], 
})
SystemSecurityUpdate = _ty.TypedDict('SystemSecurityUpdate', {
    'id': int,
    'enable_fips': bool,
    'enable_gpos_stig': bool, 
})