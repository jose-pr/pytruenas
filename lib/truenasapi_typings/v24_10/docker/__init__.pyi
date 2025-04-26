from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .network import DockerNetwork 
class Docker(_NS):
    
    def backup(self,
        backup_name:str|None=None,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str:
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
        backup_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Delete `backup_name` app backup."""
        ...
    def list_backups(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """List existing app backups."""
        ...
    def nvidia_present(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """"""
        ...
    def restore_backup(self,
        backup_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
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
        docker_update:docker_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DockerUpdate:
        """Update Docker service configuration."""
        ...
    network: DockerNetwork
DockerConfig = _ty.TypedDict('DockerConfig', {
    'id': int,
    'enable_image_updates': bool,
    'dataset': str|None,
    'pool': str|None,
    'nvidia': bool,
    'address_pools': list[_jsonschema.JsonObject],
    'cidr_v6': str, 
})
DockerStatus = _ty.TypedDict('DockerStatus', {
    'description': str,
    'status': str, 
})
docker_update = _ty.TypedDict('docker_update', {
    'enable_image_updates': _ty.NotRequired[bool],
    'pool': _ty.NotRequired[str|None],
    'nvidia': _ty.NotRequired[bool],
    'address_pools': _ty.NotRequired[_jsonschema.JsonArray],
    'cidr_v6': _ty.NotRequired[str], 
})
DockerUpdate = _ty.TypedDict('DockerUpdate', {
    'id': int,
    'enable_image_updates': bool,
    'dataset': str|None,
    'pool': str|None,
    'nvidia': bool,
    'address_pools': list[_jsonschema.JsonObject],
    'cidr_v6': str, 
})