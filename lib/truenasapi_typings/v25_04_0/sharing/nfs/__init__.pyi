from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Nfs(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[Data],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[Data],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[Data],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        data:CreateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Create a NFS Share.

`path` local path to be exported.

`aliases` IGNORED, for now.

`networks` is a list of authorized networks that are allowed to access the share having format "network/mask" CIDR notation. If empty, all networks are allowed.

`hosts` is a list of IP's/hostnames which are allowed to access the share. If empty, all IP's/hostnames are allowed.

`expose_snapshots` enable TrueNAS Enterprise feature to allow access to the ZFS snapshot directory over NFS. This feature requires a valid enterprise license."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete NFS Share of `id`."""
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
    ) -> list[QueryNfsShareQueryResultItem]|QueryNfsShareQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        data:UpdateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update NFS Share of `id`."""
        ...
Data = _ty.TypedDict('Data', {
    'path': _ty.NotRequired[str],
    'aliases': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str],
    'networks': _ty.NotRequired[list[str]],
    'hosts': _ty.NotRequired[list[str]],
    'ro': _ty.NotRequired[bool],
    'maproot_user': _ty.NotRequired[str|None],
    'maproot_group': _ty.NotRequired[str|None],
    'mapall_user': _ty.NotRequired[str|None],
    'mapall_group': _ty.NotRequired[str|None],
    'security': _ty.NotRequired[list[str]],
    'enabled': _ty.NotRequired[bool],
    'expose_snapshots': _ty.NotRequired[bool], 
})
CreateData = _ty.TypedDict('CreateData', {
    'path': str,
    'aliases': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str],
    'networks': _ty.NotRequired[list[str]],
    'hosts': _ty.NotRequired[list[str]],
    'ro': _ty.NotRequired[bool],
    'maproot_user': _ty.NotRequired[str|None],
    'maproot_group': _ty.NotRequired[str|None],
    'mapall_user': _ty.NotRequired[str|None],
    'mapall_group': _ty.NotRequired[str|None],
    'security': _ty.NotRequired[list[str]],
    'enabled': _ty.NotRequired[bool],
    'expose_snapshots': _ty.NotRequired[bool], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'path': str,
    'aliases': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str],
    'networks': _ty.NotRequired[list[str]],
    'hosts': _ty.NotRequired[list[str]],
    'ro': _ty.NotRequired[bool],
    'maproot_user': _ty.NotRequired[str|None],
    'maproot_group': _ty.NotRequired[str|None],
    'mapall_user': _ty.NotRequired[str|None],
    'mapall_group': _ty.NotRequired[str|None],
    'security': _ty.NotRequired[list[str]],
    'enabled': _ty.NotRequired[bool],
    'locked': bool|None,
    'expose_snapshots': _ty.NotRequired[bool], 
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
    'path': str,
    'aliases': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str],
    'networks': _ty.NotRequired[list[str]],
    'hosts': _ty.NotRequired[list[str]],
    'ro': _ty.NotRequired[bool],
    'maproot_user': _ty.NotRequired[str|None],
    'maproot_group': _ty.NotRequired[str|None],
    'mapall_user': _ty.NotRequired[str|None],
    'mapall_group': _ty.NotRequired[str|None],
    'security': _ty.NotRequired[list[str]],
    'enabled': _ty.NotRequired[bool],
    'locked': bool|None,
    'expose_snapshots': _ty.NotRequired[bool], 
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
QueryNfsShareQueryResultItem = _ty.TypedDict('QueryNfsShareQueryResultItem', {
    'id': _ty.NotRequired[int],
    'path': _ty.NotRequired[str],
    'aliases': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str],
    'networks': _ty.NotRequired[list[str]],
    'hosts': _ty.NotRequired[list[str]],
    'ro': _ty.NotRequired[bool],
    'maproot_user': _ty.NotRequired[str|None],
    'maproot_group': _ty.NotRequired[str|None],
    'mapall_user': _ty.NotRequired[str|None],
    'mapall_group': _ty.NotRequired[str|None],
    'security': _ty.NotRequired[list[str]],
    'enabled': _ty.NotRequired[bool],
    'locked': _ty.NotRequired[bool|None],
    'expose_snapshots': _ty.NotRequired[bool], 
})
UpdateData = _ty.TypedDict('UpdateData', {
    'path': _ty.NotRequired[str],
    'aliases': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str],
    'networks': _ty.NotRequired[list[str]],
    'hosts': _ty.NotRequired[list[str]],
    'ro': _ty.NotRequired[bool],
    'maproot_user': _ty.NotRequired[str|None],
    'maproot_group': _ty.NotRequired[str|None],
    'mapall_user': _ty.NotRequired[str|None],
    'mapall_group': _ty.NotRequired[str|None],
    'security': _ty.NotRequired[list[str]],
    'enabled': _ty.NotRequired[bool],
    'expose_snapshots': _ty.NotRequired[bool], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'path': str,
    'aliases': _ty.NotRequired[list[str]],
    'comment': _ty.NotRequired[str],
    'networks': _ty.NotRequired[list[str]],
    'hosts': _ty.NotRequired[list[str]],
    'ro': _ty.NotRequired[bool],
    'maproot_user': _ty.NotRequired[str|None],
    'maproot_group': _ty.NotRequired[str|None],
    'mapall_user': _ty.NotRequired[str|None],
    'mapall_group': _ty.NotRequired[str|None],
    'security': _ty.NotRequired[list[str]],
    'enabled': _ty.NotRequired[bool],
    'locked': bool|None,
    'expose_snapshots': _ty.NotRequired[bool], 
})