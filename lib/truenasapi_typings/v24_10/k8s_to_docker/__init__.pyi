from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class K8sToDocker(_NS):
    
    def list_backups(self,
        kubernetes_pool:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ListBackupsReturn:
        """List existing kubernetes backups"""
        ...
    def migrate(self,
        kubernetes_pool:str,
        options:MigrateOptions={'backup_name': None},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[MigrateAppMigrationDetails]:
        """Migrate kubernetes backups to docker."""
        ...
ListBackupsReturn = _ty.TypedDict('ListBackupsReturn', {
    'error': str|None,
    'backups': _jsonschema.JsonValue, 
})
MigrateOptions = _ty.TypedDict('MigrateOptions', {
    'backup_name': _ty.NotRequired[str|None], 
})
MigrateAppMigrationDetails = _ty.TypedDict('MigrateAppMigrationDetails', {
    'name': str,
    'successfully_migrated': bool,
    'error': str|None, 
})