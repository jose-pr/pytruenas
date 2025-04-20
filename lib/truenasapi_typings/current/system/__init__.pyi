from pytruenas import Namespace as _NS

from .general import SystemGeneral

from .ntpserver import SystemNtpserver

from .reboot import SystemReboot

from .security import SystemSecurity
 
class System(_NS):
    
    def reboot(
        
    ) -> SystemReboot:
        ...
    
    def shutdown(
        
    ) -> SystemShutdown:
        ...
     
    
    general: SystemGeneral
    
    ntpserver: SystemNtpserver
    
    reboot: SystemReboot
    
    security: SystemSecurity
     



class SystemReboot:
    ...

class SystemShutdown:
    ...
 