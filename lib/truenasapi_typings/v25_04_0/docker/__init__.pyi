from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .network import Network 
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
    ) -> ConfigReturn:
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
    ) -> StatusReturn:
        """Returns the status of the docker service."""
        ...
    def update(self,
        docker_update:UpdateDockerUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update Docker service configuration."""
        ...
    network: Network
ConfigReturn = _ty.TypedDict('ConfigReturn', {
    'id': int,
    'enable_image_updates': bool,
    'dataset': str|None,
    'pool': str|None,
    'nvidia': bool,
    'address_pools': list[_jsonschema.JsonObject],
    'cidr_v6': str, 
})
StatusReturn = _ty.TypedDict('StatusReturn', {
    'description': str,
    'status': str, 
})
UpdateDockerUpdate = _ty.TypedDict('UpdateDockerUpdate', {
    'enable_image_updates': _ty.NotRequired[bool],
    'pool': _ty.NotRequired[str|None],
    'nvidia': _ty.NotRequired[bool],
    'address_pools': _ty.NotRequired[_jsonschema.JsonArray],
    'cidr_v6': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'enable_image_updates': bool,
    'dataset': str|None,
    'pool': str|None,
    'nvidia': bool,
    'address_pools': list[_jsonschema.JsonObject],
    'cidr_v6': str, 
})