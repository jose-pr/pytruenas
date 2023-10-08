
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Ssh(Namespace):
    _namespace:_ty.Literal['ssh']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def bindiface_choices(self, 
    /) -> 'dict[str]': 
        """
        Available choices for the bindiface attribute of SSH service.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            ssh_bind_interfaces_choices
        """
        ...
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            ssh_entry
        """
        ...
    @_ty.overload
    def update(self, 
        ssh_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update settings of SSH daemon service.
        
        If `bindiface` is empty it will listen for all available addresses.

        Parameters
        ----------
        ssh_update:
            ssh_update
        Returns
        -------
        dict[str]:
            ssh_update_returns
        """
        ...
