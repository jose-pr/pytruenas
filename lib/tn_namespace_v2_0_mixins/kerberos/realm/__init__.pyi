
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class KerberosRealm(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['kerberos.realm']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        kerberos_realm_create:'KerberosRealmCreate',
    /) -> 'KerberosRealmCreateReturns': 
        """
        Create a new kerberos realm. This will be automatically populated during the
        domain join process in an Active Directory environment. Kerberos realm names
        are case-sensitive, but convention is to only use upper-case.
        
        Entries for kdc, admin_server, and kpasswd_server are not required.
        If they are unpopulated, then kerberos will use DNS srv records to
        discover the correct servers. The option to hard-code them is provided
        due to AD site discovery. Kerberos has no concept of Active Directory
        sites. This means that middleware performs the site discovery and
        sets the kerberos configuration based on the AD site.

        Parameters
        ----------
        kerberos_realm_create:
            kerberos_realm_create
        Returns
        -------
        KerberosRealmCreateReturns:
            kerberos_realm_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete a kerberos realm by ID.

        Parameters
        ----------
        id:
            id
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
    /) -> 'typing.Union[list[KerberosRealmEntry], KerberosRealmEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[KerberosRealmEntry], KerberosRealmEntry, int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        kerberos_realm_update:'KerberosRealmUpdate',
    /) -> 'KerberosRealmUpdateReturns': 
        """
        Update a kerberos realm by id. This will be automatically populated during the
        domain join process in an Active Directory environment. Kerberos realm names
        are case-sensitive, but convention is to only use upper-case.

        Parameters
        ----------
        id:
            id
        kerberos_realm_update:
            kerberos_realm_update
        Returns
        -------
        KerberosRealmUpdateReturns:
            kerberos_realm_update_returns
        """
        ...
    KerberosRealmCreate = typing.TypedDict('KerberosRealmCreate', {
            'realm':'str',
            'kdc':'list',
            'admin_server':'list',
            'kpasswd_server':'list',
    })
    KerberosRealmCreateReturns = typing.TypedDict('KerberosRealmCreateReturns', {
            'realm':'str',
            'kdc':'list',
            'admin_server':'list',
            'kpasswd_server':'list',
            'id':'int',
    })
    KerberosRealmEntry = typing.TypedDict('KerberosRealmEntry', {
            'realm':'str',
            'kdc':'list',
            'admin_server':'list',
            'kpasswd_server':'list',
            'id':'int',
    })
    KerberosRealmUpdate = typing.TypedDict('KerberosRealmUpdate', {
            'realm':'str',
            'kdc':'list',
            'admin_server':'list',
            'kpasswd_server':'list',
    })
    KerberosRealmUpdateReturns = typing.TypedDict('KerberosRealmUpdateReturns', {
            'realm':'str',
            'kdc':'list',
            'admin_server':'list',
            'kpasswd_server':'list',
            'id':'int',
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
