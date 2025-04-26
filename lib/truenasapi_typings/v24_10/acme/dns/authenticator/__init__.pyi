from pytruenas import Namespace as _NS
import typing as _ty 
class AcmeDnsAuthenticator(_NS):
    
    def authenticator_schemas(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AcmeDnsAuthenticatorAuthenticator_schemas:
        """Get the schemas for all DNS providers we support for ACME DNS Challenge and the respective attributes required for connecting to them while validating a DNS Challenge"""
        ...
    def create(self,
        dns_authenticator_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AcmeDnsAuthenticatorCreate:
        """Create a DNS Authenticator

Create a specific DNS Authenticator containing required authentication details for the said provider to successfully connect with it"""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AcmeDnsAuthenticatorDelete:
        """Delete DNS Authenticator of `id`"""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AcmeDnsAuthenticatorGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AcmeDnsAuthenticatorQuery:
        """"""
        ...
    def update(self,
        id,
        dns_authenticator_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AcmeDnsAuthenticatorUpdate:
        """Update DNS Authenticator of `id`"""
        ...
class AcmeDnsAuthenticatorAuthenticator_schemas(_ty.TypedDict):
    ...
class AcmeDnsAuthenticatorCreate(_ty.TypedDict):
    ...
class AcmeDnsAuthenticatorDelete(_ty.TypedDict):
    ...
class AcmeDnsAuthenticatorGet_instance(_ty.TypedDict):
    ...
class AcmeDnsAuthenticatorQuery(_ty.TypedDict):
    ...
class AcmeDnsAuthenticatorUpdate(_ty.TypedDict):
    ... 