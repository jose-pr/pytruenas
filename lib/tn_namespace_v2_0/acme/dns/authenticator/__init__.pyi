
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class AcmeDnsAuthenticator(
    Namespace
    ):
    _namespace:typing.Literal['acme.dns.authenticator']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def authenticator_schemas(self, 
    /) -> 'list[SchemaEntry]': 
        """
        Get the schemas for all DNS providers we support for ACME DNS Challenge and the respective attributes
        required for connecting to them while validating a DNS Challenge

        Parameters
        ----------
        Returns
        -------
        list[SchemaEntry]:
            Authenticator Schemas
        """
        ...
    @typing.overload
    def create(self, 
        acme_dns_authenticator_create:'AcmeDnsAuthenticatorCreate',
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
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance',
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
        query_filters:'list[list]',
        query_options:'QueryOptions',
    /) -> 'typing.Union[list[AcmeDnsAuthenticatorEntry], AcmeDnsAuthenticatorEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[AcmeDnsAuthenticatorEntry], AcmeDnsAuthenticatorEntry, int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        dns_authenticator_update:'DnsAuthenticatorUpdate',
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
    AcmeDnsAuthenticatorCreate = typing.TypedDict('AcmeDnsAuthenticatorCreate', {
            'authenticator':'Authenticator',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorCreateReturns = typing.TypedDict('AcmeDnsAuthenticatorCreateReturns', {
            'id':'int',
            'authenticator':'Authenticator',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry = typing.TypedDict('AcmeDnsAuthenticatorEntry', {
            'id':'int',
            'authenticator':'Authenticator',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorUpdateReturns = typing.TypedDict('AcmeDnsAuthenticatorUpdateReturns', {
            'id':'int',
            'authenticator':'Authenticator',
            'attributes':'dict[str]',
            'name':'str',
    })
    AttributeSchema = typing.TypedDict('AttributeSchema', {
            '_name_':'str',
            'title':'str',
            '_required_':'bool',
    })
    class Authenticator(str,Enum):
        Cloudflare = 'cloudflare'
        Route53 = 'route53'
        OVH = 'OVH'
        Shell = 'shell'
        ...
    DnsAuthenticatorUpdate = typing.TypedDict('DnsAuthenticatorUpdate', {
            'attributes':'dict[str]',
            'name':'str',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    SchemaEntry = typing.TypedDict('SchemaEntry', {
            'key':'str',
            'schema':'list[AttributeSchema]',
    })
