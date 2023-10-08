
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Ups(Namespace):
    _namespace:_ty.Literal['ups']
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
            ups_entry
        """
        ...
    @_ty.overload
    def driver_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns choices of UPS drivers supported by the system.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "blazer_ser$CPM-800": "WinPower ups 2 CPM-800 (blazer_ser)"
            }
            ```
        """
        ...
    @_ty.overload
    def port_choices(self, 
    /) -> 'list': 
        """
        

        Parameters
        ----------
        Returns
        -------
        list:
            port_choices
        """
        ...
    @_ty.overload
    def update(self, 
        ups_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update UPS Service Configuration.
        
        `powerdown` when enabled, sets UPS to power off after shutting down the system.
        
        `nocommwarntime` is a value in seconds which makes UPS Service wait the specified seconds before alerting that
        the Service cannot reach configured UPS.
        
        `shutdowntimer` is a value in seconds which tells the Service to wait specified seconds for the UPS before
        initiating a shutdown. This only applies when `shutdown` is set to "BATT".
        
        `shutdowncmd` is the command which is executed to initiate a shutdown. It defaults to "poweroff".

        Parameters
        ----------
        ups_update:
            ups_update
        Returns
        -------
        dict[str]:
            ups_update_returns
        """
        ...
