from pytruenas import Namespace as _NS
from .network import DockerNetwork 
class Docker(_NS):
    
    def backup(self,
        backup_name,
    ) -> DockerBackup:
        """Create a backup of existing apps."""
        ...
    def config(self,
    ) -> DockerConfig:
        """"""
        ...
    def delete_backup(self,
        backup_name,
    ) -> DockerDelete_backup:
        """Delete `backup_name` app backup."""
        ...
    def list_backups(self,
    ) -> DockerList_backups:
        """List existing app backups."""
        ...
    def nvidia_present(self,
    ) -> DockerNvidia_present:
        """"""
        ...
    def restore_backup(self,
        backup_name,
    ) -> DockerRestore_backup:
        """Restore a backup of existing apps."""
        ...
    def status(self,
    ) -> DockerStatus:
        """Returns the status of the docker service."""
        ...
    def update(self,
        docker_update,
    ) -> DockerUpdate:
        """Update Docker service configuration."""
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