
from pytruenas import Namespace, TrueNASClient
import typing
class Device(Namespace):
    _namespace:typing.Literal['device']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def get_info(self, 
        type:'str',
    /) -> 'list[SerialInfo]|list[GpuInfo]|dict[str]': 
        """
        Get info for SERIAL/DISK/GPU device types.

        Parameters
        ----------
        type:
            type
        Returns
        -------
        list[SerialInfo]:
            
        list[GpuInfo]:
            
        dict[str]:
            
        """
        ...
    @typing.overload
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

class SerialInfo(typing.TypedDict):
        name:'str'
        location:'str'
        drivername:'str'
        start:'str'
        size:'int'
        description:'str'
        ...
class GpuInfo(typing.TypedDict):
        addr:'Addr'
        description:'str'
        devices:'list[GpuDevice]'
        vendor:'typing.Optional[str]'
        available_to_host:'bool'
        uses_system_critical_devices:'bool'
        ...
class Addr(typing.TypedDict):
        pci_slot:'str'
        domain:'str'
        bus:'str'
        slot:'str'
        ...
class GpuDevice(typing.TypedDict):
        pci_id:'str'
        pci_slot:'str'
        vm_pci_slot:'str'
        ...
