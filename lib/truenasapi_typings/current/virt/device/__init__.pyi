from pytruenas import Namespace as _NS
 
class VirtDevice(_NS):
    
    def disk_choices(
        
    ) -> VirtDeviceDisk_choices:
        ...
    
    def export_disk_image(
        
    ) -> VirtDeviceExport_disk_image:
        ...
    
    def gpu_choices(
        
    ) -> VirtDeviceGpu_choices:
        ...
    
    def import_disk_image(
        
    ) -> VirtDeviceImport_disk_image:
        ...
    
    def nic_choices(
        
    ) -> VirtDeviceNic_choices:
        ...
    
    def pci_choices(
        
    ) -> VirtDevicePci_choices:
        ...
    
    def usb_choices(
        
    ) -> VirtDeviceUsb_choices:
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
 