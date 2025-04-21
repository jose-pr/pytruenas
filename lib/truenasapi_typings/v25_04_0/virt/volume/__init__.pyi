from pytruenas import Namespace as _NS 
class VirtVolume(_NS):
    
    def create(
        virt_volume_create,
    ) -> VirtVolumeCreate:
        """"""
        ...
    def delete(
        id,
    ) -> VirtVolumeDelete:
        """"""
        ...
    def get_instance(
        id,
        options,
    ) -> VirtVolumeGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def import_iso(
        virt_volume_import_iso,
    ) -> VirtVolumeImport_iso:
        """"""
        ...
    def import_zvol(
        virt_volume_import_iso,
    ) -> VirtVolumeImport_zvol:
        """"""
        ...
    def query(
        filters,
        options,
    ) -> VirtVolumeQuery:
        """"""
        ...
    def update(
        id,
        virt_volume_update,
    ) -> VirtVolumeUpdate:
        """"""
        ...
class VirtVolumeCreate:
    ...
class VirtVolumeDelete:
    ...
class VirtVolumeGet_instance:
    ...
class VirtVolumeImport_iso:
    ...
class VirtVolumeImport_zvol:
    ...
class VirtVolumeQuery:
    ...
class VirtVolumeUpdate:
    ... 