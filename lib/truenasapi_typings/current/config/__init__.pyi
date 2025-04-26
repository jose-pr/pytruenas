from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Config(_NS):
    
    def reset(self,
        options:ResetOptions={'reboot': True},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Reset database to configuration defaults.

If `reboot` is true this job will reboot the system after its completed with a delay of 10 seconds."""
        ...
    def save(self,
        options:SaveOptions={'secretseed': False, 'pool_keys': False, 'root_authorized_keys': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Create a tar file of security-sensitive information. These options select which information is included in the tar file:

`secretseed` bool: When true, include password secret seed. `pool_keys` bool: IGNORED and DEPRECATED as it does not apply on SCALE systems. `root_authorized_keys` bool: When true, include "/root/.ssh/authorized_keys" file for the root user.

If none of these options are set, the tar file is not generated and the database file is returned."""
        ...
    def upload(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Accepts a configuration file via job pipe."""
        ...
ResetOptions = _ty.TypedDict('ResetOptions', {
    'reboot': _ty.NotRequired[bool], 
})
SaveOptions = _ty.TypedDict('SaveOptions', {
    'secretseed': _ty.NotRequired[bool],
    'pool_keys': _ty.NotRequired[bool],
    'root_authorized_keys': _ty.NotRequired[bool], 
})