from pytruenas import Namespace as _NS
import typing as _ty 
class K8s_to_docker(_NS):
    
    def list_backups(self,
        kubernetes_pool,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> K8s_to_dockerList_backups:
        """List existing kubernetes backups"""
        ...
    def migrate(self,
        kubernetes_pool,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> K8s_to_dockerMigrate:
        """Migrate kubernetes backups to docker."""
        ...
class K8s_to_dockerList_backups(_ty.TypedDict):
    ...
class K8s_to_dockerMigrate(_ty.TypedDict):
    ... 