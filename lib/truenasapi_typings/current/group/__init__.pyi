from pytruenas import Namespace as _NS
 
class Group(_NS):
    
    def create(
        
    ) -> GroupCreate:
        ...
    
    def delete(
        
    ) -> GroupDelete:
        ...
    
    def get_group_obj(
        
    ) -> GroupGet_group_obj:
        ...
    
    def get_instance(
        
    ) -> GroupGet_instance:
        ...
    
    def get_next_gid(
        
    ) -> GroupGet_next_gid:
        ...
    
    def has_password_enabled_user(
        
    ) -> GroupHas_password_enabled_user:
        ...
    
    def query(
        
    ) -> GroupQuery:
        ...
    
    def update(
        
    ) -> GroupUpdate:
        ...
     
     



class GroupCreate:
    ...

class GroupDelete:
    ...

class GroupGet_group_obj:
    ...

class GroupGet_instance:
    ...

class GroupGet_next_gid:
    ...

class GroupHas_password_enabled_user:
    ...

class GroupQuery:
    ...

class GroupUpdate:
    ...
 