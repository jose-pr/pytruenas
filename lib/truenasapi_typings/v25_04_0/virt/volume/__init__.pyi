from pytruenas import Namespace as _NS 
class VirtVolume(_NS):
    
    def create(self,
        virt_volume_create,
    ) -> VirtVolumeCreate:
        """"""
        ...
    def delete(self,
        id,
    ) -> VirtVolumeDelete:
        """"""
        ...
    def get_instance(self,
        id,
        options,
    ) -> VirtVolumeGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def import_iso(self,
        virt_volume_import_iso,
    ) -> VirtVolumeImport_iso:
        """"""
        ...
    def import_zvol(self,
        virt_volume_import_iso,
    ) -> VirtVolumeImport_zvol:
        """"""
        ...
    def query(self,
        filters,
        options,
    ) -> VirtVolumeQuery:
        """"""
        ...
    def update(self,
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