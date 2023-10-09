
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
    AttributeSchema = typing.TypedDict('AttributeSchema', {
            '_name_':'str',
            'title':'str',
            '_required_':'bool',
    })
    AuthenticatorSchema = typing.TypedDict('AuthenticatorSchema', {
            'key':'str',
            'schema':'list[AttributeSchema]',
    })
    AcmeDnsAuthenticatorCreate = typing.TypedDict('AcmeDnsAuthenticatorCreate', {
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorCreateReturns = typing.TypedDict('AcmeDnsAuthenticatorCreateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
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
    AcmeDnsAuthenticatorEntry = typing.TypedDict('AcmeDnsAuthenticatorEntry', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry_ = typing.TypedDict('AcmeDnsAuthenticatorEntry_', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry__ = typing.TypedDict('AcmeDnsAuthenticatorEntry__', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    DnsAuthenticatorUpdate = typing.TypedDict('DnsAuthenticatorUpdate', {
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorUpdateReturns = typing.TypedDict('AcmeDnsAuthenticatorUpdateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
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
    AttributeSchema = typing.TypedDict('AttributeSchema', {
            '_name_':'str',
            'title':'str',
            '_required_':'bool',
    })
    AuthenticatorSchema = typing.TypedDict('AuthenticatorSchema', {
            'key':'str',
            'schema':'list[AttributeSchema]',
    })
    AcmeDnsAuthenticatorCreate = typing.TypedDict('AcmeDnsAuthenticatorCreate', {
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorCreateReturns = typing.TypedDict('AcmeDnsAuthenticatorCreateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
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
    AcmeDnsAuthenticatorEntry = typing.TypedDict('AcmeDnsAuthenticatorEntry', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry_ = typing.TypedDict('AcmeDnsAuthenticatorEntry_', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry__ = typing.TypedDict('AcmeDnsAuthenticatorEntry__', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    DnsAuthenticatorUpdate = typing.TypedDict('DnsAuthenticatorUpdate', {
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorUpdateReturns = typing.TypedDict('AcmeDnsAuthenticatorUpdateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
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
    AttributeSchema = typing.TypedDict('AttributeSchema', {
            '_name_':'str',
            'title':'str',
            '_required_':'bool',
    })
    AuthenticatorSchema = typing.TypedDict('AuthenticatorSchema', {
            'key':'str',
            'schema':'list[AttributeSchema]',
    })
    AcmeDnsAuthenticatorCreate = typing.TypedDict('AcmeDnsAuthenticatorCreate', {
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorCreateReturns = typing.TypedDict('AcmeDnsAuthenticatorCreateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
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
    AcmeDnsAuthenticatorEntry = typing.TypedDict('AcmeDnsAuthenticatorEntry', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry_ = typing.TypedDict('AcmeDnsAuthenticatorEntry_', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry__ = typing.TypedDict('AcmeDnsAuthenticatorEntry__', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    DnsAuthenticatorUpdate = typing.TypedDict('DnsAuthenticatorUpdate', {
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorUpdateReturns = typing.TypedDict('AcmeDnsAuthenticatorUpdateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
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
    AttributeSchema = typing.TypedDict('AttributeSchema', {
            '_name_':'str',
            'title':'str',
            '_required_':'bool',
    })
    AuthenticatorSchema = typing.TypedDict('AuthenticatorSchema', {
            'key':'str',
            'schema':'list[AttributeSchema]',
    })
    AcmeDnsAuthenticatorCreate = typing.TypedDict('AcmeDnsAuthenticatorCreate', {
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorCreateReturns = typing.TypedDict('AcmeDnsAuthenticatorCreateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
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
    AcmeDnsAuthenticatorEntry = typing.TypedDict('AcmeDnsAuthenticatorEntry', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry_ = typing.TypedDict('AcmeDnsAuthenticatorEntry_', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry__ = typing.TypedDict('AcmeDnsAuthenticatorEntry__', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    DnsAuthenticatorUpdate = typing.TypedDict('DnsAuthenticatorUpdate', {
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorUpdateReturns = typing.TypedDict('AcmeDnsAuthenticatorUpdateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[AcmeDnsAuthenticatorEntry], ForwardRef(AcmeDnsAuthenticatorEntry_), int, ForwardRef(AcmeDnsAuthenticatorEntry__)]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[AcmeDnsAuthenticatorEntry], ForwardRef(AcmeDnsAuthenticatorEntry_), int, ForwardRef(AcmeDnsAuthenticatorEntry__)]:
            
        """
        ...
    AttributeSchema = typing.TypedDict('AttributeSchema', {
            '_name_':'str',
            'title':'str',
            '_required_':'bool',
    })
    AuthenticatorSchema = typing.TypedDict('AuthenticatorSchema', {
            'key':'str',
            'schema':'list[AttributeSchema]',
    })
    AcmeDnsAuthenticatorCreate = typing.TypedDict('AcmeDnsAuthenticatorCreate', {
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorCreateReturns = typing.TypedDict('AcmeDnsAuthenticatorCreateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
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
    AcmeDnsAuthenticatorEntry = typing.TypedDict('AcmeDnsAuthenticatorEntry', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry_ = typing.TypedDict('AcmeDnsAuthenticatorEntry_', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry__ = typing.TypedDict('AcmeDnsAuthenticatorEntry__', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    DnsAuthenticatorUpdate = typing.TypedDict('DnsAuthenticatorUpdate', {
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorUpdateReturns = typing.TypedDict('AcmeDnsAuthenticatorUpdateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
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
    AttributeSchema = typing.TypedDict('AttributeSchema', {
            '_name_':'str',
            'title':'str',
            '_required_':'bool',
    })
    AuthenticatorSchema = typing.TypedDict('AuthenticatorSchema', {
            'key':'str',
            'schema':'list[AttributeSchema]',
    })
    AcmeDnsAuthenticatorCreate = typing.TypedDict('AcmeDnsAuthenticatorCreate', {
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorCreateReturns = typing.TypedDict('AcmeDnsAuthenticatorCreateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
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
    AcmeDnsAuthenticatorEntry = typing.TypedDict('AcmeDnsAuthenticatorEntry', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry_ = typing.TypedDict('AcmeDnsAuthenticatorEntry_', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorEntry__ = typing.TypedDict('AcmeDnsAuthenticatorEntry__', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })
    DnsAuthenticatorUpdate = typing.TypedDict('DnsAuthenticatorUpdate', {
            'attributes':'dict[str]',
            'name':'str',
    })
    AcmeDnsAuthenticatorUpdateReturns = typing.TypedDict('AcmeDnsAuthenticatorUpdateReturns', {
            'id':'int',
            'authenticator':'str',
            'attributes':'dict[str]',
            'name':'str',
    })

