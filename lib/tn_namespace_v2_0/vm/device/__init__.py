
from pytruenas import Namespace
import typing
class VmDevice(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'vm.device')

    VmdeviceCreate = typing.TypedDict('VmdeviceCreate', {
            'dtype':'str',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
    })
    VmDeviceCreateReturns = typing.TypedDict('VmDeviceCreateReturns', {
            'dtype':'str',
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
    IotypeChoices = typing.TypedDict('IotypeChoices', {
            'NATIVE':'str',
            'THREADS':'str',
            'IO_URING':'str',
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
    Address = typing.TypedDict('Address', {
            'domain':'str',
            'bus':'str',
            'slot':'str',
            'function':'str',
    })
    IommuGroup = typing.TypedDict('IommuGroup', {
            'number':'int',
            'addresses':'list[Address]',
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
    Capability_ = typing.TypedDict('Capability_', {
            'class':'typing.Optional[str]',
            'domain':'typing.Optional[str]',
            'bus':'typing.Optional[str]',
            'slot':'typing.Optional[str]',
            'function':'typing.Optional[str]',
            'product':'typing.Optional[str]',
            'vendor':'typing.Optional[str]',
    })
    Address_ = typing.TypedDict('Address_', {
            'domain':'str',
            'bus':'str',
            'slot':'str',
            'function':'str',
    })
    IommuGroup_ = typing.TypedDict('IommuGroup_', {
            'number':'int',
            'addresses':'list[Address_]',
    })
    PassthroughDevice_ = typing.TypedDict('PassthroughDevice_', {
            'capability':'Capability_',
            'controller_type':'typing.Optional[str]',
            'iommu_group':'IommuGroup_',
            'available':'bool',
            'drivers':'list[str]',
            'error':'typing.Optional[str]',
            'device_path':'typing.Optional[str]',
            'reset_mechanism_defined':'bool',
            'description':'str',
    })
    Capability__ = typing.TypedDict('Capability__', {
            'class':'typing.Optional[str]',
            'domain':'typing.Optional[str]',
            'bus':'typing.Optional[str]',
            'slot':'typing.Optional[str]',
            'function':'typing.Optional[str]',
            'product':'typing.Optional[str]',
            'vendor':'typing.Optional[str]',
    })
    Address__ = typing.TypedDict('Address__', {
            'domain':'str',
            'bus':'str',
            'slot':'str',
            'function':'str',
    })
    IommuGroup__ = typing.TypedDict('IommuGroup__', {
            'number':'int',
            'addresses':'list[Address__]',
    })
    PassthroughDevice__ = typing.TypedDict('PassthroughDevice__', {
            'capability':'Capability__',
            'controller_type':'typing.Optional[str]',
            'iommu_group':'IommuGroup__',
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
    VmDeviceEntry = typing.TypedDict('VmDeviceEntry', {
            'dtype':'str',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
            'id':'int',
    })
    VmDeviceEntry_ = typing.TypedDict('VmDeviceEntry_', {
            'dtype':'str',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
            'id':'int',
    })
    VmDeviceEntry__ = typing.TypedDict('VmDeviceEntry__', {
            'dtype':'str',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
            'id':'int',
    })
    VmDeviceUpdate = typing.TypedDict('VmDeviceUpdate', {
            'dtype':'str',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
    })
    VmDeviceUpdateReturns = typing.TypedDict('VmDeviceUpdateReturns', {
            'dtype':'str',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
            'id':'int',
    })
    UsbControllerChoices = typing.TypedDict('UsbControllerChoices', {
            'piix3-uhci':'str',
            'piix4-uhci':'str',
            'ehci':'str',
            'ich9-ehci1':'str',
            'vt82c686b-uhci':'str',
            'pci-ohci':'str',
            'nec-xhci':'str',
            'qemu-xhci':'str',
    })
    Capability___ = typing.TypedDict('Capability___', {
            'product':'typing.Optional[str]',
            'product_id':'typing.Optional[str]',
            'vendor':'typing.Optional[str]',
            'vendor_id':'typing.Optional[str]',
            'bus':'typing.Optional[str]',
            'device':'typing.Optional[str]',
    })
    UsbPassthroughDevice = typing.TypedDict('UsbPassthroughDevice', {
            'capability':'Capability___',
            'available':'bool',
            'error':'typing.Optional[str]',
    })
    Capability____ = typing.TypedDict('Capability____', {
            'product':'typing.Optional[str]',
            'product_id':'typing.Optional[str]',
            'vendor':'typing.Optional[str]',
            'vendor_id':'typing.Optional[str]',
            'bus':'typing.Optional[str]',
            'device':'typing.Optional[str]',
    })
    UsbPassthroughDevice_ = typing.TypedDict('UsbPassthroughDevice_', {
            'capability':'Capability____',
            'available':'bool',
            'error':'typing.Optional[str]',
    })
