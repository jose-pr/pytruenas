
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class SystemSecurity(Namespace):
    _namespace:_ty.Literal['system.security']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            system_security_entry
        """
        ...
    @_ty.overload
    def update(self, 
        system_security_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update System Security Service Configuration.
        
        `enable_fips` when set, enables FIPS mode.

        Parameters
        ----------
        system_security_update:
            system_security_update
        Returns
        -------
        dict[str]:
            system_security_update_returns
        """
        ...
