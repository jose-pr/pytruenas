from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Volume(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[VirtVolumeCreate],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:str|_ty.Sequence[str],
        **fields:_ty.Unpack[VirtVolumeUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:str|_ty.Sequence[str],
        **fields:_ty.Unpack[VirtVolumeUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        virt_volume_create:CreateVirtVolumeCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
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
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def import_iso(self,
        virt_volume_import_iso:ImportIsoVirtVolumeImportIso,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ImportIsoReturn:
        """"""
        ...
    def import_zvol(self,
        virt_volume_import_iso:ImportZvolVirtVolumeImportIso,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ImportZvolReturn:
        """"""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryVirtVolumeQueryResultItem]|QueryVirtVolumeQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:str,
        virt_volume_update:UpdateVirtVolumeUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """"""
        ...
VirtVolumeCreate = _ty.TypedDict('VirtVolumeCreate', {
    'name': str,
    'content_type': _ty.NotRequired[str],
    'size': _ty.NotRequired[int],
    'storage_pool': _ty.NotRequired[str|None], 
})
VirtVolumeUpdate = _ty.TypedDict('VirtVolumeUpdate', {
    'size': _ty.NotRequired[int], 
})
CreateVirtVolumeCreate = _ty.TypedDict('CreateVirtVolumeCreate', {
    'name': str,
    'content_type': _ty.NotRequired[str],
    'size': _ty.NotRequired[int],
    'storage_pool': _ty.NotRequired[str|None], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': str,
    'name': str,
    'storage_pool': str,
    'content_type': str,
    'created_at': str,
    'type': str,
    'config': _jsonschema.JsonObject,
    'used_by': list[str], 
})
GetInstanceOptions = _ty.TypedDict('GetInstanceOptions', {
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
GetInstanceReturn = _ty.TypedDict('GetInstanceReturn', {
    'id': str,
    'name': str,
    'storage_pool': str,
    'content_type': str,
    'created_at': str,
    'type': str,
    'config': _jsonschema.JsonObject,
    'used_by': list[str], 
})
ImportIsoVirtVolumeImportIso = _ty.TypedDict('ImportIsoVirtVolumeImportIso', {
    'name': str,
    'iso_location': _ty.NotRequired[str|None],
    'upload_iso': _ty.NotRequired[bool],
    'storage_pool': _ty.NotRequired[str|None], 
})
ImportIsoReturn = _ty.TypedDict('ImportIsoReturn', {
    'id': str,
    'name': str,
    'storage_pool': str,
    'content_type': str,
    'created_at': str,
    'type': str,
    'config': _jsonschema.JsonObject,
    'used_by': list[str], 
})
ImportZvolVirtVolumeImportIso = _ty.TypedDict('ImportZvolVirtVolumeImportIso', {
    'to_import': _jsonschema.JsonArray,
    'clone': _ty.NotRequired[bool], 
})
ImportZvolReturn = _ty.TypedDict('ImportZvolReturn', {
    'id': str,
    'name': str,
    'storage_pool': str,
    'content_type': str,
    'created_at': str,
    'type': str,
    'config': _jsonschema.JsonObject,
    'used_by': list[str], 
})
QueryOptions = _ty.TypedDict('QueryOptions', {
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
QueryVirtVolumeQueryResultItem = _ty.TypedDict('QueryVirtVolumeQueryResultItem', {
    'id': _ty.NotRequired[str],
    'name': _ty.NotRequired[str],
    'storage_pool': _ty.NotRequired[str],
    'content_type': _ty.NotRequired[str],
    'created_at': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'config': _ty.NotRequired[_jsonschema.JsonObject],
    'used_by': _ty.NotRequired[list[str]], 
})
UpdateVirtVolumeUpdate = _ty.TypedDict('UpdateVirtVolumeUpdate', {
    'size': _ty.NotRequired[int], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': str,
    'name': str,
    'storage_pool': str,
    'content_type': str,
    'created_at': str,
    'type': str,
    'config': _jsonschema.JsonObject,
    'used_by': list[str], 
})