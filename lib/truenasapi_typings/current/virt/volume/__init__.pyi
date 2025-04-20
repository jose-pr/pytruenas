from pytruenas import Namespace as _NS
 
class VirtVolume(_NS):
    
    def create(
        
    ) -> VirtVolumeCreate:
        ...
    
    def delete(
        
    ) -> VirtVolumeDelete:
        ...
    
    def get_instance(
        
    ) -> VirtVolumeGet_instance:
        ...
    
    def import_iso(
        
    ) -> VirtVolumeImport_iso:
        ...
    
    def import_zvol(
        
    ) -> VirtVolumeImport_zvol:
        ...
    
    def query(
        
    ) -> VirtVolumeQuery:
        ...
    
    def update(
        
    ) -> VirtVolumeUpdate:
        ...
     
     



class VirtVolumeCreate:
    ...

class VirtVolumeDelete:
    ...

class VirtVolumeGet_instance:
    ...

class VirtVolumeImport_iso:
    ...

class VirtVolumeImport_zvol:
    ...

class VirtVolumeQuery:
    ...

class VirtVolumeUpdate:
    ...
 