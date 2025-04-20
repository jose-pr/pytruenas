from pytruenas import Namespace as _NS
 
class Auth(_NS):
    
    def generate_onetime_password(
        
    ) -> AuthGenerate_onetime_password:
        ...
    
    def generate_token(
        
    ) -> AuthGenerate_token:
        ...
    
    def login(
        
    ) -> AuthLogin:
        ...
    
    def login_ex(
        
    ) -> AuthLogin_ex:
        ...
    
    def login_ex_continue(
        
    ) -> AuthLogin_ex_continue:
        ...
    
    def login_with_api_key(
        
    ) -> AuthLogin_with_api_key:
        ...
    
    def login_with_token(
        
    ) -> AuthLogin_with_token:
        ...
    
    def logout(
        
    ) -> AuthLogout:
        ...
    
    def me(
        
    ) -> AuthMe:
        ...
    
    def mechanism_choices(
        
    ) -> AuthMechanism_choices:
        ...
    
    def sessions(
        
    ) -> AuthSessions:
        ...
    
    def set_attribute(
        
    ) -> AuthSet_attribute:
        ...
    
    def terminate_other_sessions(
        
    ) -> AuthTerminate_other_sessions:
        ...
    
    def terminate_session(
        
    ) -> AuthTerminate_session:
        ...
     
     



class AuthGenerate_onetime_password:
    ...

class AuthGenerate_token:
    ...

class AuthLogin:
    ...

class AuthLogin_ex:
    ...

class AuthLogin_ex_continue:
    ...

class AuthLogin_with_api_key:
    ...

class AuthLogin_with_token:
    ...

class AuthLogout:
    ...

class AuthMe:
    ...

class AuthMechanism_choices:
    ...

class AuthSessions:
    ...

class AuthSet_attribute:
    ...

class AuthTerminate_other_sessions:
    ...

class AuthTerminate_session:
    ...
 