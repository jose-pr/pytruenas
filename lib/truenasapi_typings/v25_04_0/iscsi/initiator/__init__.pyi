from pytruenas import Namespace as _NS
import typing as _ty 
class IscsiInitiator(_NS):
    
    def create(self,
        iscsi_initiator_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiInitiatorCreate:
        """Create an iSCSI Initiator.

`initiators` is a list of initiator hostnames which are authorized to access an iSCSI Target. To allow all possible initiators, `initiators` can be left empty."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiInitiatorDelete:
        """Delete iSCSI initiator of `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiInitiatorGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiInitiatorQuery:
        """"""
        ...
    def update(self,
        id,
        iscsi_initiator_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiInitiatorUpdate:
        """Update iSCSI initiator of `id`."""
        ...
class IscsiInitiatorCreate(_ty.TypedDict):
    ...
class IscsiInitiatorDelete(_ty.TypedDict):
    ...
class IscsiInitiatorGet_instance(_ty.TypedDict):
    ...
class IscsiInitiatorQuery(_ty.TypedDict):
    ...
class IscsiInitiatorUpdate(_ty.TypedDict):
    ... 