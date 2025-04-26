from pytruenas import Namespace as _NS
import typing as _ty 
class VirtVolume(_NS):
    
    def create(self,
        virt_volume_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeCreate:
        """"""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeDelete:
        """"""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def import_iso(self,
        virt_volume_import_iso,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeImport_iso:
        """"""
        ...
    def import_zvol(self,
        virt_volume_import_iso,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeImport_zvol:
        """"""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeQuery:
        """"""
        ...
    def update(self,
        id,
        virt_volume_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeUpdate:
        """"""
        ...
class VirtVolumeCreate(_ty.TypedDict):
    ...
class VirtVolumeDelete(_ty.TypedDict):
    ...
class VirtVolumeGet_instance(_ty.TypedDict):
    ...
class VirtVolumeImport_iso(_ty.TypedDict):
    ...
class VirtVolumeImport_zvol(_ty.TypedDict):
    ...
class VirtVolumeQuery(_ty.TypedDict):
    ...
class VirtVolumeUpdate(_ty.TypedDict):
    ... 