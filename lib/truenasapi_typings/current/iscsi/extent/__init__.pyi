from pytruenas import Namespace as _NS
 
class IscsiExtent(_NS):
    
    def create(
        
    ) -> IscsiExtentCreate:
        ...
    
    def delete(
        
    ) -> IscsiExtentDelete:
        ...
    
    def disk_choices(
        
    ) -> IscsiExtentDisk_choices:
        ...
    
    def get_instance(
        
    ) -> IscsiExtentGet_instance:
        ...
    
    def query(
        
    ) -> IscsiExtentQuery:
        ...
    
    def update(
        
    ) -> IscsiExtentUpdate:
        ...
     
     



class IscsiExtentCreate:
    ...

class IscsiExtentDelete:
    ...

class IscsiExtentDisk_choices:
    ...

class IscsiExtentGet_instance:
    ...

class IscsiExtentQuery:
    ...

class IscsiExtentUpdate:
    ...
 