from pytruenas import Namespace as _NS 
class K8s_to_docker(_NS):
    
    def list_backups(
        kubernetes_pool,
    ) -> K8s_to_dockerList_backups:
        """List existing kubernetes backups"""
        ...
    def migrate(
        kubernetes_pool,
        options,
    ) -> K8s_to_dockerMigrate:
        """Migrate kubernetes backups to docker."""
        ...
class K8s_to_dockerList_backups:
    ...
class K8s_to_dockerMigrate:
    ... 