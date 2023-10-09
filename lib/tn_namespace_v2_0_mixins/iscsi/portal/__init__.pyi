
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class IscsiPortal(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['iscsi.portal']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        iscsiportal_create:'IscsiportalCreate'={},
    /) -> 'dict[str]': 
        """
        Create a new iSCSI Portal.
        
        `discovery_authgroup` is required for CHAP and CHAP_MUTUAL.

        Parameters
        ----------
        iscsiportal_create:
            iscsiportal_create
        Returns
        -------
        dict[str]:
            iscsi_portal_create_returns
        """
        ...
    Listen = typing.TypedDict('Listen', {
            'ip':'str',
    })
    IscsiportalCreate = typing.TypedDict('IscsiportalCreate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
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
    IscsiportalUpdate = typing.TypedDict('IscsiportalUpdate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
    })
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete iSCSI Portal `id`.

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
    Listen = typing.TypedDict('Listen', {
            'ip':'str',
    })
    IscsiportalCreate = typing.TypedDict('IscsiportalCreate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
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
    IscsiportalUpdate = typing.TypedDict('IscsiportalUpdate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
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
    Listen = typing.TypedDict('Listen', {
            'ip':'str',
    })
    IscsiportalCreate = typing.TypedDict('IscsiportalCreate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
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
    IscsiportalUpdate = typing.TypedDict('IscsiportalUpdate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
    })
    @typing.overload
    def listen_ip_choices(self, 
    /) -> None: 
        """
        Returns possible choices for `listen.ip` attribute of portal create and update.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    Listen = typing.TypedDict('Listen', {
            'ip':'str',
    })
    IscsiportalCreate = typing.TypedDict('IscsiportalCreate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
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
    IscsiportalUpdate = typing.TypedDict('IscsiportalUpdate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[dict[str]], dict[str], int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[dict[str]], dict[str], int]:
            
        """
        ...
    Listen = typing.TypedDict('Listen', {
            'ip':'str',
    })
    IscsiportalCreate = typing.TypedDict('IscsiportalCreate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
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
    IscsiportalUpdate = typing.TypedDict('IscsiportalUpdate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
    })
    @typing.overload
    def update(self, 
        id:'int',
        iscsiportal_update:'IscsiportalUpdate'={},
    /) -> 'dict[str]': 
        """
        Update iSCSI Portal `id`.

        Parameters
        ----------
        id:
            Update iSCSI Portal `id`.
            Create a new iSCSI Portal.
        iscsiportal_update:
            iscsiportal_update
        Returns
        -------
        dict[str]:
            iscsi_portal_update_returns
        """
        ...
    Listen = typing.TypedDict('Listen', {
            'ip':'str',
    })
    IscsiportalCreate = typing.TypedDict('IscsiportalCreate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
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
    IscsiportalUpdate = typing.TypedDict('IscsiportalUpdate', {
            'comment':'str',
            'discovery_authmethod':'str',
            'discovery_authgroup':'typing.Optional[int]',
            'listen':'list[Listen]',
    })
