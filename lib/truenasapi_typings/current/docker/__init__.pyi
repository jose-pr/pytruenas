from pytruenas import Namespace as _NS

from .network import DockerNetwork
 
class Docker(_NS):
    
    def backup(
        
    ) -> DockerBackup:
        ...
    
    def config(
        
    ) -> DockerConfig:
        ...
    
    def delete_backup(
        
    ) -> DockerDelete_backup:
        ...
    
    def list_backups(
        
    ) -> DockerList_backups:
        ...
    
    def nvidia_present(
        
    ) -> DockerNvidia_present:
        ...
    
    def restore_backup(
        
    ) -> DockerRestore_backup:
        ...
    
    def status(
        
    ) -> DockerStatus:
        ...
    
    def update(
        
    ) -> DockerUpdate:
        ...
     
    
    network: DockerNetwork
     



class DockerBackup:
    ...

class DockerConfig:
    ...

class DockerDelete_backup:
    ...

class DockerList_backups:
    ...

class DockerNvidia_present:
    ...

class DockerRestore_backup:
    ...

class DockerStatus:
    ...

class DockerUpdate:
    ...
 