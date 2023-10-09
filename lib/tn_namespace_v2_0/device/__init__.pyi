
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Device(
    Namespace
    ):
    _namespace:typing.Literal['device']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def get_info(self, 
        type:'Type',
    /) -> 'typing.Union[list[SerialInfo], list[GpuInfo], dict[str]]': 
        """
        Get info for SERIAL/DISK/GPU device types.

        Parameters
        ----------
        type:
            type
        Returns
        -------
        typing.Union[list[SerialInfo], list[GpuInfo], dict[str]]:
            
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
    class Type(str,Enum):
        SERIAL = 'SERIAL'
        DISK = 'DISK'
        GPU = 'GPU'
        ...
    SerialInfo = typing.TypedDict('SerialInfo', {
            'name':'str',
            'location':'str',
            'drivername':'str',
            'start':'str',
            'size':'int',
            'description':'str',
    })
    Addr = typing.TypedDict('Addr', {
            'pci_slot':'str',
            'domain':'str',
            'bus':'str',
            'slot':'str',
    })
    GpuDevice = typing.TypedDict('GpuDevice', {
            'pci_id':'str',
            'pci_slot':'str',
            'vm_pci_slot':'str',
    })
    GpuInfo = typing.TypedDict('GpuInfo', {
            'addr':'Addr',
            'description':'str',
            'devices':'list[GpuDevice]',
            'vendor':'typing.Optional[str]',
            'available_to_host':'bool',
            'uses_system_critical_devices':'bool',
    })
