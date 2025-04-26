from pytruenas import Namespace as _NS
import typing as _ty 
class Config(_NS):
    
    def reset(self,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ConfigReset:
        """Reset database to configuration defaults.

If `reboot` is true this job will reboot the system after its completed with a delay of 10 seconds."""
        ...
    def save(self,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ConfigSave:
        """Create a tar file of security-sensitive information. These options select which information is included in the tar file:

`secretseed` bool: When true, include password secret seed. `pool_keys` bool: IGNORED and DEPRECATED as it does not apply on SCALE systems. `root_authorized_keys` bool: When true, include "/root/.ssh/authorized_keys" file for the root user.

If none of these options are set, the tar file is not generated and the database file is returned."""
        ...
    def upload(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ConfigUpload:
        """Accepts a configuration file via job pipe."""
        ...
class ConfigReset(_ty.TypedDict):
    ...
class ConfigSave(_ty.TypedDict):
    ...
class ConfigUpload(_ty.TypedDict):
    ... 