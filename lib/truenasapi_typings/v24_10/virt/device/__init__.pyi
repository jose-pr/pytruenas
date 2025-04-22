from pytruenas import Namespace as _NS 
class VirtDevice(_NS):
    
    def disk_choices(self,
    ) -> VirtDeviceDisk_choices:
        """Returns disk choices available for device type "DISK" for virtual machines. This includes both available virt volumes and zvol choices. Disk choices for containers depend on the mounted file tree (paths)."""
        ...
    def export_disk_image(self,
        virt_device_export_disk_image,
    ) -> VirtDeviceExport_disk_image:
        """Exports a zvol to a formatted VM disk image.

Utilized qemu-img with the conversion functionality to export a zvol to any supported disk image format, from RAW -> ${OTHER}. The resulting file will be set to inherit the permissions of the target directory.

As of this implementation it supports the following {format} options :

- QCOW2 - QED - RAW - VDI - VPC - VMDK

`format` is a required parameter for the exported disk image `directory` is a required parameter for the export disk image `zvol` is the source for the disk image"""
        ...
    def gpu_choices(self,
        gpu_type,
    ) -> VirtDeviceGpu_choices:
        """Provide choices for GPU devices."""
        ...
    def import_disk_image(self,
        virt_device_import_disk_image,
    ) -> VirtDeviceImport_disk_image:
        """Imports a specified disk image.

Utilized qemu-img with the auto-detect functionality to auto-convert any supported disk image format to RAW -> ZVOL

As of this implementation it supports:

- QCOW2 - QED - RAW - VDI - VPC - VMDK

`diskimg` is a required parameter for the incoming disk image `zvol` is the required target for the imported disk image"""
        ...
    def nic_choices(self,
        nic_type,
    ) -> VirtDeviceNic_choices:
        """Returns choices for NIC device."""
        ...
    def pci_choices(self,
    ) -> VirtDevicePci_choices:
        """Returns choices for PCI devices valid for VM virt instances."""
        ...
    def usb_choices(self,
    ) -> VirtDeviceUsb_choices:
        """Provide choices for USB devices."""
        ...
class VirtDeviceDisk_choices:
    ...
class VirtDeviceExport_disk_image:
    ...
class VirtDeviceGpu_choices:
    ...
class VirtDeviceImport_disk_image:
    ...
class VirtDeviceNic_choices:
    ...
class VirtDevicePci_choices:
    ...
class VirtDeviceUsb_choices:
    ... 