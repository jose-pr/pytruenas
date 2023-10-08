
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Device(Namespace):
    _namespace:_ty.Literal['device']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def get_info(self, 
        type:'str',
    /) -> 'list|list|dict[str]': 
        """
        Get info for SERIAL/DISK/GPU device types.

        Parameters
        ----------
        type:
            type
        Returns
        -------
        list:
            
        list:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def gpu_pci_ids_choices(self, 
    /) -> 'dict[str]': 
        """
        Retrieve choices for GPU PCI ids located in the system.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Returns PCI id(s) of GPU(s) located in the system
            
            Example(s):
            ```
            {
                "Red Hat, Inc. QXL paravirtual graphic card": "0000:00:02.0"
            }
            ```
        """
        ...
