
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class SharingNfs(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['sharing.nfs']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        _sharingnfs_create:'SharingnfsCreate',
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
    @typing.overload
    def delete(self, 
        _id:'int',
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
    @typing.overload
    def get_instance(self, 
        _id:'typing.Union[str, int, bool, dict[str], list]',
        _query_options_get_instance:'QueryOptionsGetInstance',
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
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list[SharingNfsEntry], SharingNfsEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[SharingNfsEntry], SharingNfsEntry, int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        _id:'int',
        _sharingnfs_update:'SharingnfsUpdate',
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
    class Provider(str,Enum):
        SYS = 'SYS'
        KRB5 = 'KRB5'
        KRB5I = 'KRB5I'
        KRB5P = 'KRB5P'
        ...
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
            'security':'list[Provider]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
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
            'security':'list[Provider]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
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
            'security':'list[Provider]',
            'enabled':'bool',
            'id':'int',
            'locked':'bool',
    })
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
            'security':'list[Provider]',
            'enabled':'bool',
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
            'security':'list[Provider]',
            'enabled':'bool',
    })
