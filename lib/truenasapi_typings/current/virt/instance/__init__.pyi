from pytruenas import Namespace as _NS
 
class VirtInstance(_NS):
    
    def create(
        
    ) -> VirtInstanceCreate:
        ...
    
    def delete(
        
    ) -> VirtInstanceDelete:
        ...
    
    def device_add(
        
    ) -> VirtInstanceDevice_add:
        ...
    
    def device_delete(
        
    ) -> VirtInstanceDevice_delete:
        ...
    
    def device_list(
        
    ) -> VirtInstanceDevice_list:
        ...
    
    def device_update(
        
    ) -> VirtInstanceDevice_update:
        ...
    
    def get_instance(
        
    ) -> VirtInstanceGet_instance:
        ...
    
    def image_choices(
        
    ) -> VirtInstanceImage_choices:
        ...
    
    def query(
        
    ) -> VirtInstanceQuery:
        ...
    
    def restart(
        
    ) -> VirtInstanceRestart:
        ...
    
    def start(
        
    ) -> VirtInstanceStart:
        ...
    
    def stop(
        
    ) -> VirtInstanceStop:
        ...
    
    def update(
        
    ) -> VirtInstanceUpdate:
        ...
     
     



class VirtInstanceCreate:
    ...

class VirtInstanceDelete:
    ...

class VirtInstanceDevice_add:
    ...

class VirtInstanceDevice_delete:
    ...

class VirtInstanceDevice_list:
    ...

class VirtInstanceDevice_update:
    ...

class VirtInstanceGet_instance:
    ...

class VirtInstanceImage_choices:
    ...

class VirtInstanceQuery:
    ...

class VirtInstanceRestart:
    ...

class VirtInstanceStart:
    ...

class VirtInstanceStop:
    ...

class VirtInstanceUpdate:
    ...
 