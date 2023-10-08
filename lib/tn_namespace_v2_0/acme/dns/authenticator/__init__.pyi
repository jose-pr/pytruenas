
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class AcmeDnsAuthenticator(Namespace):
    _namespace:_ty.Literal['acme.dns.authenticator']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def authenticator_schemas(self, 
    /) -> 'list': 
        """
        Get the schemas for all DNS providers we support for ACME DNS Challenge and the respective attributes
        required for connecting to them while validating a DNS Challenge

        Parameters
        ----------
        Returns
        -------
        list:
            Authenticator Schemas
        """
        ...
    @_ty.overload
    def create(self, 
        acme_dns_authenticator_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a DNS Authenticator
        
        Create a specific DNS Authenticator containing required authentication details for the said
        provider to successfully connect with it

        Parameters
        ----------
        acme_dns_authenticator_create:
            acme_dns_authenticator_create
        Returns
        -------
        dict[str]:
            acme_dns_authenticator_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete DNS Authenticator of `id`

        Parameters
        ----------
        id:
            Delete DNS Authenticator of `id`
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        dns_authenticator_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update DNS Authenticator of `id`

        Parameters
        ----------
        id:
            Update DNS Authenticator of `id`
        dns_authenticator_update:
            dns_authenticator_update
        Returns
        -------
        dict[str]:
            acme_dns_authenticator_update_returns
        """
        ...
