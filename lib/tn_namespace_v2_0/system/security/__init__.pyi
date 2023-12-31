
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class SystemSecurity(
    Namespace
    ):
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
        _system_security_update:'SystemSecurityUpdate',
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
    SystemSecurityEntry = typing.TypedDict('SystemSecurityEntry', {
            'enable_fips':'bool',
            'id':'int',
    })
    SystemSecurityUpdate = typing.TypedDict('SystemSecurityUpdate', {
            'enable_fips':'bool',
    })
    SystemSecurityUpdateReturns = typing.TypedDict('SystemSecurityUpdateReturns', {
            'enable_fips':'bool',
            'id':'int',
    })
