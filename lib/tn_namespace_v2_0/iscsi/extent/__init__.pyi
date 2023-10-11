
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class IscsiExtent(
    Namespace
    ):
    _namespace:typing.Literal['iscsi.extent']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        iscsi_extent_create:'IscsiExtentCreate',
    /) -> 'dict[str]': 
        """
        Create an iSCSI Extent.
        
        When `type` is set to FILE, attribute `filesize` is used and it represents number of bytes. `filesize` if
        not zero should be a multiple of `blocksize`. `path` is a required attribute with `type` set as FILE.
        
        With `type` being set to DISK, a valid ZFS volume is required.
        
        `insecure_tpc` when enabled allows an initiator to bypass normal access control and access any scannable
        target. This allows xcopy operations otherwise blocked by access control.
        
        `xen` is a boolean value which is set to true if Xen is being used as the iSCSI initiator.
        
        `ro` when set to true prevents the initiator from writing to this LUN.

        Parameters
        ----------
        iscsi_extent_create:
            iscsi_extent_create
        Returns
        -------
        dict[str]:
            iscsi_extent_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
        remove:'bool',
        force:'bool',
    /) -> 'bool': 
        """
        Delete iSCSI Extent of `id`.
        
        If `id` iSCSI Extent's `type` was configured to FILE, `remove` can be set to remove the configured file.

        Parameters
        ----------
        id:
            Delete iSCSI Extent of `id`.
        remove:
            remove
        force:
            force
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def disk_choices(self, 
    /) -> None: 
        """
        Return a dict of available zvols that can be used
        when creating an extent.

        Parameters
        ----------
        Returns
        -------
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
    /) -> 'typing.Union[list, dict[str], int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list, dict[str], int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        iscsi_extent_update:'IscsiExtentUpdate',
    /) -> 'dict[str]': 
        """
        Update iSCSI Extent of `id`.

        Parameters
        ----------
        id:
            Update iSCSI Extent of `id`.
            Create an iSCSI Extent.
        iscsi_extent_update:
            iscsi_extent_update
        Returns
        -------
        dict[str]:
            iscsi_extent_update_returns
        """
        ...
    IscsiExtentCreate = typing.TypedDict('IscsiExtentCreate', {
            'name':'str',
            'type':'Type',
            'disk':'typing.Optional[str]',
            'serial':'typing.Optional[str]',
            'path':'typing.Optional[str]',
            'filesize':'int',
            'blocksize':'int',
            'pblocksize':'bool',
            'avail_threshold':'typing.Optional[int]',
            'comment':'str',
            'insecure_tpc':'bool',
            'xen':'bool',
            'rpm':'Rpm',
            'ro':'bool',
            'enabled':'bool',
    })
    class Type(str,Enum):
        DISK = 'DISK'
        FILE = 'FILE'
        ...
    class Rpm(str,Enum):
        UNKNOWN = 'UNKNOWN'
        SSD = 'SSD'
        _5400 = '5400'
        _7200 = '7200'
        _10000 = '10000'
        _15000 = '15000'
        ...
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
    IscsiExtentUpdate = typing.TypedDict('IscsiExtentUpdate', {
            'name':'str',
            'type':'Type',
            'disk':'typing.Optional[str]',
            'serial':'typing.Optional[str]',
            'path':'typing.Optional[str]',
            'filesize':'int',
            'blocksize':'int',
            'pblocksize':'bool',
            'avail_threshold':'typing.Optional[int]',
            'comment':'str',
            'insecure_tpc':'bool',
            'xen':'bool',
            'rpm':'Rpm',
            'ro':'bool',
            'enabled':'bool',
    })
