from pytruenas import Namespace as _NS
 
class IscsiGlobal(_NS):
    
    def alua_enabled(
        
    ) -> IscsiGlobalAlua_enabled:
        ...
    
    def client_count(
        
    ) -> IscsiGlobalClient_count:
        ...
    
    def config(
        
    ) -> IscsiGlobalConfig:
        ...
    
    def iser_enabled(
        
    ) -> IscsiGlobalIser_enabled:
        ...
    
    def sessions(
        
    ) -> IscsiGlobalSessions:
        ...
    
    def update(
        
    ) -> IscsiGlobalUpdate:
        ...
     
     



class IscsiGlobalAlua_enabled:
    ...

class IscsiGlobalClient_count:
    ...

class IscsiGlobalConfig:
    ...

class IscsiGlobalIser_enabled:
    ...

class IscsiGlobalSessions:
    ...

class IscsiGlobalUpdate:
    ...
 