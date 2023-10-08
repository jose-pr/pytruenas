
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class InterfaceCapabilities(Namespace):
    _namespace:_ty.Literal['interface.capabilities']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def get(self, 
        name:'str',
    /) -> 'dict[str]': 
        """
        Return enabled, disabled and supported capabilities (also known as features)
        on a given interface.
        
        `name` String representing name of the interface

        Parameters
        ----------
        name:
            name
        Returns
        -------
        dict[str]:
            capabilties
        """
        ...
    @_ty.overload
    def set(self, 
        capabilities_set:'dict[str]'={},
    /) -> 'list': 
        """
        Enable or Disable capabilties (also known as features) on a given interface.
        
        `name` String representing name of the interface
        `capabilities` List representing capabilities to be acted upon
        `action` String when set to 'ENABLE' will enable `capabilities` else if set
                    to `DISABLE` will disable `capabilities`.

        Parameters
        ----------
        capabilities_set:
            capabilities_set
        Returns
        -------
        list:
            capabilities
        """
        ...
