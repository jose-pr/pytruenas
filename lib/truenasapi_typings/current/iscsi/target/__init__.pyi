from pytruenas import Namespace as _NS
 
class IscsiTarget(_NS):
    
    def create(
        
    ) -> IscsiTargetCreate:
        ...
    
    def delete(
        
    ) -> IscsiTargetDelete:
        ...
    
    def get_instance(
        
    ) -> IscsiTargetGet_instance:
        ...
    
    def query(
        
    ) -> IscsiTargetQuery:
        ...
    
    def update(
        
    ) -> IscsiTargetUpdate:
        ...
    
    def validate_name(
        
    ) -> IscsiTargetValidate_name:
        ...
     
     



class IscsiTargetCreate:
    ...

class IscsiTargetDelete:
    ...

class IscsiTargetGet_instance:
    ...

class IscsiTargetQuery:
    ...

class IscsiTargetUpdate:
    ...

class IscsiTargetValidate_name:
    ...
 