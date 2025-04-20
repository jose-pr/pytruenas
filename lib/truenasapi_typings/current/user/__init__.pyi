from pytruenas import Namespace as _NS
 
class User(_NS):
    
    def create(
        
    ) -> UserCreate:
        ...
    
    def delete(
        
    ) -> UserDelete:
        ...
    
    def get_instance(
        
    ) -> UserGet_instance:
        ...
    
    def get_next_uid(
        
    ) -> UserGet_next_uid:
        ...
    
    def get_user_obj(
        
    ) -> UserGet_user_obj:
        ...
    
    def has_local_administrator_set_up(
        
    ) -> UserHas_local_administrator_set_up:
        ...
    
    def query(
        
    ) -> UserQuery:
        ...
    
    def renew_2fa_secret(
        
    ) -> UserRenew_2fa_secret:
        ...
    
    def set_password(
        
    ) -> UserSet_password:
        ...
    
    def setup_local_administrator(
        
    ) -> UserSetup_local_administrator:
        ...
    
    def shell_choices(
        
    ) -> UserShell_choices:
        ...
    
    def unset_2fa_secret(
        
    ) -> UserUnset_2fa_secret:
        ...
    
    def update(
        
    ) -> UserUpdate:
        ...
     
     



class UserCreate:
    ...

class UserDelete:
    ...

class UserGet_instance:
    ...

class UserGet_next_uid:
    ...

class UserGet_user_obj:
    ...

class UserHas_local_administrator_set_up:
    ...

class UserQuery:
    ...

class UserRenew_2fa_secret:
    ...

class UserSet_password:
    ...

class UserSetup_local_administrator:
    ...

class UserShell_choices:
    ...

class UserUnset_2fa_secret:
    ...

class UserUpdate:
    ...
 