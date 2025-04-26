from pytruenas import Namespace as _NS
import typing as _ty 
class IscsiTarget(_NS):
    
    def create(self,
        iscsi_target_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetCreate:
        """Create an iSCSI Target.

`groups` is a list of group dictionaries which provide information related to using a `portal`, `initiator`, `authmethod` and `auth` with this target. `auth` represents a valid iSCSI Authorized Access and defaults to null.

`auth_networks` is a list of IP/CIDR addresses which are allowed to use this initiator. If all networks are to be allowed, this field should be left empty."""
        ...
    def delete(self,
        id,
        force,
        delete_extents,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetDelete:
        """Delete iSCSI Target of `id`.

Deleting an iSCSI Target makes sure we delete all Associated Targets which use `id` iSCSI Target."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetQuery:
        """"""
        ...
    def update(self,
        id,
        iscsi_target_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetUpdate:
        """Update iSCSI Target of `id`."""
        ...
    def validate_name(self,
        name,
        existing_id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiTargetValidate_name:
        """Returns validation error for iSCSI target name :param name: name to be validated :param existing_id: id of an existing iSCSI target that will receive this name (or `None` if a new target is being created) :return: error message (or `None` if there is no error)"""
        ...
class IscsiTargetCreate(_ty.TypedDict):
    ...
class IscsiTargetDelete(_ty.TypedDict):
    ...
class IscsiTargetGet_instance(_ty.TypedDict):
    ...
class IscsiTargetQuery(_ty.TypedDict):
    ...
class IscsiTargetUpdate(_ty.TypedDict):
    ...
class IscsiTargetValidate_name(_ty.TypedDict):
    ... 