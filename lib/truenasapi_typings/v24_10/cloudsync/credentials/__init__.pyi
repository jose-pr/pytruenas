from pytruenas import Namespace as _NS
import typing as _ty 
class CloudsyncCredentials(_NS):
    
    def create(self,
        cloud_sync_credentials_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncCredentialsCreate:
        """Create Cloud Sync Credentials.

`attributes` is a dictionary of valid values which will be used to authorize with the `provider`."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncCredentialsDelete:
        """Delete Cloud Sync Credentials of `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncCredentialsGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncCredentialsQuery:
        """"""
        ...
    def update(self,
        id,
        cloud_sync_credentials_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncCredentialsUpdate:
        """Update Cloud Sync Credentials of `id`."""
        ...
    def verify(self,
        cloud_sync_credentials_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncCredentialsVerify:
        """Verify if `attributes` provided for `provider` are authorized by the `provider`."""
        ...
class CloudsyncCredentialsCreate(_ty.TypedDict):
    ...
class CloudsyncCredentialsDelete(_ty.TypedDict):
    ...
class CloudsyncCredentialsGet_instance(_ty.TypedDict):
    ...
class CloudsyncCredentialsQuery(_ty.TypedDict):
    ...
class CloudsyncCredentialsUpdate(_ty.TypedDict):
    ...
class CloudsyncCredentialsVerify(_ty.TypedDict):
    ... 