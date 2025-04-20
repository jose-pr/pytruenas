from pytruenas import Namespace as _NS

from .info import SystemSecurityInfo
 
class SystemSecurity(_NS):
    
    def config(
        
    ) -> SystemSecurityConfig:
        ...
    
    def update(
        
    ) -> SystemSecurityUpdate:
        ...
     
    
    info: SystemSecurityInfo
     



class SystemSecurityConfig:
    ...

class SystemSecurityUpdate:
    ...
 