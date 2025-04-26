from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class VirtVolume(_NS):
    
    def create(self,
        virt_volume_create:virt_volume_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeCreate:
        """"""
        ...
    def delete(self,
        id:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """"""
        ...
    def get_instance(self,
        id:str,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def import_iso(self,
        virt_volume_import_iso:virt_volume_import_iso,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeImport_iso:
        """"""
        ...
    def import_zvol(self,
        virt_volume_import_iso:virt_volume_import_iso,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeImport_zvol:
        """"""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[VirtVolumeQueryResultItem]|VirtVolumeQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:str,
        virt_volume_update:virt_volume_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtVolumeUpdate:
        """"""
        ...
virt_volume_create = _ty.TypedDict('virt_volume_create', {
    'name': str,
    'content_type': _ty.NotRequired[str],
    'size': _ty.NotRequired[int],
    'storage_pool': _ty.NotRequired[str|None], 
})
VirtVolumeCreate = _ty.TypedDict('VirtVolumeCreate', {
    'id': str,
    'name': str,
    'storage_pool': str,
    'content_type': str,
    'created_at': str,
    'type': str,
    'config': _jsonschema.JsonObject,
    'used_by': list[str], 
})
options = _ty.TypedDict('options', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
VirtVolumeGet_instance = _ty.TypedDict('VirtVolumeGet_instance', {
    'id': str,
    'name': str,
    'storage_pool': str,
    'content_type': str,
    'created_at': str,
    'type': str,
    'config': _jsonschema.JsonObject,
    'used_by': list[str], 
})
virt_volume_import_iso = _ty.TypedDict('virt_volume_import_iso', {
    'to_import': _jsonschema.JsonArray,
    'clone': _ty.NotRequired[bool], 
})
VirtVolumeImport_iso = _ty.TypedDict('VirtVolumeImport_iso', {
    'id': str,
    'name': str,
    'storage_pool': str,
    'content_type': str,
    'created_at': str,
    'type': str,
    'config': _jsonschema.JsonObject,
    'used_by': list[str], 
})
VirtVolumeImport_zvol = _ty.TypedDict('VirtVolumeImport_zvol', {
    'id': str,
    'name': str,
    'storage_pool': str,
    'content_type': str,
    'created_at': str,
    'type': str,
    'config': _jsonschema.JsonObject,
    'used_by': list[str], 
})
VirtVolumeQueryResultItem = _ty.TypedDict('VirtVolumeQueryResultItem', {
    'id': _ty.NotRequired[str],
    'name': _ty.NotRequired[str],
    'storage_pool': _ty.NotRequired[str],
    'content_type': _ty.NotRequired[str],
    'created_at': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'config': _ty.NotRequired[_jsonschema.JsonObject],
    'used_by': _ty.NotRequired[list[str]], 
})
virt_volume_update = _ty.TypedDict('virt_volume_update', {
    'size': _ty.NotRequired[int], 
})
VirtVolumeUpdate = _ty.TypedDict('VirtVolumeUpdate', {
    'id': str,
    'name': str,
    'storage_pool': str,
    'content_type': str,
    'created_at': str,
    'type': str,
    'config': _jsonschema.JsonObject,
    'used_by': list[str], 
})