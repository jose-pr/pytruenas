from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class IscsiTarget(_NS):
    
    def create(self,
        iscsi_target_create:iscsi_target_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetCreate:
        """Create an iSCSI Target.

`groups` is a list of group dictionaries which provide information related to using a `portal`, `initiator`, `authmethod` and `auth` with this target. `auth` represents a valid iSCSI Authorized Access and defaults to null.

`auth_networks` is a list of IP/CIDR addresses which are allowed to use this initiator. If all networks are to be allowed, this field should be left empty."""
        ...
    def delete(self,
        id:int,
        force:bool=False,
        delete_extents:bool=False,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete iSCSI Target of `id`.

Deleting an iSCSI Target makes sure we delete all Associated Targets which use `id` iSCSI Target."""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[IscsiTargetQueryResultItem]|IscsiTargetQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        iscsi_target_update:iscsi_target_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetUpdate:
        """Update iSCSI Target of `id`."""
        ...
    def validate_name(self,
        name:str,
        existing_id:int|None=None,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str|None:
        """Returns validation error for iSCSI target name :param name: name to be validated :param existing_id: id of an existing iSCSI target that will receive this name (or `None` if a new target is being created) :return: error message (or `None` if there is no error)"""
        ...
iscsi_target_create = _ty.TypedDict('iscsi_target_create', {
    'name': str,
    'alias': _ty.NotRequired[str|None],
    'mode': _ty.NotRequired[str],
    'groups': _ty.NotRequired[_jsonschema.JsonArray],
    'auth_networks': _ty.NotRequired[list[str]],
    'iscsi_parameters': _ty.NotRequired[_jsonschema.JsonValue|None], 
})
IscsiTargetCreate = _ty.TypedDict('IscsiTargetCreate', {
    'id': int,
    'name': str,
    'alias': _ty.NotRequired[str|None],
    'mode': _ty.NotRequired[str],
    'groups': _ty.NotRequired[_jsonschema.JsonArray],
    'auth_networks': _ty.NotRequired[list[str]],
    'rel_tgt_id': int,
    'iscsi_parameters': _ty.NotRequired[_jsonschema.JsonValue|None], 
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
IscsiTargetGet_instance = _ty.TypedDict('IscsiTargetGet_instance', {
    'id': int,
    'name': str,
    'alias': _ty.NotRequired[str|None],
    'mode': _ty.NotRequired[str],
    'groups': _ty.NotRequired[_jsonschema.JsonArray],
    'auth_networks': _ty.NotRequired[list[str]],
    'rel_tgt_id': int,
    'iscsi_parameters': _ty.NotRequired[_jsonschema.JsonValue|None], 
})
IscsiTargetQueryResultItem = _ty.TypedDict('IscsiTargetQueryResultItem', {
    'id': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'alias': _ty.NotRequired[str|None],
    'mode': _ty.NotRequired[str],
    'groups': _ty.NotRequired[_jsonschema.JsonArray],
    'auth_networks': _ty.NotRequired[list[str]],
    'rel_tgt_id': _ty.NotRequired[int],
    'iscsi_parameters': _ty.NotRequired[_jsonschema.JsonValue|None], 
})
iscsi_target_update = _ty.TypedDict('iscsi_target_update', {
    'name': _ty.NotRequired[str],
    'alias': _ty.NotRequired[str|None],
    'mode': _ty.NotRequired[str],
    'groups': _ty.NotRequired[_jsonschema.JsonArray],
    'auth_networks': _ty.NotRequired[list[str]],
    'iscsi_parameters': _ty.NotRequired[_jsonschema.JsonValue|None], 
})
IscsiTargetUpdate = _ty.TypedDict('IscsiTargetUpdate', {
    'id': int,
    'name': str,
    'alias': _ty.NotRequired[str|None],
    'mode': _ty.NotRequired[str],
    'groups': _ty.NotRequired[_jsonschema.JsonArray],
    'auth_networks': _ty.NotRequired[list[str]],
    'rel_tgt_id': int,
    'iscsi_parameters': _ty.NotRequired[_jsonschema.JsonValue|None], 
})