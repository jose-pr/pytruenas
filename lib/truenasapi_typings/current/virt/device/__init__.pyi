from pytruenas import Namespace as _NS
import typing as _ty 
class VirtDevice(_NS):
    
    def disk_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtDeviceDisk_choices:
        """Returns disk choices available for device type "DISK" for virtual machines. This includes both available virt volumes and zvol choices. Disk choices for containers depend on the mounted file tree (paths)."""
        ...
    def export_disk_image(self,
        virt_device_export_disk_image,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtDeviceExport_disk_image:
        """Exports a zvol to a formatted VM disk image.

Utilized qemu-img with the conversion functionality to export a zvol to any supported disk image format, from RAW -> ${OTHER}. The resulting file will be set to inherit the permissions of the target directory.

As of this implementation it supports the following {format} options :

- QCOW2 - QED - RAW - VDI - VPC - VMDK

`format` is a required parameter for the exported disk image `directory` is a required parameter for the export disk image `zvol` is the source for the disk image"""
        ...
    def gpu_choices(self,
        gpu_type,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtDeviceGpu_choices:
        """Provide choices for GPU devices."""
        ...
    def import_disk_image(self,
        virt_device_import_disk_image,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtDeviceImport_disk_image:
        """Imports a specified disk image.

Utilized qemu-img with the auto-detect functionality to auto-convert any supported disk image format to RAW -> ZVOL

As of this implementation it supports:

- QCOW2 - QED - RAW - VDI - VPC - VMDK

`diskimg` is a required parameter for the incoming disk image `zvol` is the required target for the imported disk image"""
        ...
    def nic_choices(self,
        nic_type,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtDeviceNic_choices:
        """Returns choices for NIC device."""
        ...
    def pci_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtDevicePci_choices:
        """Returns choices for PCI devices valid for VM virt instances."""
        ...
    def usb_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtDeviceUsb_choices:
        """Provide choices for USB devices."""
        ...
class VirtDeviceDisk_choices(_ty.TypedDict):
    ...
class VirtDeviceExport_disk_image(_ty.TypedDict):
    ...
class VirtDeviceGpu_choices(_ty.TypedDict):
    ...
class VirtDeviceImport_disk_image(_ty.TypedDict):
    ...
class VirtDeviceNic_choices(_ty.TypedDict):
    ...
class VirtDevicePci_choices(_ty.TypedDict):
    ...
class VirtDeviceUsb_choices(_ty.TypedDict):
    ... 