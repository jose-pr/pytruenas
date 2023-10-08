
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Pool(Namespace):
    _namespace:_ty.Literal['pool']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def attach(self, 
        oid:'int',
        pool_attach:'dict[str]'={},
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
    @_ty.overload
    def attachments(self, 
        id:'int',
    /) -> 'list': 
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
        list:
            attachments
        """
        ...
    @_ty.overload
    def create(self, 
        pool_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            pool_create_returns
        """
        ...
    @_ty.overload
    def detach(self, 
        id:'int',
        options:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
    def export(self, 
        id:'int',
        options:'dict[str]'={},
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
    @_ty.overload
    def filesystem_choices(self, 
        types:'list'=["FILESYSTEM", "VOLUME"],
    /) -> 'list': 
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
        list:
            filesystem_choices
        """
        ...
    @_ty.overload
    def get_disks(self, 
        id:'int|None'=None,
    /) -> 'list': 
        """
        Get all disks in use by pools.
        If `id` is provided only the disks from the given pool `id` will be returned.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        list:
            pool_disks
        """
        ...
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
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
    @_ty.overload
    def get_instance_by_name(self, 
        name:'str',
    /) -> 'dict[str]': 
        """
        Returns pool with name `name`. If `name` is not found, Validation error is raised.

        Parameters
        ----------
        name:
            name
        Returns
        -------
        dict[str]:
            pool_entry
        """
        ...
    @_ty.overload
    def import_find(self, 
    /) -> 'list': 
        """
        Returns a job id which can be used to retrieve a list of pools available for
        import with the following details as a result of the job:
        name, guid, status, hostname.

        Parameters
        ----------
        Returns
        -------
        list:
            Pools Available For Import
        """
        ...
    @_ty.overload
    def import_pool(self, 
        pool_import:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
    def offline(self, 
        id:'int',
        options:'dict[str]'={},
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
    @_ty.overload
    def online(self, 
        id:'int',
        options:'dict[str]'={},
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
    @_ty.overload
    def processes(self, 
        id:'int',
    /) -> 'list': 
        """
        Returns a list of running processes using this pool.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        list:
            processes
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def remove(self, 
        id:'int',
        options:'dict[str]'={},
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
    @_ty.overload
    def replace(self, 
        id:'int',
        options:'dict[str]'={},
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
    @_ty.overload
    def scrub(self, 
        id:'int',
        action:'str',
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
    @_ty.overload
    def update(self, 
        id:'int',
        pool_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            pool_update_returns
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
