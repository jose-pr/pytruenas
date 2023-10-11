
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class VmDevice(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['vm.device']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def bind_choices(self, 
    /) -> 'dict[str]': 
        """
        Available choices for Bind attribute.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            bind_choices
        """
        ...
    @typing.overload
    def create(self, 
        vmdevice_create:'VmdeviceCreate',
    /) -> 'VmDeviceCreateReturns': 
        """
        Create a new device for the VM of id `vm`.
        
        If `dtype` is the `RAW` type and a new raw file is to be created, `attributes.exists` will be passed as false.
        This means the API handles creating the raw file and raises the appropriate exception if file creation fails.
        
        If `dtype` is of `DISK` type and a new Zvol is to be created, `attributes.create_zvol` will be passed as
        true with valid `attributes.zvol_name` and `attributes.zvol_volsize` values.

        Parameters
        ----------
        vmdevice_create:
            vmdevice_create
        Returns
        -------
        VmDeviceCreateReturns:
            vm_device_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
        vm_device_delete:'VmDeviceDelete',
    /) -> 'bool': 
        """
        Delete a VM device of `id`.

        Parameters
        ----------
        id:
            id
        vm_device_delete:
            vm_device_delete
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def disk_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns disk choices for device type "DISK".

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "vms/test 1": "/dev/zvol/vms/test+1"
            }
            ```
        """
        ...
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance',
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @typing.overload
    def iommu_enabled(self, 
    /) -> 'bool': 
        """
        Returns "true" if iommu is enabled, "false" otherwise

        Parameters
        ----------
        Returns
        -------
        bool:
            iommu_enabled
        """
        ...
    @typing.overload
    def iotype_choices(self, 
    /) -> 'IotypeChoices': 
        """
        IO-type choices for storage devices.

        Parameters
        ----------
        Returns
        -------
        IotypeChoices:
            iotype_choices
        """
        ...
    @typing.overload
    def nic_attach_choices(self, 
    /) -> 'dict[str]': 
        """
        Available choices for NIC Attach attribute.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            nic_attach_choices
        """
        ...
    @typing.overload
    def passthrough_device(self, 
        device:'str',
    /) -> 'PassthroughDevice': 
        """
        Retrieve details about `device` PCI device

        Parameters
        ----------
        device:
            device
        Returns
        -------
        PassthroughDevice:
            passthrough_device
        """
        ...
    @typing.overload
    def passthrough_device_choices(self, 
    /) -> 'list[PassthroughDevice]': 
        """
        Available choices for PCI passthru devices

        Parameters
        ----------
        Returns
        -------
        list[PassthroughDevice]:
            passthrough_device_choices
        """
        ...
    @typing.overload
    def pptdev_choices(self, 
    /) -> 'list[PassthroughDevice]': 
        """
        Available choices for PCI passthru device

        Parameters
        ----------
        Returns
        -------
        list[PassthroughDevice]:
            passthrough_device_choices
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]',
        query_options:'QueryOptions',
    /) -> 'typing.Union[list[VmDeviceEntry], VmDeviceEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[VmDeviceEntry], VmDeviceEntry, int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        vm_device_update:'VmDeviceUpdate',
    /) -> 'VmDeviceUpdateReturns': 
        """
        Update a VM device of `id`.
        
        Pass `attributes.size` to resize a `dtype` `RAW` device. The raw file will be resized.

        Parameters
        ----------
        id:
            Update a VM device of `id`.
        vm_device_update:
            vm_device_update
        Returns
        -------
        VmDeviceUpdateReturns:
            vm_device_update_returns
        """
        ...
    @typing.overload
    def usb_controller_choices(self, 
    /) -> 'UsbControllerChoices': 
        """
        Retrieve USB controller type choices

        Parameters
        ----------
        Returns
        -------
        UsbControllerChoices:
            usb_controller_choices
        """
        ...
    @typing.overload
    def usb_passthrough_choices(self, 
    /) -> 'list[UsbPassthroughDevice]': 
        """
        Available choices for USB passthrough devices.

        Parameters
        ----------
        Returns
        -------
        list[UsbPassthroughDevice]:
            usb_passthrough_choices
        """
        ...
    @typing.overload
    def usb_passthrough_device(self, 
        device:'str',
    /) -> 'UsbPassthroughDevice': 
        """
        Retrieve details about `device` USB device.

        Parameters
        ----------
        device:
            device
        Returns
        -------
        UsbPassthroughDevice:
            usb_passthrough_device
        """
        ...
    VmdeviceCreate = typing.TypedDict('VmdeviceCreate', {
            'dtype':'Dtype',
            'vm':'int',
            'attributes':'dict[str]',
            'order':'typing.Optional[int]',
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
            'NATIVE':'NATIVE',
            'THREADS':'THREADS',
            'IO_URING':'IOURING',
    })
    class NATIVE(str,Enum):
        NATIVE = 'NATIVE'
        ...
    class THREADS(str,Enum):
        THREADS = 'THREADS'
        ...
    class IOURING(str,Enum):
        IOURING = 'IO_URING'
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
    Capability = typing.TypedDict('Capability', {
            'class':'typing.Optional[str]',
            'domain':'typing.Optional[str]',
            'bus':'typing.Optional[str]',
            'slot':'typing.Optional[str]',
            'function':'typing.Optional[str]',
            'product':'typing.Optional[str]',
            'vendor':'typing.Optional[str]',
    })
    IommuGroup = typing.TypedDict('IommuGroup', {
            'number':'int',
            'addresses':'list[Address]',
    })
    Address = typing.TypedDict('Address', {
            'domain':'str',
            'bus':'str',
            'slot':'str',
            'function':'str',
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
    class Piix3Uhci(str,Enum):
        Piix3Uhci = 'piix3-uhci'
        ...
    class Piix4Uhci(str,Enum):
        Piix4Uhci = 'piix4-uhci'
        ...
    class Ehci(str,Enum):
        Ehci = 'ehci'
        ...
    class Ich9Ehci1(str,Enum):
        Ich9Ehci1 = 'ich9-ehci1'
        ...
    class Vt82c686bUhci(str,Enum):
        Vt82c686bUhci = 'vt82c686b-uhci'
        ...
    class PciOhci(str,Enum):
        PciOhci = 'pci-ohci'
        ...
    class NecXhci(str,Enum):
        NecXhci = 'nec-xhci'
        ...
    class QemuXhci(str,Enum):
        QemuXhci = 'qemu-xhci'
        ...
    UsbPassthroughDevice = typing.TypedDict('UsbPassthroughDevice', {
            'capability':'Capability_',
            'available':'bool',
            'error':'typing.Optional[str]',
    })
    Capability_ = typing.TypedDict('Capability_', {
            'product':'typing.Optional[str]',
            'product_id':'typing.Optional[str]',
            'vendor':'typing.Optional[str]',
            'vendor_id':'typing.Optional[str]',
            'bus':'typing.Optional[str]',
            'device':'typing.Optional[str]',
    })
