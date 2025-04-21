from pytruenas import Namespace as _NS
from .network import DockerNetwork 
class Docker(_NS):
    
    def backup(
        backup_name,
    ) -> DockerBackup:
        """Create a backup of existing apps."""
        ...
    def config(
    ) -> DockerConfig:
        """"""
        ...
    def delete_backup(
        backup_name,
    ) -> DockerDelete_backup:
        """Delete `backup_name` app backup."""
        ...
    def list_backups(
    ) -> DockerList_backups:
        """List existing app backups."""
        ...
    def nvidia_present(
    ) -> DockerNvidia_present:
        """"""
        ...
    def restore_backup(
        backup_name,
    ) -> DockerRestore_backup:
        """Restore a backup of existing apps."""
        ...
    def status(
    ) -> DockerStatus:
        """Returns the status of the docker service."""
        ...
    def update(
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