from pytruenas import Namespace as _NS
import typing as _ty 
class IscsiAuth(_NS):
    
    def create(self,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiAuthCreate:
        """Create an iSCSI Authorized Access.

`tag` should be unique among all configured iSCSI Authorized Accesses.

`secret` and `peersecret` should have length between 12-16 letters inclusive.

`peeruser` and `peersecret` are provided only when configuring mutual CHAP. `peersecret` should not be similar to `secret`."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiAuthDelete:
        """Delete iSCSI Authorized Access of `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiAuthGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiAuthQuery:
        """"""
        ...
    def update(self,
        id,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiAuthUpdate:
        """Update iSCSI Authorized Access of `id`."""
        ...
class IscsiAuthCreate(_ty.TypedDict):
    ...
class IscsiAuthDelete(_ty.TypedDict):
    ...
class IscsiAuthGet_instance(_ty.TypedDict):
    ...
class IscsiAuthQuery(_ty.TypedDict):
    ...
class IscsiAuthUpdate(_ty.TypedDict):
    ... 