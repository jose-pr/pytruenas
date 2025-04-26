from pytruenas import Namespace as _NS
import typing as _ty 
class SharingNfs(_NS):
    
    def create(self,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SharingNfsCreate:
        """Create a NFS Share.

`path` local path to be exported.

`aliases` IGNORED, for now.

`networks` is a list of authorized networks that are allowed to access the share having format "network/mask" CIDR notation. If empty, all networks are allowed.

`hosts` is a list of IP's/hostnames which are allowed to access the share. If empty, all IP's/hostnames are allowed.

`expose_snapshots` enable TrueNAS Enterprise feature to allow access to the ZFS snapshot directory over NFS. This feature requires a valid enterprise license."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SharingNfsDelete:
        """Delete NFS Share of `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SharingNfsGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SharingNfsQuery:
        """"""
        ...
    def update(self,
        id,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SharingNfsUpdate:
        """Update NFS Share of `id`."""
        ...
class SharingNfsCreate(_ty.TypedDict):
    ...
class SharingNfsDelete(_ty.TypedDict):
    ...
class SharingNfsGet_instance(_ty.TypedDict):
    ...
class SharingNfsQuery(_ty.TypedDict):
    ...
class SharingNfsUpdate(_ty.TypedDict):
    ... 