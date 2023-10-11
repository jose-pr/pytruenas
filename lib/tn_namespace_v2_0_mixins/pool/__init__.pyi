
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class Pool(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['pool']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def attach(self, 
        oid:'int',
        pool_attach:'PoolAttach',
    /) -> None: 
        """
        `target_vdev` is the GUID of the vdev where the disk needs to be attached. In case of STRIPED vdev, this
        is the STRIPED disk GUID which will be converted to mirror. If `target_vdev` is mirror, it will be converted
        into a n-way mirror.

        Parameters
        ----------
        oid:
            oid
        pool_attach:
            pool_attach
        Returns
        -------
        """
        ...
    @typing.overload
    def attachments(self, 
        id:'int',
    /) -> 'list[Attachment]': 
        """
        Return a list of services dependent of this pool.
        
        Responsible for telling the user whether there is a related
        share, asking for confirmation.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        list[Attachment]:
            attachments
        """
        ...
    @typing.overload
    def create(self, 
        pool_create:'PoolCreate',
    /) -> 'PoolCreateReturns': 
        """
        Create a new ZFS Pool.
        
        `topology` is a object which requires at least one `data` entry.
        All of `data` entries (vdevs) require to be of the same type.
        
        `deduplication` when set to ON or VERIFY makes sure that no block of data is duplicated in the pool. When
        VERIFY is specified, if two blocks have similar signatures, byte to byte comparison is performed to ensure that
        the blocks are identical. This should be used in special circumstances as it carries a significant overhead.
        
        `encryption` when enabled will create an ZFS encrypted root dataset for `name` pool.
        
        `encryption_options` specifies configuration for encryption of root dataset for `name` pool.
        `encryption_options.passphrase` must be specified if encryption for root dataset is desired with a passphrase
        as a key.
        Otherwise a hex encoded key can be specified by providing `encryption_options.key`.
        `encryption_options.generate_key` when enabled automatically generates the key to be used
        for dataset encryption.
        
        It should be noted that keys are stored by the system for automatic locking/unlocking
        on import/export of encrypted datasets. If that is not desired, dataset should be created
        with a passphrase as a key.
        
        Example of `topology`:
        
            {
                "data": [
                    {"type": "RAIDZ1", "disks": ["da1", "da2", "da3"]}
                ],
                "cache": [
                    {"type": "STRIPE", "disks": ["da4"]}
                ],
                "log": [
                    {"type": "STRIPE", "disks": ["da5"]}
                ],
                "spares": ["da6"]
            }

        Parameters
        ----------
        pool_create:
            pool_create
        Returns
        -------
        PoolCreateReturns:
            pool_create_returns
        """
        ...
    @typing.overload
    def detach(self, 
        id:'int',
        options:'Options',
    /) -> 'bool': 
        """
        Detach a disk from pool of id `id`.
        
        `label` is the vdev guid or device name.

        Parameters
        ----------
        id:
            Detach a disk from pool of id `id`.
        options:
            options
        Returns
        -------
        bool:
            detached
        """
        ...
    @typing.overload
    def expand(self, 
        id:'int',
    /) -> None: 
        """
        Expand pool to fit all available disk space.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @typing.overload
    def export(self, 
        id:'int',
        options:'Options_',
    /) -> None: 
        """
        Export pool of `id`.
        
        `cascade` will delete all attachments of the given pool (`pool.attachments`).
        `restart_services` will restart services that have open files on given pool.
        `destroy` will also PERMANENTLY destroy the pool/data.

        Parameters
        ----------
        id:
            Export pool of `id`.
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def filesystem_choices(self, 
        types:'list[Type____]',
    /) -> 'list[str]': 
        """
        Returns all available datasets, except the following:
            1. system datasets
            2. glusterfs datasets
            3. application(s) internal datasets

        Parameters
        ----------
        types:
            types
        Returns
        -------
        list[str]:
            filesystem_choices
        """
        ...
    @typing.overload
    def get_disks(self, 
        id:'typing.Optional[int]',
    /) -> 'list[str]': 
        """
        Get all disks in use by pools.
        If `id` is provided only the disks from the given pool `id` will be returned.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        list[str]:
            pool_disks
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
    def get_instance_by_name(self, 
        name:'str',
    /) -> 'PoolEntry': 
        """
        Returns pool with name `name`. If `name` is not found, Validation error is raised.

        Parameters
        ----------
        name:
            name
        Returns
        -------
        PoolEntry:
            pool_entry
        """
        ...
    @typing.overload
    def import_find(self, 
    /) -> 'list[PoolInfo]': 
        """
        Returns a job id which can be used to retrieve a list of pools available for
        import with the following details as a result of the job:
        name, guid, status, hostname.

        Parameters
        ----------
        Returns
        -------
        list[PoolInfo]:
            Pools Available For Import
        """
        ...
    @typing.overload
    def import_pool(self, 
        pool_import:'PoolImport',
    /) -> 'bool': 
        """
        Import a pool found with `pool.import_find`.
        
        If a `name` is specified the pool will be imported using that new name.
        
        If `enable_attachments` is set to true, attachments that were disabled during pool export will be
        re-enabled.
        
        Errors:
            ENOENT - Pool not found

        Parameters
        ----------
        pool_import:
            pool_import
        Returns
        -------
        bool:
            successful_import
        """
        ...
    @typing.overload
    def is_upgraded(self, 
        id:'int',
    /) -> 'bool': 
        """
        Returns whether or not the pool of `id` is on the latest version and with all feature
        flags enabled.

        Parameters
        ----------
        id:
            Returns whether or not the pool of `id` is on the latest version and with all feature
            flags enabled.
        Returns
        -------
        bool:
            pool_is_upgraded
        """
        ...
    @typing.overload
    def offline(self, 
        id:'int',
        options:'Options',
    /) -> 'bool': 
        """
        Offline a disk from pool of id `id`.
        
        `label` is the vdev guid or device name.

        Parameters
        ----------
        id:
            Offline a disk from pool of id `id`.
        options:
            options
        Returns
        -------
        bool:
            offline_successful
        """
        ...
    @typing.overload
    def online(self, 
        id:'int',
        options:'Options',
    /) -> 'bool': 
        """
        Online a disk from pool of id `id`.
        
        `label` is the vdev guid or device name.

        Parameters
        ----------
        id:
            Online a disk from pool of id `id`.
        options:
            options
        Returns
        -------
        bool:
            online_successful
        """
        ...
    @typing.overload
    def processes(self, 
        id:'int',
    /) -> 'list[Process]': 
        """
        Returns a list of running processes using this pool.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        list[Process]:
            processes
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]',
        query_options:'QueryOptions',
    /) -> 'typing.Union[list[PoolEntry], PoolEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[PoolEntry], PoolEntry, int]:
            
        """
        ...
    @typing.overload
    def remove(self, 
        id:'int',
        options:'Options',
    /) -> None: 
        """
        Remove a disk from pool of id `id`.
        
        `label` is the vdev guid or device name.
        
        Error codes:
        
            EZFS_NOSPC(2032): out of space to remove a device
            EZFS_NODEVICE(2017): no such device in pool
            EZFS_NOREPLICAS(2019): no valid replicas

        Parameters
        ----------
        id:
            Remove a disk from pool of id `id`.
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def replace(self, 
        id:'int',
        options:'Options__',
    /) -> 'bool': 
        """
        Replace a disk on a pool.
        
        `label` is the ZFS guid or a device name
        `disk` is the identifier of a disk
        If `preserve_settings` is true, then settings (power management, S.M.A.R.T., etc.) of a disk being replaced
        will be applied to a new disk.

        Parameters
        ----------
        id:
            id
        options:
            options
        Returns
        -------
        bool:
            replaced_successfully
        """
        ...
    @typing.overload
    def scrub(self, 
        id:'int',
        action:'Action',
    /) -> None: 
        """
        Performs a scrub action to pool of `id`.
        
        `action` can be either of "START", "STOP" or "PAUSE".

        Parameters
        ----------
        id:
            Performs a scrub action to pool of `id`.
        action:
            `action` can be either of "START", "STOP" or "PAUSE".
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        pool_update:'PoolUpdate',
    /) -> 'PoolUpdateReturns': 
        """
        Update pool of `id`, adding the new topology.
        
        The `type` of `data` must be the same of existing vdevs.

        Parameters
        ----------
        id:
            Update pool of `id`, adding the new topology.
        pool_update:
            pool_update
        Returns
        -------
        PoolUpdateReturns:
            pool_update_returns
        """
        ...
    @typing.overload
    def upgrade(self, 
        id:'int',
    /) -> 'bool': 
        """
        Upgrade pool of `id` to latest version with all feature flags.

        Parameters
        ----------
        id:
            Upgrade pool of `id` to latest version with all feature flags.
        Returns
        -------
        bool:
            upgraded
        """
        ...
    @typing.overload
    def validate_name(self, 
        pool_name:'str',
    /) -> None: 
        """
        Validates `pool_name` is a valid name for a pool.

        Parameters
        ----------
        pool_name:
            pool_name
        Returns
        -------
        """
        ...
    PoolAttach = typing.TypedDict('PoolAttach', {
            'target_vdev':'str',
            'new_disk':'str',
            'allow_duplicate_serials':'bool',
    })
    Attachment = typing.TypedDict('Attachment', {
            'type':'str',
            'service':'typing.Optional[str]',
            'attachments':'list[str]',
    })
    PoolCreate = typing.TypedDict('PoolCreate', {
            'name':'str',
            'encryption':'bool',
            'deduplication':'typing.Optional[str]',
            'checksum':'typing.Optional[str]',
            'encryption_options':'EncryptionOptions',
            'topology':'Topology',
            'allow_duplicate_serials':'bool',
    })
    EncryptionOptions = typing.TypedDict('EncryptionOptions', {
            'generate_key':'bool',
            'pbkdf2iters':'int',
            'algorithm':'Algorithm',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    class Algorithm(str,Enum):
        AES128CCM = 'AES-128-CCM'
        AES192CCM = 'AES-192-CCM'
        AES256CCM = 'AES-256-CCM'
        AES128GCM = 'AES-128-GCM'
        AES192GCM = 'AES-192-GCM'
        AES256GCM = 'AES-256-GCM'
        ...
    Topology = typing.TypedDict('Topology', {
            'data':'list[Datavdevs]',
            'special':'list[Specialvdevs]',
            'dedup':'list[Dedupvdevs]',
            'cache':'list[Cachevdevs]',
            'log':'list[Logvdevs]',
            'spares':'list[str]',
    })
    Datavdevs = typing.TypedDict('Datavdevs', {
            'type':'Type',
            'disks':'list[str]',
            'draid_data_disks':'int',
            'draid_spare_disks':'int',
    })
    class Type(str,Enum):
        DRAID1 = 'DRAID1'
        DRAID2 = 'DRAID2'
        DRAID3 = 'DRAID3'
        RAIDZ1 = 'RAIDZ1'
        RAIDZ2 = 'RAIDZ2'
        RAIDZ3 = 'RAIDZ3'
        MIRROR = 'MIRROR'
        STRIPE = 'STRIPE'
        ...
    Specialvdevs = typing.TypedDict('Specialvdevs', {
            'type':'Type_',
            'disks':'list[str]',
    })
    class Type_(str,Enum):
        MIRROR = 'MIRROR'
        STRIPE = 'STRIPE'
        ...
    Dedupvdevs = typing.TypedDict('Dedupvdevs', {
            'type':'Type_',
            'disks':'list[str]',
    })
    Cachevdevs = typing.TypedDict('Cachevdevs', {
            'type':'Type__',
            'disks':'list[str]',
    })
    class Type__(str,Enum):
        STRIPE = 'STRIPE'
        ...
    Logvdevs = typing.TypedDict('Logvdevs', {
            'type':'Type___',
            'disks':'list[str]',
    })
    class Type___(str,Enum):
        STRIPE = 'STRIPE'
        MIRROR = 'MIRROR'
        ...
    PoolCreateReturns = typing.TypedDict('PoolCreateReturns', {
            'id':'int',
            'name':'str',
            'guid':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology_',
    })
    Topology_ = typing.TypedDict('Topology_', {
            'data':'list',
            'log':'list',
            'cache':'list',
            'spare':'list',
            'special':'list',
            'dedup':'list',
    })
    Options = typing.TypedDict('Options', {
            'label':'str',
    })
    Options_ = typing.TypedDict('Options_', {
            'cascade':'bool',
            'restart_services':'bool',
            'destroy':'bool',
    })
    class Type____(str,Enum):
        FILESYSTEM = 'FILESYSTEM'
        VOLUME = 'VOLUME'
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
    PoolEntry = typing.TypedDict('PoolEntry', {
            'id':'int',
            'name':'str',
            'guid':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology_',
    })
    PoolInfo = typing.TypedDict('PoolInfo', {
            'name':'str',
            'guid':'str',
            'status':'str',
            'hostname':'str',
    })
    PoolImport = typing.TypedDict('PoolImport', {
            'guid':'str',
            'name':'str',
            'enable_attachments':'bool',
    })
    Process = typing.TypedDict('Process', {
            'pid':'int',
            'name':'str',
            'service':'str',
            'cmdline':'str',
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
    Options__ = typing.TypedDict('Options__', {
            'label':'str',
            'disk':'str',
            'force':'bool',
            'preserve_settings':'bool',
    })
    class Action(str,Enum):
        START = 'START'
        STOP = 'STOP'
        PAUSE = 'PAUSE'
        ...
    PoolUpdate = typing.TypedDict('PoolUpdate', {
            'topology':'Topology',
            'allow_duplicate_serials':'bool',
            'autotrim':'Autotrim',
    })
    class Autotrim(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        ...
    PoolUpdateReturns = typing.TypedDict('PoolUpdateReturns', {
            'id':'int',
            'name':'str',
            'guid':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology_',
    })
