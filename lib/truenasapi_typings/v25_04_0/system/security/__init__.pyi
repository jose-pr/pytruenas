from pytruenas import Namespace as _NS
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
        system_security_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemSecurityUpdate:
        """Update System Security Service Configuration.

`enable_fips` when set, enables FIPS mode. `enable_gpos_stig` when set, enables compatibility with the General Purpose Operating System STIG."""
        ...
    info: SystemSecurityInfo
class SystemSecurityConfig(_ty.TypedDict):
    ...
class SystemSecurityUpdate(_ty.TypedDict):
    ... 