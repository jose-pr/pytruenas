
from pytruenas import Namespace, TrueNASClient
import typing
class VmDevice(Namespace):
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
        vmdevice_create:'VmdeviceCreate'={},
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
        vm_device_delete:'VmDeviceDelete'={},
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
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'QueryOptionsGetInstance'={},
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
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[VmDeviceEntry]|VmDeviceEntry|int|VmDeviceEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[VmDeviceEntry]:
            
        VmDeviceEntry:
            
        int:
            
        VmDeviceEntry:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        vm_device_update:'VmDeviceUpdate'={},
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

class VmdeviceCreate(typing.TypedDict):
        dtype:'str'
        vm:'int'
        attributes:'dict[str]'
        order:'typing.Optional[int]'
        ...
class VmDeviceCreateReturns(typing.TypedDict):
        dtype:'str'
        vm:'int'
        attributes:'dict[str]'
        order:'typing.Optional[int]'
        id:'int'
        ...
class VmDeviceDelete(typing.TypedDict):
        zvol:'bool'
        raw_file:'bool'
        force:'bool'
        ...
class QueryOptionsGetInstance(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class IotypeChoices(typing.TypedDict):
        NATIVE:'str'
        THREADS:'str'
        IO_URING:'str'
        ...
class PassthroughDevice(typing.TypedDict):
        capability:'Capability'
        controller_type:'typing.Optional[str]'
        iommu_group:'IommuGroup'
        available:'bool'
        drivers:'list[str]'
        error:'typing.Optional[str]'
        device_path:'typing.Optional[str]'
        reset_mechanism_defined:'bool'
        description:'str'
        ...
class Capability(typing.TypedDict):
        class:'typing.Optional[str]'
        domain:'typing.Optional[str]'
        bus:'typing.Optional[str]'
        slot:'typing.Optional[str]'
        function:'typing.Optional[str]'
        product:'typing.Optional[str]'
        vendor:'typing.Optional[str]'
        ...
class IommuGroup(typing.TypedDict):
        number:'int'
        addresses:'list[Address]'
        ...
class Address(typing.TypedDict):
        domain:'str'
        bus:'str'
        slot:'str'
        function:'str'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class VmDeviceEntry(typing.TypedDict):
        dtype:'str'
        vm:'int'
        attributes:'dict[str]'
        order:'typing.Optional[int]'
        id:'int'
        ...
class VmDeviceUpdate(typing.TypedDict):
        dtype:'str'
        vm:'int'
        attributes:'dict[str]'
        order:'typing.Optional[int]'
        ...
class VmDeviceUpdateReturns(typing.TypedDict):
        dtype:'str'
        vm:'int'
        attributes:'dict[str]'
        order:'typing.Optional[int]'
        id:'int'
        ...
class UsbControllerChoices(typing.TypedDict):
        piix3-uhci:'str'
        piix4-uhci:'str'
        ehci:'str'
        ich9-ehci1:'str'
        vt82c686b-uhci:'str'
        pci-ohci:'str'
        nec-xhci:'str'
        qemu-xhci:'str'
        ...
class UsbPassthroughDevice(typing.TypedDict):
        capability:'Capability'
        available:'bool'
        error:'typing.Optional[str]'
        ...
class Capability_(typing.TypedDict):
        product:'typing.Optional[str]'
        product_id:'typing.Optional[str]'
        vendor:'typing.Optional[str]'
        vendor_id:'typing.Optional[str]'
        bus:'typing.Optional[str]'
        device:'typing.Optional[str]'
        ...
