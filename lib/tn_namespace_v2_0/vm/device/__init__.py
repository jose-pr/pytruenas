
from pytruenas.base import Namespace

import typing
from enum import Enum

class VmDevice(Namespace):
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
    IommuGroup = typing.TypedDict('IommuGroup', {
            'number':'int',
            'addresses':'list[Address]',
    })
    IotypeChoices = typing.TypedDict('IotypeChoices', {
            'NATIVE':'typing.Literal["NATIVE"]',
            'THREADS':'typing.Literal["THREADS"]',
            'IO_URING':'typing.Literal["IO_URING"]',
    })
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
    UsbControllerChoices = typing.TypedDict('UsbControllerChoices', {
            'piix3-uhci':'typing.Literal["piix3-uhci"]',
            'piix4-uhci':'typing.Literal["piix4-uhci"]',
            'ehci':'typing.Literal["ehci"]',
            'ich9-ehci1':'typing.Literal["ich9-ehci1"]',
            'vt82c686b-uhci':'typing.Literal["vt82c686b-uhci"]',
            'pci-ohci':'typing.Literal["pci-ohci"]',
            'nec-xhci':'typing.Literal["nec-xhci"]',
            'qemu-xhci':'typing.Literal["qemu-xhci"]',
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
