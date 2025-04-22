from pytruenas import Namespace as _NS 
class AcmeDnsAuthenticator(_NS):
    
    def authenticator_schemas(self,
    ) -> AcmeDnsAuthenticatorAuthenticator_schemas:
        """Get the schemas for all DNS providers we support for ACME DNS Challenge and the respective attributes required for connecting to them while validating a DNS Challenge"""
        ...
    def create(self,
        dns_authenticator_create,
    ) -> AcmeDnsAuthenticatorCreate:
        """Create a DNS Authenticator

Create a specific DNS Authenticator containing required authentication details for the said provider to successfully connect with it"""
        ...
    def delete(self,
        id,
    ) -> AcmeDnsAuthenticatorDelete:
        """Delete DNS Authenticator of `id`"""
        ...
    def get_instance(self,
        id,
        options,
    ) -> AcmeDnsAuthenticatorGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> AcmeDnsAuthenticatorQuery:
        """"""
        ...
    def update(self,
        id,
        dns_authenticator_update,
    ) -> AcmeDnsAuthenticatorUpdate:
        """Update DNS Authenticator of `id`"""
        ...
class AcmeDnsAuthenticatorAuthenticator_schemas:
    ...
class AcmeDnsAuthenticatorCreate:
    ...
class AcmeDnsAuthenticatorDelete:
    ...
class AcmeDnsAuthenticatorGet_instance:
    ...
class AcmeDnsAuthenticatorQuery:
    ...
class AcmeDnsAuthenticatorUpdate:
    ... 