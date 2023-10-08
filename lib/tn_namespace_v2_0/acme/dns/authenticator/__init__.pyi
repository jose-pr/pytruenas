
from pytruenas import Namespace, TrueNASClient
import typing
class AcmeDnsAuthenticator(Namespace):
    _namespace:typing.Literal['acme.dns.authenticator']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def authenticator_schemas(self, 
    /) -> 'list[AuthenticatorSchema]': 
        """
        Get the schemas for all DNS providers we support for ACME DNS Challenge and the respective attributes
        required for connecting to them while validating a DNS Challenge

        Parameters
        ----------
        Returns
        -------
        list[AuthenticatorSchema]:
            Authenticator Schemas
        """
        ...
    @typing.overload
    def create(self, 
        acme_dns_authenticator_create:'AcmeDnsAuthenticatorCreate'={},
    /) -> 'AcmeDnsAuthenticatorCreateReturns': 
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
        AcmeDnsAuthenticatorCreateReturns:
            acme_dns_authenticator_create_returns
        """
        ...
    @typing.overload
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
    @typing.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'QueryOptionsGetInstance'={},
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
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[AcmeDnsAuthenticatorEntry]|AcmeDnsAuthenticatorEntry|int|AcmeDnsAuthenticatorEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[AcmeDnsAuthenticatorEntry]:
            
        AcmeDnsAuthenticatorEntry:
            
        int:
            
        AcmeDnsAuthenticatorEntry:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        dns_authenticator_update:'DnsAuthenticatorUpdate'={},
    /) -> 'AcmeDnsAuthenticatorUpdateReturns': 
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
        AcmeDnsAuthenticatorUpdateReturns:
            acme_dns_authenticator_update_returns
        """
        ...

class AuthenticatorSchema(typing.TypedDict):
        key:'str'
        schema:'list[AttributeSchema]'
        ...
class AttributeSchema(typing.TypedDict):
        _name_:'str'
        title:'str'
        _required_:'bool'
        ...
class AcmeDnsAuthenticatorCreate(typing.TypedDict):
        authenticator:'str'
        attributes:'dict[str]'
        name:'str'
        ...
class AcmeDnsAuthenticatorCreateReturns(typing.TypedDict):
        id:'int'
        authenticator:'str'
        attributes:'dict[str]'
        name:'str'
        ...
class QueryOptionsGetInstance(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class AcmeDnsAuthenticatorEntry(typing.TypedDict):
        id:'int'
        authenticator:'str'
        attributes:'dict[str]'
        name:'str'
        ...
class DnsAuthenticatorUpdate(typing.TypedDict):
        attributes:'dict[str]'
        name:'str'
        ...
class AcmeDnsAuthenticatorUpdateReturns(typing.TypedDict):
        id:'int'
        authenticator:'str'
        attributes:'dict[str]'
        name:'str'
        ...
