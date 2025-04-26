from pytruenas import Namespace as _NS
import typing as _ty
from .general import SystemGeneral
from .ntpserver import SystemNtpserver
from .reboot import SystemReboot
from .security import SystemSecurity 
class System(_NS):
    
    def reboot(self,
        reason,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemReboot:
        """Reboots the operating system.

Emits an "added" event of name "system" and id "reboot"."""
        ...
    def shutdown(self,
        reason,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemShutdown:
        """Shuts down the operating system.

An "added" event of name "system" and id "shutdown" is emitted when shutdown is initiated."""
        ...
    general: SystemGeneral
    ntpserver: SystemNtpserver
    reboot: SystemReboot
    security: SystemSecurity
class SystemReboot(_ty.TypedDict):
    ...
class SystemShutdown(_ty.TypedDict):
    ... 