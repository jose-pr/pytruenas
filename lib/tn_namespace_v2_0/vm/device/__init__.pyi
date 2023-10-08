
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class VmDevice(Namespace):
    _namespace:_ty.Literal['vm.device']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
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
    @_ty.overload
    def create(self, 
        vmdevice_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            vm_device_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
        vm_device_delete:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
    def iotype_choices(self, 
    /) -> 'dict[str]': 
        """
        IO-type choices for storage devices.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            iotype_choices
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def passthrough_device(self, 
        device:'str',
    /) -> 'dict[str]': 
        """
        Retrieve details about `device` PCI device

        Parameters
        ----------
        device:
            device
        Returns
        -------
        dict[str]:
            passthrough_device
        """
        ...
    @_ty.overload
    def passthrough_device_choices(self, 
    /) -> 'list': 
        """
        Available choices for PCI passthru devices

        Parameters
        ----------
        Returns
        -------
        list:
            passthrough_device_choices
        """
        ...
    @_ty.overload
    def pptdev_choices(self, 
    /) -> 'list': 
        """
        Available choices for PCI passthru device

        Parameters
        ----------
        Returns
        -------
        list:
            passthrough_device_choices
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        vm_device_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            vm_device_update_returns
        """
        ...
    @_ty.overload
    def usb_controller_choices(self, 
    /) -> 'dict[str]': 
        """
        Retrieve USB controller type choices

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            usb_controller_choices
        """
        ...
    @_ty.overload
    def usb_passthrough_choices(self, 
    /) -> 'list': 
        """
        Available choices for USB passthrough devices.

        Parameters
        ----------
        Returns
        -------
        list:
            usb_passthrough_choices
        """
        ...
    @_ty.overload
    def usb_passthrough_device(self, 
        device:'str',
    /) -> 'dict[str]': 
        """
        Retrieve details about `device` USB device.

        Parameters
        ----------
        device:
            device
        Returns
        -------
        dict[str]:
            usb_passthrough_device
        """
        ...
