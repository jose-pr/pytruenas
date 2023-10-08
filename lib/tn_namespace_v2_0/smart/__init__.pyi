
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Smart(Namespace):
    _namespace:_ty.Literal['smart']
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
            smart_entry
        """
        ...
    @_ty.overload
    def update(self, 
        smart_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update SMART Service Configuration.
        
        `interval` is an integer value in minutes which defines how often smartd activates to check if any tests
        are configured to run.
        
        `critical`, `informational` and `difference` are integer values on which alerts for SMART are configured if
        the disks temperature crosses the assigned threshold for each respective attribute. They default to 0 which
        indicates they are disabled.

        Parameters
        ----------
        smart_update:
            smart_update
        Returns
        -------
        dict[str]:
            smart_update_returns
        """
        ...
