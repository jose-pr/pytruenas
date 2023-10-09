
from pytruenas.base import Namespace

import typing
from enum import Enum

class Device(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'device')

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
