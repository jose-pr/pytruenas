
from pytruenas import Namespace, TrueNASClient
import typing
class SystemSecurity(Namespace):
    _namespace:typing.Literal['system.security']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'SystemSecurityEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        SystemSecurityEntry:
            system_security_entry
        """
        ...
    @typing.overload
    def update(self, 
        system_security_update:'SystemSecurityUpdate'={},
    /) -> 'SystemSecurityUpdateReturns': 
        """
        Update System Security Service Configuration.
        
        `enable_fips` when set, enables FIPS mode.

        Parameters
        ----------
        system_security_update:
            system_security_update
        Returns
        -------
        SystemSecurityUpdateReturns:
            system_security_update_returns
        """
        ...

class SystemSecurityEntry(typing.TypedDict):
        enable_fips:'bool'
        id:'int'
        ...
class SystemSecurityUpdate(typing.TypedDict):
        enable_fips:'bool'
        ...
class SystemSecurityUpdateReturns(typing.TypedDict):
        enable_fips:'bool'
        id:'int'
        ...
