from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class VirtDevice(_NS):
    
    def disk_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns disk choices available for device type "DISK" for virtual machines. This includes both available virt volumes and zvol choices. Disk choices for containers depend on the mounted file tree (paths)."""
        ...
    def export_disk_image(self,
        virt_device_export_disk_image:virt_device_export_disk_image,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Exports a zvol to a formatted VM disk image.

Utilized qemu-img with the conversion functionality to export a zvol to any supported disk image format, from RAW -> ${OTHER}. The resulting file will be set to inherit the permissions of the target directory.

As of this implementation it supports the following {format} options :

- QCOW2 - QED - RAW - VDI - VPC - VMDK

`format` is a required parameter for the exported disk image `directory` is a required parameter for the export disk image `zvol` is the source for the disk image"""
        ...
    def gpu_choices(self,
        gpu_type:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Provide choices for GPU devices."""
        ...
    def import_disk_image(self,
        virt_device_import_disk_image:virt_device_import_disk_image,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Imports a specified disk image.

Utilized qemu-img with the auto-detect functionality to auto-convert any supported disk image format to RAW -> ZVOL

As of this implementation it supports:

- QCOW2 - QED - RAW - VDI - VPC - VMDK

`diskimg` is a required parameter for the incoming disk image `zvol` is the required target for the imported disk image"""
        ...
    def nic_choices(self,
        nic_type:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns choices for NIC device."""
        ...
    def pci_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns choices for PCI devices valid for VM virt instances."""
        ...
    def usb_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Provide choices for USB devices."""
        ...
virt_device_export_disk_image = _ty.TypedDict('virt_device_export_disk_image', {
    'format': str,
    'directory': str,
    'zvol': str, 
})
virt_device_import_disk_image = _ty.TypedDict('virt_device_import_disk_image', {
    'diskimg': str,
    'zvol': str, 
})