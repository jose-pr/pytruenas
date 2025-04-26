from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class K8s_to_docker(_NS):
    
    def list_backups(self,
        kubernetes_pool:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> K8s_to_dockerList_backups:
        """List existing kubernetes backups"""
        ...
    def migrate(self,
        kubernetes_pool:str,
        options:options={'backup_name': None},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AppMigrationDetails]:
        """Migrate kubernetes backups to docker."""
        ...
K8s_to_dockerList_backups = _ty.TypedDict('K8s_to_dockerList_backups', {
    'error': str|None,
    'backups': _jsonschema.JsonValue, 
})
options = _ty.TypedDict('options', {
    'backup_name': _ty.NotRequired[str|None], 
})
AppMigrationDetails = _ty.TypedDict('AppMigrationDetails', {
    'name': str,
    'successfully_migrated': bool,
    'error': str|None, 
})