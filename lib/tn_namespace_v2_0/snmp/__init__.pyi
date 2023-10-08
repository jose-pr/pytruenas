
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Snmp(Namespace):
    _namespace:_ty.Literal['snmp']
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
            snmp_entry
        """
        ...
    @_ty.overload
    def update(self, 
        snmp_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update SNMP Service Configuration.
        
        `v3` when set enables SNMP version 3.
        
        `v3_username`, `v3_authtype`, `v3_password`, `v3_privproto` and `v3_privpassphrase` are only used when `v3`
        is enabled.

        Parameters
        ----------
        snmp_update:
            snmp_update
        Returns
        -------
        dict[str]:
            snmp_update_returns
        """
        ...
