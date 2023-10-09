
from pytruenas import TrueNASClient
from pytruenas.base import Namespace

import typing
class GlusterVolume(
    Namespace
    ):
    _namespace:typing.Literal['gluster.volume']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        glustervolume_create:'GlustervolumeCreate'={},
    /) -> 'GlusterVolumeCreateReturns': 
        """
        Create a gluster volume.
        
        `name` String representing name to be given to the volume
        `bricks` List representing the brick paths
            `peer_name` String representing IP or DNS name of the peer
            `peer_path` String representing the full path of the brick
        
        `replica` Integer representing number of replica bricks
        `arbiter` Integer representing number of arbiter bricks
        `disperse` Integer representing number of disperse bricks
        `disperse_data` Integer representing number of disperse data bricks
        `redundancy` Integer representing number of redundancy bricks
        `force` Boolean, if True ignore potential warnings
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        glustervolume_create:
            glustervolume_create
        Returns
        -------
        GlusterVolumeCreateReturns:
            gluster_volume_create_returns
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def delete(self, 
        id:'str',
    /) -> None: 
        """
        Delete a gluster volume.
        
        `id` String representing name of gluster volume
                to be deleted
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        id:
            `id` String representing name of gluster volume
                    to be deleted
        Returns
        -------
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
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
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def info(self, 
        volume_info:'VolumeInfo'={},
    /) -> 'list[Volume]': 
        """
        Return information about gluster volume(s).
        
        `name` String representing name of gluster volume

        Parameters
        ----------
        volume_info:
            volume_info
        Returns
        -------
        list[Volume]:
            volumes
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def list(self, 
    /) -> 'list[str]': 
        """
        Return list of gluster volumes.

        Parameters
        ----------
        Returns
        -------
        list[str]:
            volumes
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def optreset(self, 
        volume_optreset:'VolumeOptreset'={},
    /) -> None: 
        """
        Reset volumes options.
            If `opt` is not provided, then all options
            will be reset.
        
        `name` String representing name of gluster volume
        `opt` String representing name of the option to reset
        `force` Boolean, if True forcefully reset option(s)

        Parameters
        ----------
        volume_optreset:
            volume_optreset
        Returns
        -------
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def optset(self, 
        volume_optset:'VolumeOptset'={},
    /) -> None: 
        """
        Set gluster volume options.
        
        `name` String representing name of gluster volume
        `opts` Dict where
            --key-- is the name of the option
            --value-- is the value to be given to the option
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        volume_optset:
            volume_optset
        Returns
        -------
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[GlusterVolumeEntry], ForwardRef(GlusterVolumeEntry), int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[GlusterVolumeEntry], ForwardRef(GlusterVolumeEntry), int]:
            
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def quota(self, 
        volume_quota:'VolumeQuota'={},
    /) -> None: 
        """
        Enable/Disable the quota for a given gluster volume.
        
        `name` String representing name of gluster volume
        `enable` Boolean, if True enable quota else disable it
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        volume_quota:
            volume_quota
        Returns
        -------
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def restart(self, 
        volume_restart:'VolumeRestart'={},
    /) -> None: 
        """
        Restart a gluster volume.
        
        `name` String representing name of gluster volume
        `force` Boolean, if True forcefully restart the gluster volume

        Parameters
        ----------
        volume_restart:
            volume_restart
        Returns
        -------
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def start(self, 
        volume_start:'VolumeStart'={},
    /) -> None: 
        """
        Start a gluster volume.
        
        `name` String representing name of gluster volume
        `force` Boolean, if True forcefully start the gluster volume
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        volume_start:
            volume_start
        Returns
        -------
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def status(self, 
        volume_status:'VolumeStatus'={},
    /) -> 'list[GlusterVolumeEntry]': 
        """
        Return detailed information about gluster volume.
        
        `name` String representing name of gluster volume
        `verbose` Boolean, If False, only return brick information

        Parameters
        ----------
        volume_status:
            volume_status
        Returns
        -------
        list[GlusterVolumeEntry]:
            volumes
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })
    @typing.overload
    def stop(self, 
        volume_stop:'VolumeStop'={},
    /) -> None: 
        """
        Stop a gluster volume.
        
        `name` String representing name of gluster volume
        `force` Boolean, if True forcefully stop the gluster volume
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        volume_stop:
            volume_stop
        Returns
        -------
        """
        ...
    Brick = typing.TypedDict('Brick', {
            'peer_name':'str',
            'peer_path':'str',
    })
    GlustervolumeCreate = typing.TypedDict('GlustervolumeCreate', {
            'name':'str',
            'bricks':'list[Brick]',
            'replica':'int',
            'arbiter':'int',
            'disperse':'int',
            'disperse_data':'int',
            'redundancy':'int',
            'force':'bool',
    })
    Ports = typing.TypedDict('Ports', {
            'tcp':'str',
            'rdma':'str',
    })
    GlusterVolumeCreateReturns = typing.TypedDict('GlusterVolumeCreateReturns', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
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
    VolumeInfo = typing.TypedDict('VolumeInfo', {
            'name':'str',
    })
    Volume = typing.TypedDict('Volume', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'status':'str',
            'num_bricks':'int',
            'distribute':'int',
            'stripe':'int',
            'replica':'int',
            'disperse':'int',
            'disperse_redundancy':'int',
            'transport':'int',
            'snapshot_count':'int',
            'bricks':'list',
            'options':'list',
    })
    VolumeOptreset = typing.TypedDict('VolumeOptreset', {
            'name':'str',
            'opt':'str',
            'force':'bool',
    })
    VolumeOptset = typing.TypedDict('VolumeOptset', {
            'name':'str',
            'opts':'dict[str]',
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
    GlusterVolumeEntry = typing.TypedDict('GlusterVolumeEntry', {
            'name':'str',
            'uuid':'str',
            'type':'str',
            'online':'bool',
            'ports':'Ports',
            'pid':'str',
            'size_total':'int',
            'size_free':'int',
            'size_used':'int',
            'inodes_total':'int',
            'inodes_free':'int',
            'inodes_used':'int',
            'device':'str',
            'block_size':'str',
            'mnt_options':'str',
            'fs_name':'str',
    })
    VolumeQuota = typing.TypedDict('VolumeQuota', {
            'name':'str',
            'enable':'bool',
    })
    VolumeRestart = typing.TypedDict('VolumeRestart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStart = typing.TypedDict('VolumeStart', {
            'name':'str',
            'force':'bool',
    })
    VolumeStatus = typing.TypedDict('VolumeStatus', {
            'name':'str',
            'verbose':'bool',
    })
    VolumeStop = typing.TypedDict('VolumeStop', {
            'name':'str',
            'force':'bool',
    })

