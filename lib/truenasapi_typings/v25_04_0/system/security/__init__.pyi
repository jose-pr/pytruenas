from pytruenas import Namespace as _NS
from .info import SystemSecurityInfo 
class SystemSecurity(_NS):
    
    def config(
    ) -> SystemSecurityConfig:
        """"""
        ...
    def update(
        system_security_update,
    ) -> SystemSecurityUpdate:
        """Update System Security Service Configuration.

`enable_fips` when set, enables FIPS mode. `enable_gpos_stig` when set, enables compatibility with the General Purpose Operating System STIG."""
        ...
    info: SystemSecurityInfo
class SystemSecurityConfig:
    ...
class SystemSecurityUpdate:
    ... 