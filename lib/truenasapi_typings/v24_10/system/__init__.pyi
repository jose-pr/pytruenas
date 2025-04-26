from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .general import General
from .ntpserver import Ntpserver
from .reboot import Reboot
from .security import Security 
class System(_NS):
    
    def reboot(self,
        reason:str,
        options:RebootOptions={'delay': None},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Reboots the operating system.

Emits an "added" event of name "system" and id "reboot"."""
        ...
    def shutdown(self,
        reason:str,
        options:ShutdownOptions={'delay': None},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Shuts down the operating system.

An "added" event of name "system" and id "shutdown" is emitted when shutdown is initiated."""
        ...
    general: General
    ntpserver: Ntpserver
    reboot: Reboot
    security: Security
RebootOptions = _ty.TypedDict('RebootOptions', {
    'delay': _ty.NotRequired[int|None], 
})
ShutdownOptions = _ty.TypedDict('ShutdownOptions', {
    'delay': _ty.NotRequired[int|None], 
})