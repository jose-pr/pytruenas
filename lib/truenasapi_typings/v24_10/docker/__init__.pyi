from pytruenas import Namespace as _NS
import typing as _ty
from .network import DockerNetwork 
class Docker(_NS):
    
    def backup(self,
        backup_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerBackup:
        """Create a backup of existing apps."""
        ...
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerConfig:
        """"""
        ...
    def delete_backup(self,
        backup_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerDelete_backup:
        """Delete `backup_name` app backup."""
        ...
    def list_backups(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerList_backups:
        """List existing app backups."""
        ...
    def nvidia_present(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerNvidia_present:
        """"""
        ...
    def restore_backup(self,
        backup_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerRestore_backup:
        """Restore a backup of existing apps."""
        ...
    def status(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerStatus:
        """Returns the status of the docker service."""
        ...
    def update(self,
        docker_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerUpdate:
        """Update Docker service configuration."""
        ...
    network: DockerNetwork
class DockerBackup(_ty.TypedDict):
    ...
class DockerConfig(_ty.TypedDict):
    ...
class DockerDelete_backup(_ty.TypedDict):
    ...
class DockerList_backups(_ty.TypedDict):
    ...
class DockerNvidia_present(_ty.TypedDict):
    ...
class DockerRestore_backup(_ty.TypedDict):
    ...
class DockerStatus(_ty.TypedDict):
    ...
class DockerUpdate(_ty.TypedDict):
    ... 