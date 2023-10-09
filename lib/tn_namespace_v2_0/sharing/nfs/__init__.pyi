
from pytruenas import Namespace, TrueNASClient
import typing
class SharingNfs(Namespace):
    _namespace:typing.Literal['sharing.nfs']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        sharingnfs_create:'SharingnfsCreate'={},
    /) -> 'SharingNfsCreateReturns': 
        """
        Create a NFS Share.
        
        `path` local path to be exported.
        
        `aliases` IGNORED, for now.
        
        `networks` is a list of authorized networks that are allowed to access the share having format
        "network/mask" CIDR notation. If empty, all networks are allowed.
        
        `hosts` is a list of IP's/hostnames which are allowed to access the share. If empty, all IP's/hostnames are
        allowed.

        Parameters
        ----------
        sharingnfs_create:
            sharingnfs_create
        Returns
        -------
        SharingNfsCreateReturns:
            sharing_nfs_create_returns
        """
        ...
    SharingnfsCreate = typing.TypedDict('SharingnfsCreate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
    })
    SharingNfsCreateReturns = typing.TypedDict('SharingNfsCreateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
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
    SharingNfsEntry = typing.TypedDict('SharingNfsEntry', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry_ = typing.TypedDict('SharingNfsEntry_', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry__ = typing.TypedDict('SharingNfsEntry__', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingnfsUpdate = typing.TypedDict('SharingnfsUpdate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
    })
    SharingNfsUpdateReturns = typing.TypedDict('SharingNfsUpdateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> None: 
        """
        Delete NFS Share of `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    SharingnfsCreate = typing.TypedDict('SharingnfsCreate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
    })
    SharingNfsCreateReturns = typing.TypedDict('SharingNfsCreateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
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
    SharingNfsEntry = typing.TypedDict('SharingNfsEntry', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry_ = typing.TypedDict('SharingNfsEntry_', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry__ = typing.TypedDict('SharingNfsEntry__', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingnfsUpdate = typing.TypedDict('SharingnfsUpdate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
    })
    SharingNfsUpdateReturns = typing.TypedDict('SharingNfsUpdateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
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
    SharingnfsCreate = typing.TypedDict('SharingnfsCreate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
    })
    SharingNfsCreateReturns = typing.TypedDict('SharingNfsCreateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
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
    SharingNfsEntry = typing.TypedDict('SharingNfsEntry', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry_ = typing.TypedDict('SharingNfsEntry_', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry__ = typing.TypedDict('SharingNfsEntry__', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingnfsUpdate = typing.TypedDict('SharingnfsUpdate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
    })
    SharingNfsUpdateReturns = typing.TypedDict('SharingNfsUpdateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[SharingNfsEntry], ForwardRef(SharingNfsEntry_), int, ForwardRef(SharingNfsEntry__)]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[SharingNfsEntry], ForwardRef(SharingNfsEntry_), int, ForwardRef(SharingNfsEntry__)]:
            
        """
        ...
    SharingnfsCreate = typing.TypedDict('SharingnfsCreate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
    })
    SharingNfsCreateReturns = typing.TypedDict('SharingNfsCreateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
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
    SharingNfsEntry = typing.TypedDict('SharingNfsEntry', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry_ = typing.TypedDict('SharingNfsEntry_', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry__ = typing.TypedDict('SharingNfsEntry__', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingnfsUpdate = typing.TypedDict('SharingnfsUpdate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
    })
    SharingNfsUpdateReturns = typing.TypedDict('SharingNfsUpdateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    @typing.overload
    def update(self, 
        id:'int',
        sharingnfs_update:'SharingnfsUpdate'={},
    /) -> 'SharingNfsUpdateReturns': 
        """
        Update NFS Share of `id`.

        Parameters
        ----------
        id:
            Update NFS Share of `id`.
            Create a NFS Share.
        sharingnfs_update:
            sharingnfs_update
        Returns
        -------
        SharingNfsUpdateReturns:
            sharing_nfs_update_returns
        """
        ...
    SharingnfsCreate = typing.TypedDict('SharingnfsCreate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
    })
    SharingNfsCreateReturns = typing.TypedDict('SharingNfsCreateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
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
    SharingNfsEntry = typing.TypedDict('SharingNfsEntry', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry_ = typing.TypedDict('SharingNfsEntry_', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingNfsEntry__ = typing.TypedDict('SharingNfsEntry__', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
    SharingnfsUpdate = typing.TypedDict('SharingnfsUpdate', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
    })
    SharingNfsUpdateReturns = typing.TypedDict('SharingNfsUpdateReturns', {
            'path':'str',
            'aliases':'list[str]',
            'comment':'str',
            'networks':'list[str]',
            'hosts':'list[str]',
            'ro':'bool',
            'maproot_user':'typing.Optional[str]',
            'maproot_group':'typing.Optional[str]',
            'mapall_user':'typing.Optional[str]',
            'mapall_group':'typing.Optional[str]',
            'security':'list[str]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })

