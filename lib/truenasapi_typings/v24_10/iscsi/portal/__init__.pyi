from pytruenas import Namespace as _NS
import typing as _ty 
class IscsiPortal(_NS):
    
    def create(self,
        iscsi_portal_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiPortalCreate:
        """Create a new iSCSI Portal."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiPortalDelete:
        """Delete iSCSI Portal `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiPortalGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def listen_ip_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiPortalListen_ip_choices:
        """Returns possible choices for `listen.ip` attribute of portal create and update."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiPortalQuery:
        """"""
        ...
    def update(self,
        id,
        iscsi_portal_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiPortalUpdate:
        """Update iSCSI Portal `id`."""
        ...
class IscsiPortalCreate(_ty.TypedDict):
    ...
class IscsiPortalDelete(_ty.TypedDict):
    ...
class IscsiPortalGet_instance(_ty.TypedDict):
    ...
class IscsiPortalListen_ip_choices(_ty.TypedDict):
    ...
class IscsiPortalQuery(_ty.TypedDict):
    ...
class IscsiPortalUpdate(_ty.TypedDict):
    ... 