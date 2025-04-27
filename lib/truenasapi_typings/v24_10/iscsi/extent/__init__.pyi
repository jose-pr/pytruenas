from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Extent(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[IscsiExtentCreate],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[IscsiExtentUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[IscsiExtentUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        iscsi_extent_create:CreateIscsiExtentCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Create an iSCSI Extent.

When `type` is set to FILE, attribute `filesize` is used and it represents number of bytes. `filesize` if not zero should be a multiple of `blocksize`. `path` is a required attribute with `type` set as FILE.

With `type` being set to DISK, a valid ZFS volume is required.

`insecure_tpc` when enabled allows an initiator to bypass normal access control and access any scannable target. This allows xcopy operations otherwise blocked by access control.

`xen` is a boolean value which is set to true if Xen is being used as the iSCSI initiator.

`ro` when set to true prevents the initiator from writing to this LUN."""
        ...
    def delete(self,
        id:int,
        remove:bool=False,
        force:bool=False,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete iSCSI Extent of `id`.

If `id` iSCSI Extent's `type` was configured to FILE, `remove` can be set to remove the configured file."""
        ...
    def disk_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Return a dict of available zvols that can be used when creating an extent."""
        ...
    def get_instance(self,
        id:int,
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryIscsiExtentQueryResultItem]|QueryIscsiExtentQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        iscsi_extent_update:UpdateIscsiExtentUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update iSCSI Extent of `id`."""
        ...
IscsiExtentCreate = _ty.TypedDict('IscsiExtentCreate', {
    'name': str,
    'type': _ty.NotRequired[str],
    'disk': _ty.NotRequired[str|None],
    'serial': _ty.NotRequired[str|None],
    'path': _ty.NotRequired[str|None],
    'filesize': _ty.NotRequired[str|int],
    'blocksize': _ty.NotRequired[int],
    'pblocksize': _ty.NotRequired[bool],
    'avail_threshold': _ty.NotRequired[int|None],
    'comment': _ty.NotRequired[str],
    'insecure_tpc': _ty.NotRequired[bool],
    'xen': _ty.NotRequired[bool],
    'rpm': _ty.NotRequired[str],
    'ro': _ty.NotRequired[bool],
    'enabled': _ty.NotRequired[bool], 
})
IscsiExtentUpdate = _ty.TypedDict('IscsiExtentUpdate', {
    'name': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'disk': _ty.NotRequired[str|None],
    'serial': _ty.NotRequired[str|None],
    'path': _ty.NotRequired[str|None],
    'filesize': _ty.NotRequired[str|int],
    'blocksize': _ty.NotRequired[int],
    'pblocksize': _ty.NotRequired[bool],
    'avail_threshold': _ty.NotRequired[int|None],
    'comment': _ty.NotRequired[str],
    'insecure_tpc': _ty.NotRequired[bool],
    'xen': _ty.NotRequired[bool],
    'rpm': _ty.NotRequired[str],
    'ro': _ty.NotRequired[bool],
    'enabled': _ty.NotRequired[bool], 
})
CreateIscsiExtentCreate = _ty.TypedDict('CreateIscsiExtentCreate', {
    'name': str,
    'type': _ty.NotRequired[str],
    'disk': _ty.NotRequired[str|None],
    'serial': _ty.NotRequired[str|None],
    'path': _ty.NotRequired[str|None],
    'filesize': _ty.NotRequired[str|int],
    'blocksize': _ty.NotRequired[int],
    'pblocksize': _ty.NotRequired[bool],
    'avail_threshold': _ty.NotRequired[int|None],
    'comment': _ty.NotRequired[str],
    'insecure_tpc': _ty.NotRequired[bool],
    'xen': _ty.NotRequired[bool],
    'rpm': _ty.NotRequired[str],
    'ro': _ty.NotRequired[bool],
    'enabled': _ty.NotRequired[bool], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'name': str,
    'type': _ty.NotRequired[str],
    'disk': _ty.NotRequired[str|None],
    'serial': _ty.NotRequired[str|None],
    'path': _ty.NotRequired[str|None],
    'filesize': _ty.NotRequired[str|int],
    'blocksize': _ty.NotRequired[int],
    'pblocksize': _ty.NotRequired[bool],
    'avail_threshold': _ty.NotRequired[int|None],
    'comment': _ty.NotRequired[str],
    'naa': str,
    'insecure_tpc': _ty.NotRequired[bool],
    'xen': _ty.NotRequired[bool],
    'rpm': _ty.NotRequired[str],
    'ro': _ty.NotRequired[bool],
    'enabled': _ty.NotRequired[bool],
    'vendor': str,
    'locked': bool|None, 
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
    'id': int,
    'name': str,
    'type': _ty.NotRequired[str],
    'disk': _ty.NotRequired[str|None],
    'serial': _ty.NotRequired[str|None],
    'path': _ty.NotRequired[str|None],
    'filesize': _ty.NotRequired[str|int],
    'blocksize': _ty.NotRequired[int],
    'pblocksize': _ty.NotRequired[bool],
    'avail_threshold': _ty.NotRequired[int|None],
    'comment': _ty.NotRequired[str],
    'naa': str,
    'insecure_tpc': _ty.NotRequired[bool],
    'xen': _ty.NotRequired[bool],
    'rpm': _ty.NotRequired[str],
    'ro': _ty.NotRequired[bool],
    'enabled': _ty.NotRequired[bool],
    'vendor': str,
    'locked': bool|None, 
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
QueryIscsiExtentQueryResultItem = _ty.TypedDict('QueryIscsiExtentQueryResultItem', {
    'id': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'disk': _ty.NotRequired[str|None],
    'serial': _ty.NotRequired[str|None],
    'path': _ty.NotRequired[str|None],
    'filesize': _ty.NotRequired[str|int],
    'blocksize': _ty.NotRequired[int],
    'pblocksize': _ty.NotRequired[bool],
    'avail_threshold': _ty.NotRequired[int|None],
    'comment': _ty.NotRequired[str],
    'naa': _ty.NotRequired[str],
    'insecure_tpc': _ty.NotRequired[bool],
    'xen': _ty.NotRequired[bool],
    'rpm': _ty.NotRequired[str],
    'ro': _ty.NotRequired[bool],
    'enabled': _ty.NotRequired[bool],
    'vendor': _ty.NotRequired[str],
    'locked': _ty.NotRequired[bool|None], 
})
UpdateIscsiExtentUpdate = _ty.TypedDict('UpdateIscsiExtentUpdate', {
    'name': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'disk': _ty.NotRequired[str|None],
    'serial': _ty.NotRequired[str|None],
    'path': _ty.NotRequired[str|None],
    'filesize': _ty.NotRequired[str|int],
    'blocksize': _ty.NotRequired[int],
    'pblocksize': _ty.NotRequired[bool],
    'avail_threshold': _ty.NotRequired[int|None],
    'comment': _ty.NotRequired[str],
    'insecure_tpc': _ty.NotRequired[bool],
    'xen': _ty.NotRequired[bool],
    'rpm': _ty.NotRequired[str],
    'ro': _ty.NotRequired[bool],
    'enabled': _ty.NotRequired[bool], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'name': str,
    'type': _ty.NotRequired[str],
    'disk': _ty.NotRequired[str|None],
    'serial': _ty.NotRequired[str|None],
    'path': _ty.NotRequired[str|None],
    'filesize': _ty.NotRequired[str|int],
    'blocksize': _ty.NotRequired[int],
    'pblocksize': _ty.NotRequired[bool],
    'avail_threshold': _ty.NotRequired[int|None],
    'comment': _ty.NotRequired[str],
    'naa': str,
    'insecure_tpc': _ty.NotRequired[bool],
    'xen': _ty.NotRequired[bool],
    'rpm': _ty.NotRequired[str],
    'ro': _ty.NotRequired[bool],
    'enabled': _ty.NotRequired[bool],
    'vendor': str,
    'locked': bool|None, 
})