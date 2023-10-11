
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class VmDevice(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'vm.device')

    Address = typing.TypedDict('Address', {
            'domain':'str',
            'bus':'str',
            'slot':'str',
            'function':'str',
    })
    Capability = typing.TypedDict('Capability', {
            'class':'typing.Optional[str]',
            'domain':'typing.Optional[str]',
            'bus':'typing.Optional[str]',
            'slot':'typing.Optional[str]',
            'function':'typing.Optional[str]',
            'product':'typing.Optional[str]',
            'vendor':'typing.Optional[str]',
    })
    Capability_ = typing.TypedDict('Capability_', {
            'product':'typing.Optional[str]',
            'product_id':'typing.Optional[str]',
            'vendor':'typing.Optional[str]',
            'vendor_id':'typing.Optional[str]',
            'bus':'typing.Optional[str]',
            'device':'typing.Optional[str]',
    })
    class Dtype(str,Enum):
        NIC = 'NIC'
        DISK = 'DISK'
        CDROM = 'CDROM'
        PCI = 'PCI'
        DISPLAY = 'DISPLAY'
        RAW = 'RAW'
        USB = 'USB'
        ...
    class Ehci(str,Enum):
        Ehci = 'ehci'
        ...
    class IOURING(str,Enum):
        IOURING = 'IO_URING'
        ...
    class Ich9Ehci1(str,Enum):
        Ich9Ehci1 = 'ich9-ehci1'
        ...
    IommuGroup = typing.TypedDict('IommuGroup', {
            'number':'int',
            'addresses':'list[Address]',
    })
    IotypeChoices = typing.TypedDict('IotypeChoices', {
            'NATIVE':'NATIVE',
            'THREADS':'THREADS',
            'IO_URING':'IOURING',
    })
    class NATIVE(str,Enum):
        NATIVE = 'NATIVE'
        ...
    class NecXhci(str,Enum):
        NecXhci = 'nec-xhci'
        ...
    PassthroughDevice = typing.TypedDict('PassthroughDevice', {
            'capability':'Capability',
            'controller_type':'typing.Optional[str]',
            'iommu_group':'IommuGroup',
            'available':'bool',
            'drivers':'list[str]',
            'error':'typing.Optional[str]',
            'device_path':'typing.Optional[str]',
            'reset_mechanism_defined':'bool',
            'description':'str',
    })
    class PciOhci(str,Enum):
        PciOhci = 'pci-ohci'
        ...
    class Piix3Uhci(str,Enum):
        Piix3Uhci = 'piix3-uhci'
        ...
    class Piix4Uhci(str,Enum):
        Piix4Uhci = 'piix4-uhci'
        ...
    class QemuXhci(str,Enum):
        QemuXhci = 'qemu-xhci'
        ...
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    class THREADS(str,Enum):
        THREADS = 'THREADS'
        ...
    UsbControllerChoices = typing.TypedDict('UsbControllerChoices', {
            'piix3-uhci':'Piix3Uhci',
            'piix4-uhci':'Piix4Uhci',
            'ehci':'Ehci',
            'ich9-ehci1':'Ich9Ehci1',
            'vt82c686b-uhci':'Vt82c686bUhci',
            'pci-ohci':'PciOhci',
            'nec-xhci':'NecXhci',
            'qemu-xhci':'QemuXhci',
    })
    UsbPassthroughDevice = typing.TypedDict('UsbPassthroughDevice', {
            'capability':'Capability_',
            'available':'bool',
            'error':'typing.Optional[str]',
    })
    VmDeviceCreateReturns = typing.TypedDict('VmDeviceCreateReturns', {
            'dtype':'Dtype',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
            'id':'int',
    })
    VmDeviceDelete = typing.TypedDict('VmDeviceDelete', {
            'zvol':'bool',
            'raw_file':'bool',
            'force':'bool',
    })
    VmDeviceEntry = typing.TypedDict('VmDeviceEntry', {
            'dtype':'Dtype',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
            'id':'int',
    })
    VmDeviceUpdate = typing.TypedDict('VmDeviceUpdate', {
            'dtype':'Dtype',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
    })
    VmDeviceUpdateReturns = typing.TypedDict('VmDeviceUpdateReturns', {
            'dtype':'Dtype',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
            'id':'int',
    })
    VmdeviceCreate = typing.TypedDict('VmdeviceCreate', {
            'dtype':'Dtype',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
    })
    class Vt82c686bUhci(str,Enum):
        Vt82c686bUhci = 'vt82c686b-uhci'
        ...
