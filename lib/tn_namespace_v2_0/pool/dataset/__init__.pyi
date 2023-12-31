
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class PoolDataset(
    Namespace
    ):
    _namespace:typing.Literal['pool.dataset']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def attachments(self, 
        _id:'str',
    /) -> 'list[Attachment]': 
        """
        Return a list of services dependent of this dataset.
        
        Responsible for telling the user whether there is a related
        share, asking for confirmation.
        
        Example return value:
        [
          {
            "type": "NFS Share",
            "service": "nfs",
            "attachments": ["/mnt/tank/work"]
          }
        ]

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
    def change_key(self, 
        _id:'str',
        _change_key_options:'ChangeKeyOptions',
    /) -> None: 
        """
        Change encryption properties for `id` encrypted dataset.
        
        Changing dataset encryption to use passphrase instead of a key is not allowed if:
        
        1) It has encrypted roots as children which are encrypted with a key
        2) If it is a root dataset where the system dataset is located

        Parameters
        ----------
        id:
            Change encryption properties for `id` encrypted dataset.
        change_key_options:
            change_key_options
        Returns
        -------
        """
        ...
    @typing.overload
    def checksum_choices(self, 
    /) -> 'ChecksumChoices': 
        """
        Retrieve checksums supported for ZFS dataset.

        Parameters
        ----------
        Returns
        -------
        ChecksumChoices:
            checksum_choices
        """
        ...
    @typing.overload
    def compression_choices(self, 
    /) -> 'CompressionChoices': 
        """
        Retrieve compression algorithm supported by ZFS.

        Parameters
        ----------
        Returns
        -------
        CompressionChoices:
            compression_choices
        """
        ...
    @typing.overload
    def create(self, 
        _pool_dataset_create:'PoolDatasetCreate',
    /) -> 'PoolDatasetCreateReturns': 
        """
        Creates a dataset/zvol.
        
        `volsize` is required for type=VOLUME and is supposed to be a multiple of the block size.
        `sparse` and `volblocksize` are only used for type=VOLUME.
        
        `encryption` when enabled will create an ZFS encrypted root dataset for `name` pool.
        There is 1 case where ZFS encryption is not allowed for a dataset:
        1) If the parent dataset is encrypted with a passphrase and `name` is being created
           with a key for encrypting the dataset.
        
        `encryption_options` specifies configuration for encryption of dataset for `name` pool.
        `encryption_options.passphrase` must be specified if encryption for dataset is desired with a passphrase
        as a key.
        Otherwise a hex encoded key can be specified by providing `encryption_options.key`.
        `encryption_options.generate_key` when enabled automatically generates the key to be used
        for dataset encryption.
        
        It should be noted that keys are stored by the system for automatic locking/unlocking
        on import/export of encrypted datasets. If that is not desired, dataset should be created
        with a passphrase as a key.

        Parameters
        ----------
        pool_dataset_create:
            pool_dataset_create
        Returns
        -------
        PoolDatasetCreateReturns:
            pool_dataset_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        _id:'str',
        _dataset_delete:'DatasetDelete',
    /) -> 'bool': 
        """
        Delete dataset/zvol `id`.
        
        `recursive` will also delete/destroy all children datasets.
        `force` will force delete busy datasets.
        
        When root dataset is specified as `id` with `recursive`, it will destroy all the children of the
        root dataset present leaving root dataset intact.

        Parameters
        ----------
        id:
            Delete dataset/zvol `id`.
            When root dataset is specified as `id` with `recursive`, it will destroy all the children of the
            root dataset present leaving root dataset intact.
        dataset_delete:
            dataset_delete
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def destroy_snapshots(self, 
        _name:'str',
        _snapshots:'Snapshots',
    /) -> 'list[str]': 
        """
        Destroy specified snapshots of a given dataset.

        Parameters
        ----------
        name:
            name
        snapshots:
            snapshots
        Returns
        -------
        list[str]:
            deleted_snapshots
        """
        ...
    @typing.overload
    def details(self, 
    /) -> 'list': 
        """
        Retrieve all dataset(s) details outlining any services/tasks which might be consuming the dataset(s).

        Parameters
        ----------
        Returns
        -------
        list:
            Example(s):
            ```
            [
                {
                    "id": "tank",
                    "type": "FILESYSTEM",
                    "name": "tank",
                    "pool": "tank",
                    "encrypted": false,
                    "encryption_root": null,
                    "key_loaded": false,
                    "children": [
                        {
                            "id": "tank/soemthing",
                            "type": "VOLUME",
                            "name": "tank/soemthing",
                            "pool": "tank",
                            "encrypted": false,
                            "encryption_root": null,
                            "key_loaded": false,
                            "children": [],
                            "managed_by": {
                                "value": "10.231.1.155",
                                "rawvalue": "10.231.1.155",
                                "source": "LOCAL",
                                "parsed": "10.231.1.155"
                            },
                            "quota_warning": {
                                "value": "80",
                                "rawvalue": "80",
                                "source": "LOCAL",
                                "parsed": "80"
                            },
                            "quota_critical": {
                                "value": "95",
                                "rawvalue": "95",
                                "source": "LOCAL",
                                "parsed": "95"
                            },
                            "refquota_warning": {
                                "value": "80",
                                "rawvalue": "80",
                                "source": "LOCAL",
                                "parsed": "80"
                            },
                            "refquota_critical": {
                                "value": "95",
                                "rawvalue": "95",
                                "source": "LOCAL",
                                "parsed": "95"
                            },
                            "reservation": {
                                "parsed": null,
                                "rawvalue": "0",
                                "value": null,
                                "source": "DEFAULT",
                                "source_info": null
                            },
                            "refreservation": {
                                "parsed": null,
                                "rawvalue": "0",
                                "value": null,
                                "source": "DEFAULT",
                                "source_info": null
                            },
                            "key_format": {
                                "parsed": "none",
                                "rawvalue": "none",
                                "value": null,
                                "source": "DEFAULT",
                                "source_info": null
                            },
                            "volsize": {
                                "parsed": 57344,
                                "rawvalue": "57344",
                                "value": "56K",
                                "source": "LOCAL",
                                "source_info": null
                            },
                            "encryption_algorithm": {
                                "parsed": "off",
                                "rawvalue": "off",
                                "value": null,
                                "source": "DEFAULT",
                                "source_info": null
                            },
                            "used": {
                                "parsed": 57344,
                                "rawvalue": "57344",
                                "value": "56K",
                                "source": "NONE",
                                "source_info": null
                            },
                            "usedbychildren": {
                                "parsed": 0,
                                "rawvalue": "0",
                                "value": "0B",
                                "source": "NONE",
                                "source_info": null
                            },
                            "usedbydataset": {
                                "parsed": 57344,
                                "rawvalue": "57344",
                                "value": "56K",
                                "source": "NONE",
                                "source_info": null
                            },
                            "usedbysnapshots": {
                                "parsed": 0,
                                "rawvalue": "0",
                                "value": "0B",
                                "source": "NONE",
                                "source_info": null
                            },
                            "available": {
                                "parsed": 14328811520,
                                "rawvalue": "14328811520",
                                "value": "13.3G",
                                "source": "NONE",
                                "source_info": null
                            },
                            "mountpoint": "/mnt/tank/something",
                            "sync": {
                                "parsed": "standard",
                                "rawvalue": "standard",
                                "value": "STANDARD",
                                "source": "DEFAULT",
                                "source_info": null
                            },
                            "compression": {
                                "parsed": "lz4",
                                "rawvalue": "lz4",
                                "value": "LZ4",
                                "source": "INHERITED",
                                "source_info": "tank"
                            },
                            "deduplication": {
                                "parsed": "on",
                                "rawvalue": "on",
                                "value": "ON",
                                "source": "LOCAL",
                                "source_info": null
                            },
                            "user_properties": {},
                            "snapshot_count": 0,
                            "locked": false,
                            "thick_provisioned": true,
                            "nfs_shares": [
                                {
                                    "enabled": true,
                                    "path": "/mnt/tank/something"
                                }
                            ],
                            "smb_shares": [
                                {
                                    "enabled": false,
                                    "path": "/mnt/tank/something/smbshare01",
                                    "share_name": "Home Pictures"
                                }
                            ],
                            "iscsi_shares": [
                                {
                                    "enabled": false,
                                    "type": "DISK",
                                    "path": "/mnt/tank/something"
                                }
                            ],
                            "vms": [
                                {
                                    "name": "deb01",
                                    "path": "/dev/zvol/tank/something"
                                }
                            ],
                            "apps": [
                                {
                                    "name": "diskoverdata",
                                    "path": "/mnt/tank/something"
                                }
                            ],
                            "replication_tasks_count": 0,
                            "snapshot_tasks_count": 0,
                            "cloudsync_tasks_count": 0,
                            "rsync_tasks_count": 0
                        }
                    ],
                    "mountpoint": "/mnt/tank",
                    "quota": {
                        "parsed": null,
                        "rawvalue": "0",
                        "value": null,
                        "source": "DEFAULT",
                        "source_info": null
                    },
                    "refquota": {
                        "parsed": null,
                        "rawvalue": "0",
                        "value": null,
                        "source": "DEFAULT",
                        "source_info": null
                    },
                    "reservation": {
                        "parsed": null,
                        "rawvalue": "0",
                        "value": null,
                        "source": "DEFAULT",
                        "source_info": null
                    },
                    "refreservation": {
                        "parsed": null,
                        "rawvalue": "0",
                        "value": null,
                        "source": "DEFAULT",
                        "source_info": null
                    },
                    "encryption_algorithm": {
                        "parsed": "off",
                        "rawvalue": "off",
                        "value": null,
                        "source": "DEFAULT",
                        "source_info": null
                    },
                    "origin": {
                        "parsed": "",
                        "rawvalue": "",
                        "value": "",
                        "source": "NONE",
                        "source_info": null
                    },
                    "used": {
                        "parsed": 3874467840,
                        "rawvalue": "3874467840",
                        "value": "3.61G",
                        "source": "NONE",
                        "source_info": null
                    },
                    "usedbychildren": {
                        "parsed": 3874369536,
                        "rawvalue": "3874369536",
                        "value": "3.61G",
                        "source": "NONE",
                        "source_info": null
                    },
                    "usedbydataset": {
                        "parsed": 98304,
                        "rawvalue": "98304",
                        "value": "96K",
                        "source": "NONE",
                        "source_info": null
                    },
                    "usedbysnapshots": {
                        "parsed": 0,
                        "rawvalue": "0",
                        "value": "0B",
                        "source": "NONE",
                        "source_info": null
                    },
                    "available": {
                        "parsed": 14328811520,
                        "rawvalue": "14328811520",
                        "value": "13.3G",
                        "source": "NONE",
                        "source_info": null
                    },
                    "user_properties": {},
                    "snapshot_count": 0,
                    "locked": false,
                    "atime": false,
                    "casesensitive": true,
                    "readonly": false,
                    "nfs_shares": [],
                    "smb_shares": [],
                    "iscsi_shares": [],
                    "vms": [],
                    "apps": [
                        {
                            "name": "plex",
                            "path": "/mnt/evo/data"
                        }
                    ],
                    "replication_tasks_count": 0,
                    "snapshot_tasks_count": 0,
                    "cloudsync_tasks_count": 0,
                    "rsync_tasks_count": 0
                }
            ]
            ```
        """
        ...
    @typing.overload
    def encryption_algorithm_choices(self, 
    /) -> 'EncryptionAlgorithmChoices': 
        """
        Retrieve encryption algorithms supported for ZFS dataset encryption.

        Parameters
        ----------
        Returns
        -------
        EncryptionAlgorithmChoices:
            encryption_algorithm_choices
        """
        ...
    @typing.overload
    def encryption_summary(self, 
        _id:'str',
        _encryption_root_summary_options:'EncryptionRootSummaryOptions',
    /) -> 'list[DatasetEncryptionSummary]': 
        """
        Retrieve summary of all encrypted roots under `id`.
        
        Keys/passphrase can be supplied to check if the keys are valid.
        
        It should be noted that there are 2 keys which show if a recursive unlock operation is
        done for `id`, which dataset will be unlocked and if not why it won't be unlocked. The keys
        namely are "unlock_successful" and "unlock_error". The former is a boolean value showing if unlock
        would succeed/fail. The latter is description why it failed if it failed.
        
        In some cases it's possible that the provided key/passphrase is valid but the path where the dataset is
        supposed to be mounted after being unlocked already exists and is not empty. In this case, unlock operation
        would fail and `unlock_error` will reflect this error appropriately. This can be overridden by setting
        `encryption_root_summary_options.datasets.X.force` boolean flag or by setting
        `encryption_root_summary_options.force` flag. In practice, when the dataset is going to be unlocked
        and these flags have been provided to `pool.dataset.unlock`, system will rename the directory/file path
        where the dataset should be mounted resulting in successful unlock of the dataset.
        
        If a dataset is already unlocked, it will show up as true for "unlock_successful" regardless of what
        key user provided as the unlock keys in the output are to reflect what a real unlock operation would
        behave. If user is interested in seeing if a provided key is valid or not, then the key to look out for
        in the output is "valid_key" which based on what system has in database or if a user provided one, validates
        the key and sets a boolean value for the dataset.
        
        Example output:
        [
            {
                "name": "vol",
                "key_format": "PASSPHRASE",
                "key_present_in_database": false,
                "valid_key": true,
                "locked": true,
                "unlock_error": null,
                "unlock_successful": true
            },
            {
                "name": "vol/c1/d1",
                "key_format": "PASSPHRASE",
                "key_present_in_database": false,
                "valid_key": false,
                "locked": true,
                "unlock_error": "Provided key is invalid",
                "unlock_successful": false
            },
            {
                "name": "vol/c",
                "key_format": "PASSPHRASE",
                "key_present_in_database": false,
                "valid_key": false,
                "locked": true,
                "unlock_error": "Key not provided",
                "unlock_successful": false
            },
            {
                "name": "vol/c/d2",
                "key_format": "PASSPHRASE",
                "key_present_in_database": false,
                "valid_key": false,
                "locked": true,
                "unlock_error": "Child cannot be unlocked when parent "vol/c" is locked and provided key is invalid",
                "unlock_successful": false
            }
        ]

        Parameters
        ----------
        id:
            Retrieve summary of all encrypted roots under `id`.
            It should be noted that there are 2 keys which show if a recursive unlock operation is
            done for `id`, which dataset will be unlocked and if not why it won't be unlocked. The keys
            namely are "unlock_successful" and "unlock_error". The former is a boolean value showing if unlock
            would succeed/fail. The latter is description why it failed if it failed.
        encryption_root_summary_options:
            encryption_root_summary_options
        Returns
        -------
        list[DatasetEncryptionSummary]:
            encryption_summary
        """
        ...
    @typing.overload
    def export_key(self, 
        _id:'str',
        _download:'bool',
    /) -> 'typing.Optional[str]': 
        """
        Export own encryption key for dataset `id`. If `download` is `true`, key will be downloaded in a json file
        where the same file can be used to unlock the dataset, otherwise it will be returned as string.
        
        Please refer to websocket documentation for downloading the file.

        Parameters
        ----------
        id:
            Export own encryption key for dataset `id`. If `download` is `true`, key will be downloaded in a json file
            where the same file can be used to unlock the dataset, otherwise it will be returned as string.
        download:
            Export own encryption key for dataset `id`. If `download` is `true`, key will be downloaded in a json file
            where the same file can be used to unlock the dataset, otherwise it will be returned as string.
        Returns
        -------
        typing.Optional[str]:
            key
        """
        ...
    @typing.overload
    def export_keys(self, 
        _id:'str',
    /) -> None: 
        """
        Export keys for `id` and its children which are stored in the system. The exported file is a JSON file
        which has a dictionary containing dataset names as keys and their keys as the value.
        
        Please refer to websocket documentation for downloading the file.

        Parameters
        ----------
        id:
            Export keys for `id` and its children which are stored in the system. The exported file is a JSON file
            which has a dictionary containing dataset names as keys and their keys as the value.
        Returns
        -------
        """
        ...
    @typing.overload
    def export_keys_for_replication(self, 
        _id:'int',
    /) -> None: 
        """
        Export keys for replication task `id` for source dataset(s) which are stored in the system. The exported file
        is a JSON file which has a dictionary containing dataset names as keys and their keys as the value.
        
        Please refer to websocket documentation for downloading the file.

        Parameters
        ----------
        id:
            Export keys for replication task `id` for source dataset(s) which are stored in the system. The exported file
            is a JSON file which has a dictionary containing dataset names as keys and their keys as the value.
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
    def get_quota(self, 
        _ds:'str',
        _quota_type:'QuotaType',
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> None: 
        """
        Return a list of the specified `quota_type` of quotas on the ZFS dataset `ds`.
        Support `query-filters` and `query-options`. used_bytes may not instantly
        update as space is used.
        
        When quota_type is not DATASET, each quota entry has these fields:
        
        `id` - the uid or gid to which the quota applies.
        
        `name` - the user or group name to which the quota applies. Value is
        null if the id in the quota cannot be resolved to a user or group. This
        indicates that the user or group does not exist on the server.
        
        `quota` - the quota size in bytes.  Absent if no quota is set.
        
        `used_bytes` - the amount of bytes the user has written to the dataset.
        A value of zero means unlimited.
        
        `obj_quota` - the number of objects that may be owned by `id`.
        A value of zero means unlimited.  Absent if no objquota is set.
        
        `obj_used` - the number of objects currently owned by `id`.
        
        Note: SMB client requests to set a quota granting no space will result
        in an on-disk quota of 1 KiB.

        Parameters
        ----------
        ds:
            Return a list of the specified `quota_type` of quotas on the ZFS dataset `ds`.
            Support `query-filters` and `query-options`. used_bytes may not instantly
            update as space is used.
        quota_type:
            Return a list of the specified `quota_type` of quotas on the ZFS dataset `ds`.
            Support `query-filters` and `query-options`. used_bytes may not instantly
            update as space is used.
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        """
        ...
    @typing.overload
    def inherit_parent_encryption_properties(self, 
        _id:'str',
    /) -> None: 
        """
        Allows inheriting parent's encryption root discarding its current encryption settings. This
        can only be done where `id` has an encrypted parent and `id` itself is an encryption root.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @typing.overload
    def lock(self, 
        _id:'str',
        _lock_options:'LockOptions',
    /) -> 'bool': 
        """
        Locks `id` dataset. It will unmount the dataset and its children before locking.
        
        After the dataset has been unmounted, system will set immutable flag on the dataset's mountpoint where
        the dataset was mounted before it was locked making sure that the path cannot be modified. Once the dataset
        is unlocked, it will not be affected by this change and consumers can continue consuming it.

        Parameters
        ----------
        id:
            Locks `id` dataset. It will unmount the dataset and its children before locking.
        lock_options:
            lock_options
        Returns
        -------
        bool:
            locked
        """
        ...
    @typing.overload
    def mountpoint(self, 
        _dataset:'str',
        _raise:'bool',
    /) -> 'typing.Optional[str]': 
        """
        Returns mountpoint for specific mounted dataset. If it is not mounted and `raise` is `true` (default), an
        error is raised. `null` is returned otherwise.

        Parameters
        ----------
        dataset:
            dataset
        raise:
            raise
        Returns
        -------
        typing.Optional[str]:
            mountpoint
        """
        ...
    @typing.overload
    def permission(self, 
        _id:'str',
        _pool_dataset_permission:'PoolDatasetPermission',
    /) -> 'PoolDatasetPermission': 
        """
        Set permissions for a dataset `id`. Permissions may be specified as
        either a posix `mode` or an `acl`. This method is a wrapper around
        `filesystem.setperm`, `filesystem.setacl`, and `filesystem.chown`
        
        `filesystem.setperm` is called if `mode` is specified.
        `filesystem.setacl` is called if `acl` is specified or if the
        option `set_default_acl` is selected.
        `filesystem.chown` is called if neither `mode` nor `acl` is
        specified.
        
        The following `options` are supported:
        
        `set_default_acl` - apply a default ACL appropriate for specified
        dataset. Default ACL is `NFS4_RESTRICTED` or `POSIX_RESTRICTED`
        ACL template builtin with additional entries builtin_users group
        and builtin_administrators group. See documentation for
        `filesystem.acltemplate` for more details.
        
        `stripacl` - this option must be set in order to apply a POSIX
        mode to a dataset that has a non-trivial ACL. The effect will
        be to remove existing ACL and replace with specified mode.
        
        `recursive` - apply permissions recursively to dataset (all files
        and directories will be impacted.
        
        `traverse` - permit recursive job to traverse filesystem boundaries
        (child datasets).

        Parameters
        ----------
        id:
            Set permissions for a dataset `id`. Permissions may be specified as
            either a posix `mode` or an `acl`. This method is a wrapper around
            `filesystem.setperm`, `filesystem.setacl`, and `filesystem.chown`
        pool_dataset_permission:
            pool_dataset_permission
        Returns
        -------
        PoolDatasetPermission:
            pool_dataset_permission
        """
        ...
    @typing.overload
    def processes(self, 
        _id:'str',
    /) -> 'list[Process]': 
        """
        Return a list of processes using this dataset.
        
        Example return value:
        
        [
          {
            "pid": 2520,
            "name": "smbd",
            "service": "cifs"
          },
          {
            "pid": 97778,
            "name": "minio",
            "cmdline": "/usr/local/bin/minio -C /usr/local/etc/minio server --address=0.0.0.0:9000 --quiet /mnt/tank/wk"
          }
        ]

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
    def promote(self, 
        _id:'str',
    /) -> None: 
        """
        Promote the cloned dataset `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @typing.overload
    def query(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list[PoolDatasetEntry], PoolDatasetEntry, int]': 
        """
        Query Pool Datasets with `query-filters` and `query-options`.
        
        We provide two ways to retrieve datasets. The first is a flat structure (default), where
        all datasets in the system are returned as separate objects which contain all data
        there is for their children. This retrieval type is slightly slower because of duplicates in each object.
        The second type is hierarchical, where only top level datasets are returned in the list. They contain all the
        children in the `children` key. This retrieval type is slightly faster.
        These options are controlled by the `query-options.extra.flat` attribute (default true).
        
        In some cases it might be desirable to only retrieve details of a dataset itself and not it's children, in this
        case `query-options.extra.retrieve_children` should be explicitly specified and set to `false` which will
        result in children not being retrieved.
        
        In case only some properties are desired to be retrieved for datasets, consumer should specify
        `query-options.extra.properties` which when `null` ( which is the default ) will retrieve all properties
        and otherwise a list can be specified like `["type", "used", "available"]` to retrieve selective properties.
        If no properties are desired, in that case an empty list should be sent.
        
        `query-options.extra.snapshots` can be set to retrieve snapshot(s) of dataset in question.
        
        `query-options.extra.snapshots_recursive` can be set to retrieve snapshot(s) recursively of dataset in question.
        If `query-options.extra.snapshots_recursive` and `query-options.extra.snapshots` are set, snapshot(s) will be
        retrieved recursively.
        
        `query-options.extra.snapshots_properties` can be specified to list out properties which should be retrieved
        for snapshot(s) related to each dataset. By default only name of the snapshot would be retrieved, however
        if `null` is specified all properties of the snapshot would be retrieved in this case.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[PoolDatasetEntry], PoolDatasetEntry, int]:
            
        """
        ...
    @typing.overload
    def recommended_zvol_blocksize(self, 
        _pool:'str',
    /) -> 'str': 
        """
        Helper method to get recommended size for a new zvol (dataset of type VOLUME).

        Parameters
        ----------
        pool:
            pool
        Returns
        -------
        str:
            recommended_zvol_blocksize
        """
        ...
    @typing.overload
    def recordsize_choices(self, 
        _pool_name:'typing.Optional[str]',
    /) -> 'list[str]': 
        """
        Retrieve recordsize choices for datasets.

        Parameters
        ----------
        pool_name:
            pool_name
        Returns
        -------
        list[str]:
            recordsize_choices
        """
        ...
    @typing.overload
    def set_quota(self, 
        _ds:'str',
        _quotas:'list[QuotaEntry]',
    /) -> None: 
        """
        There are three over-arching types of quotas for ZFS datasets.
        1) dataset quotas and refquotas. If a DATASET quota type is specified in
        this API call, then the API acts as a wrapper for `pool.dataset.update`.
        
        2) User and group quotas. These limit the amount of disk space consumed
        by files that are owned by the specified users or groups. If the respective
        "object quota" type is specfied, then the quota limits the number of objects
        that may be owned by the specified user or group.
        
        3) Project quotas. These limit the amount of disk space consumed by files
        that are owned by the specified project. Project quotas are not yet implemended.
        
        This API allows users to set multiple quotas simultaneously by submitting a
        list of quotas. The list may contain all supported quota types.
        
        `ds` the name of the target ZFS dataset.
        
        `quotas` specifies a list of `quota_entry` entries to apply to dataset.
        
        `quota_entry` entries have these required parameters:
        
        `quota_type`: specifies the type of quota to apply to the dataset. Possible
        values are USER, USEROBJ, GROUP, GROUPOBJ, and DATASET. USEROBJ and GROUPOBJ
        quotas limit the number of objects consumed by the specified user or group.
        
        `id`: the uid, gid, or name to which the quota applies. If quota_type is
        'DATASET', then `id` must be either `QUOTA` or `REFQUOTA`.
        
        `quota_value`: the quota size in bytes. Setting a value of `0` removes
        the user or group quota.

        Parameters
        ----------
        ds:
            `ds` the name of the target ZFS dataset.
        quotas:
            `quotas` specifies a list of `quota_entry` entries to apply to dataset.
        Returns
        -------
        """
        ...
    @typing.overload
    def snapshot_count(self, 
        _dataset:'str',
    /) -> 'int': 
        """
        Returns snapshot count for specified `dataset`.

        Parameters
        ----------
        dataset:
            dataset
        Returns
        -------
        int:
            snapshot_count
        """
        ...
    @typing.overload
    def unlock(self, 
        _id:'str',
        _unlock_options:'UnlockOptions',
    /) -> 'Unlock': 
        """
        Unlock dataset `id` (and its children if `unlock_options.recursive` is `true`).
        
        If `id` dataset is not encrypted an exception will be raised. There is one exception:
        when `id` is a root dataset and `unlock_options.recursive` is specified, encryption
        validation will not be performed for `id`. This allow unlocking encrypted children for the entire pool `id`.
        
        There are two ways to supply the key(s)/passphrase(s) for unlocking a dataset:
        
        1. Upload a json file which contains encrypted dataset keys (it will be read from the input pipe if
        `unlock_options.key_file` is `true`). The format is the one that is used for exporting encrypted dataset keys
        (`pool.export_keys`).
        
        2. Specify a key or a passphrase for each unlocked dataset using `unlock_options.datasets`.
        
        If `unlock_options.datasets.{i}.recursive` is `true`, a key or a passphrase is applied to all the encrypted
        children of a dataset.
        
        `unlock_options.toggle_attachments` controls whether attachments  should be put in action after unlocking
        dataset(s). Toggling attachments can theoretically lead to service interruption when daemons configurations are
        reloaded (this should not happen,  and if this happens it should be considered a bug). As TrueNAS does not have
        a state for resources that should be unlocked but are still locked, disabling this option will put the system
        into an inconsistent state so it should really never be disabled.
        
        In some cases it's possible that the provided key/passphrase is valid but the path where the dataset is
        supposed to be mounted after being unlocked already exists and is not empty. In this case, unlock operation
        would fail. This can be overridden by setting `unlock_options.datasets.X.force` boolean flag or by setting
        `unlock_options.force` flag. When any of these flags are set, system will rename the existing
        directory/file path where the dataset should be mounted resulting in successful unlock of the dataset.

        Parameters
        ----------
        id:
            Unlock dataset `id` (and its children if `unlock_options.recursive` is `true`).
            If `id` dataset is not encrypted an exception will be raised. There is one exception:
            when `id` is a root dataset and `unlock_options.recursive` is specified, encryption
            validation will not be performed for `id`. This allow unlocking encrypted children for the entire pool `id`.
        unlock_options:
            unlock_options
        Returns
        -------
        Unlock:
            unlock
        """
        ...
    @typing.overload
    def unlock_services_restart_choices(self, 
        _dataset:'str',
    /) -> 'dict[str]': 
        """
        Get a mapping of services identifiers and labels that can be restart on dataset unlock.

        Parameters
        ----------
        dataset:
            dataset
        Returns
        -------
        dict[str]:
            services_to_restart
        """
        ...
    @typing.overload
    def update(self, 
        _id:'str',
        _pool_dataset_update:'PoolDatasetUpdate',
    /) -> 'PoolDatasetUpdateReturns': 
        """
        Updates a dataset/zvol `id`.

        Parameters
        ----------
        id:
            Updates a dataset/zvol `id`.
        pool_dataset_update:
            pool_dataset_update
        Returns
        -------
        PoolDatasetUpdateReturns:
            pool_dataset_update_returns
        """
        ...
    class Aclmode(str,Enum):
        PASSTHROUGH = 'PASSTHROUGH'
        RESTRICTED = 'RESTRICTED'
        DISCARD = 'DISCARD'
        INHERIT = 'INHERIT'
        ...
    Aclmode_ = typing.TypedDict('Aclmode_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Acltype(str,Enum):
        OFF = 'OFF'
        NFSV4 = 'NFSV4'
        POSIX = 'POSIX'
        INHERIT = 'INHERIT'
        ...
    Acltype_ = typing.TypedDict('Acltype_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Algorithm(str,Enum):
        AES128CCM = 'AES-128-CCM'
        AES192CCM = 'AES-192-CCM'
        AES256CCM = 'AES-256-CCM'
        AES128GCM = 'AES-128-GCM'
        AES192GCM = 'AES-192-GCM'
        AES256GCM = 'AES-256-GCM'
        ...
    class Atime(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    Atime_ = typing.TypedDict('Atime_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Attachment = typing.TypedDict('Attachment', {
            'type':'str',
            'service':'typing.Optional[str]',
            'attachments':'list[str]',
    })
    Available = typing.TypedDict('Available', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class BASIC(str,Enum):
        FULLCONTROL = 'FULL_CONTROL'
        MODIFY = 'MODIFY'
        READ = 'READ'
        TRAVERSE = 'TRAVERSE'
        ...
    class BASIC_(str,Enum):
        INHERIT = 'INHERIT'
        NOINHERIT = 'NOINHERIT'
        ...
    class Casesensitivity(str,Enum):
        SENSITIVE = 'SENSITIVE'
        INSENSITIVE = 'INSENSITIVE'
        INHERIT = 'INHERIT'
        ...
    Casesensitivity_ = typing.TypedDict('Casesensitivity_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    ChangeKeyOptions = typing.TypedDict('ChangeKeyOptions', {
            'generate_key':'bool',
            'key_file':'bool',
            'pbkdf2iters':'int',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    class Checksum(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        FLETCHER2 = 'FLETCHER2'
        FLETCHER4 = 'FLETCHER4'
        SHA256 = 'SHA256'
        SHA512 = 'SHA512'
        SKEIN = 'SKEIN'
        EDONR = 'EDONR'
        INHERIT = 'INHERIT'
        ...
    ChecksumChoices = typing.TypedDict('ChecksumChoices', {
            'ON':'typing.Literal["ON"]',
            'FLETCHER2':'typing.Literal["FLETCHER2"]',
            'FLETCHER4':'typing.Literal["FLETCHER4"]',
            'SHA256':'typing.Literal["SHA256"]',
            'SHA512':'typing.Literal["SHA512"]',
            'SKEIN':'typing.Literal["SKEIN"]',
            'EDONR':'typing.Literal["EDONR"]',
    })
    Checksum_ = typing.TypedDict('Checksum_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Comments = typing.TypedDict('Comments', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Compression(str,Enum):
        OFF = 'OFF'
        LZ4 = 'LZ4'
        GZIP = 'GZIP'
        GZIP1 = 'GZIP-1'
        GZIP9 = 'GZIP-9'
        ZSTD = 'ZSTD'
        ZSTDFAST = 'ZSTD-FAST'
        ZLE = 'ZLE'
        LZJB = 'LZJB'
        ZSTD1 = 'ZSTD-1'
        ZSTD2 = 'ZSTD-2'
        ZSTD3 = 'ZSTD-3'
        ZSTD4 = 'ZSTD-4'
        ZSTD5 = 'ZSTD-5'
        ZSTD6 = 'ZSTD-6'
        ZSTD7 = 'ZSTD-7'
        ZSTD8 = 'ZSTD-8'
        ZSTD9 = 'ZSTD-9'
        ZSTD10 = 'ZSTD-10'
        ZSTD11 = 'ZSTD-11'
        ZSTD12 = 'ZSTD-12'
        ZSTD13 = 'ZSTD-13'
        ZSTD14 = 'ZSTD-14'
        ZSTD15 = 'ZSTD-15'
        ZSTD16 = 'ZSTD-16'
        ZSTD17 = 'ZSTD-17'
        ZSTD18 = 'ZSTD-18'
        ZSTD19 = 'ZSTD-19'
        ZSTDFAST1 = 'ZSTD-FAST-1'
        ZSTDFAST2 = 'ZSTD-FAST-2'
        ZSTDFAST3 = 'ZSTD-FAST-3'
        ZSTDFAST4 = 'ZSTD-FAST-4'
        ZSTDFAST5 = 'ZSTD-FAST-5'
        ZSTDFAST6 = 'ZSTD-FAST-6'
        ZSTDFAST7 = 'ZSTD-FAST-7'
        ZSTDFAST8 = 'ZSTD-FAST-8'
        ZSTDFAST9 = 'ZSTD-FAST-9'
        ZSTDFAST10 = 'ZSTD-FAST-10'
        ZSTDFAST20 = 'ZSTD-FAST-20'
        ZSTDFAST30 = 'ZSTD-FAST-30'
        ZSTDFAST40 = 'ZSTD-FAST-40'
        ZSTDFAST50 = 'ZSTD-FAST-50'
        ZSTDFAST60 = 'ZSTD-FAST-60'
        ZSTDFAST70 = 'ZSTD-FAST-70'
        ZSTDFAST80 = 'ZSTD-FAST-80'
        ZSTDFAST90 = 'ZSTD-FAST-90'
        ZSTDFAST100 = 'ZSTD-FAST-100'
        ZSTDFAST500 = 'ZSTD-FAST-500'
        ZSTDFAST1000 = 'ZSTD-FAST-1000'
        INHERIT = 'INHERIT'
        ...
    CompressionChoices = typing.TypedDict('CompressionChoices', {
            'OFF':'typing.Literal["OFF"]',
            'LZ4':'typing.Literal["LZ4"]',
            'GZIP':'typing.Literal["GZIP"]',
            'GZIP-1':'typing.Literal["GZIP-1"]',
            'GZIP-9':'typing.Literal["GZIP-9"]',
            'ZSTD':'typing.Literal["ZSTD"]',
            'ZSTD-FAST':'typing.Literal["ZSTD-FAST"]',
            'ZLE':'typing.Literal["ZLE"]',
            'LZJB':'typing.Literal["LZJB"]',
            'ZSTD-1':'typing.Literal["ZSTD-1"]',
            'ZSTD-2':'typing.Literal["ZSTD-2"]',
            'ZSTD-3':'typing.Literal["ZSTD-3"]',
            'ZSTD-4':'typing.Literal["ZSTD-4"]',
            'ZSTD-5':'typing.Literal["ZSTD-5"]',
            'ZSTD-6':'typing.Literal["ZSTD-6"]',
            'ZSTD-7':'typing.Literal["ZSTD-7"]',
            'ZSTD-8':'typing.Literal["ZSTD-8"]',
            'ZSTD-9':'typing.Literal["ZSTD-9"]',
            'ZSTD-10':'typing.Literal["ZSTD-10"]',
            'ZSTD-11':'typing.Literal["ZSTD-11"]',
            'ZSTD-12':'typing.Literal["ZSTD-12"]',
            'ZSTD-13':'typing.Literal["ZSTD-13"]',
            'ZSTD-14':'typing.Literal["ZSTD-14"]',
            'ZSTD-15':'typing.Literal["ZSTD-15"]',
            'ZSTD-16':'typing.Literal["ZSTD-16"]',
            'ZSTD-17':'typing.Literal["ZSTD-17"]',
            'ZSTD-18':'typing.Literal["ZSTD-18"]',
            'ZSTD-19':'typing.Literal["ZSTD-19"]',
            'ZSTD-FAST-1':'typing.Literal["ZSTD-FAST-1"]',
            'ZSTD-FAST-2':'typing.Literal["ZSTD-FAST-2"]',
            'ZSTD-FAST-3':'typing.Literal["ZSTD-FAST-3"]',
            'ZSTD-FAST-4':'typing.Literal["ZSTD-FAST-4"]',
            'ZSTD-FAST-5':'typing.Literal["ZSTD-FAST-5"]',
            'ZSTD-FAST-6':'typing.Literal["ZSTD-FAST-6"]',
            'ZSTD-FAST-7':'typing.Literal["ZSTD-FAST-7"]',
            'ZSTD-FAST-8':'typing.Literal["ZSTD-FAST-8"]',
            'ZSTD-FAST-9':'typing.Literal["ZSTD-FAST-9"]',
            'ZSTD-FAST-10':'typing.Literal["ZSTD-FAST-10"]',
            'ZSTD-FAST-20':'typing.Literal["ZSTD-FAST-20"]',
            'ZSTD-FAST-30':'typing.Literal["ZSTD-FAST-30"]',
            'ZSTD-FAST-40':'typing.Literal["ZSTD-FAST-40"]',
            'ZSTD-FAST-50':'typing.Literal["ZSTD-FAST-50"]',
            'ZSTD-FAST-60':'typing.Literal["ZSTD-FAST-60"]',
            'ZSTD-FAST-70':'typing.Literal["ZSTD-FAST-70"]',
            'ZSTD-FAST-80':'typing.Literal["ZSTD-FAST-80"]',
            'ZSTD-FAST-90':'typing.Literal["ZSTD-FAST-90"]',
            'ZSTD-FAST-100':'typing.Literal["ZSTD-FAST-100"]',
            'ZSTD-FAST-500':'typing.Literal["ZSTD-FAST-500"]',
            'ZSTD-FAST-1000':'typing.Literal["ZSTD-FAST-1000"]',
    })
    Compression_ = typing.TypedDict('Compression_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compressratio = typing.TypedDict('Compressratio', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Copies = typing.TypedDict('Copies', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Creation = typing.TypedDict('Creation', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Dataset = typing.TypedDict('Dataset', {
            'force':'bool',
            'name':'str',
            'key':'str',
            'passphrase':'str',
    })
    DatasetDelete = typing.TypedDict('DatasetDelete', {
            'recursive':'bool',
            'force':'bool',
    })
    DatasetEncryptionSummary = typing.TypedDict('DatasetEncryptionSummary', {
            'name':'str',
            'key_format':'str',
            'key_present_in_database':'bool',
            'valid_key':'bool',
            'locked':'bool',
            'unlock_error':'typing.Optional[str]',
            'unlock_successful':'bool',
    })
    Dataset_ = typing.TypedDict('Dataset_', {
            'force':'bool',
            'name':'str',
            'key':'str',
            'passphrase':'str',
            'recursive':'bool',
    })
    class Deduplication(str,Enum):
        ON = 'ON'
        VERIFY = 'VERIFY'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    Deduplication_ = typing.TypedDict('Deduplication_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithm = typing.TypedDict('EncryptionAlgorithm', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithmChoices = typing.TypedDict('EncryptionAlgorithmChoices', {
            'AES-128-CCM':'typing.Literal["AES-128-CCM"]',
            'AES-192-CCM':'typing.Literal["AES-192-CCM"]',
            'AES-256-CCM':'typing.Literal["AES-256-CCM"]',
            'AES-128-GCM':'typing.Literal["AES-128-GCM"]',
            'AES-192-GCM':'typing.Literal["AES-192-GCM"]',
            'AES-256-GCM':'typing.Literal["AES-256-GCM"]',
    })
    EncryptionOptions = typing.TypedDict('EncryptionOptions', {
            'generate_key':'bool',
            'pbkdf2iters':'int',
            'algorithm':'Algorithm',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    EncryptionRootSummaryOptions = typing.TypedDict('EncryptionRootSummaryOptions', {
            'key_file':'bool',
            'force':'bool',
            'datasets':'list[Dataset]',
    })
    class Exec(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    Exec_ = typing.TypedDict('Exec_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Flags = typing.TypedDict('Flags', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'BASIC_',
    })
    KeyFormat = typing.TypedDict('KeyFormat', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    LockOptions = typing.TypedDict('LockOptions', {
            'force_umount':'bool',
    })
    Managedby = typing.TypedDict('Managedby', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Nfs4Ace = typing.TypedDict('Nfs4Ace', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type_',
            'perms':'Perms',
            'flags':'Flags',
    })
    Options = typing.TypedDict('Options', {
            'set_default_acl':'bool',
            'stripacl':'bool',
            'recursive':'bool',
            'traverse':'bool',
    })
    Origin = typing.TypedDict('Origin', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Pbkdf2iters = typing.TypedDict('Pbkdf2iters', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Perms = typing.TypedDict('Perms', {
            'READ_DATA':'bool',
            'WRITE_DATA':'bool',
            'APPEND_DATA':'bool',
            'READ_NAMED_ATTRS':'bool',
            'WRITE_NAMED_ATTRS':'bool',
            'EXECUTE':'bool',
            'DELETE_CHILD':'bool',
            'READ_ATTRIBUTES':'bool',
            'WRITE_ATTRIBUTES':'bool',
            'DELETE':'bool',
            'READ_ACL':'bool',
            'WRITE_ACL':'bool',
            'WRITE_OWNER':'bool',
            'SYNCHRONIZE':'bool',
            'BASIC':'BASIC',
    })
    Perms_ = typing.TypedDict('Perms_', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    PoolDatasetCreate = typing.TypedDict('PoolDatasetCreate', {
            'name':'str',
            'type':'Type',
            'volsize':'int',
            'volblocksize':'Volblocksize',
            'sparse':'bool',
            'force_size':'bool',
            'comments':'typing.Union[str, typing.Literal["INHERIT"]]',
            'sync':'Sync',
            'snapdev':'Snapdev',
            'compression':'Compression',
            'atime':'Atime',
            'exec':'Exec',
            'managedby':'typing.Union[str, typing.Literal["INHERIT"]]',
            'quota':'typing.Optional[int]',
            'quota_warning':'typing.Union[int, typing.Literal["INHERIT"]]',
            'quota_critical':'typing.Union[int, typing.Literal["INHERIT"]]',
            'refquota':'typing.Optional[int]',
            'refquota_warning':'typing.Union[int, typing.Literal["INHERIT"]]',
            'refquota_critical':'typing.Union[int, typing.Literal["INHERIT"]]',
            'reservation':'int',
            'refreservation':'int',
            'special_small_block_size':'typing.Union[int, typing.Literal["INHERIT"]]',
            'copies':'typing.Union[int, typing.Literal["INHERIT"]]',
            'snapdir':'Snapdir',
            'deduplication':'Deduplication',
            'checksum':'Checksum',
            'readonly':'Readonly',
            'recordsize':'typing.Union[str, typing.Literal["INHERIT"]]',
            'casesensitivity':'Casesensitivity',
            'aclmode':'Aclmode',
            'acltype':'Acltype',
            'share_type':'ShareType',
            'xattr':'Xattr',
            'encryption_options':'EncryptionOptions',
            'encryption':'bool',
            'inherit_encryption':'bool',
            'user_properties':'list[UserProperty]',
            'create_ancestors':'bool',
    })
    PoolDatasetCreateReturns = typing.TypedDict('PoolDatasetCreateReturns', {
            'id':'str',
            'type':'str',
            'name':'str',
            'pool':'str',
            'encrypted':'bool',
            'encryption_root':'typing.Optional[str]',
            'key_loaded':'typing.Optional[bool]',
            'children':'list',
            'user_properties':'dict[str]',
            'locked':'bool',
            'comments':'Comments',
            'quota_warning':'QuotaWarning',
            'quota_critical':'QuotaCritical',
            'refquota_warning':'RefquotaWarning',
            'refquota_critical':'RefquotaCritical',
            'managedby':'Managedby',
            'deduplication':'Deduplication_',
            'aclmode':'Aclmode_',
            'acltype':'Acltype_',
            'xattr':'Xattr_',
            'atime':'Atime_',
            'casesensitivity':'Casesensitivity_',
            'checksum':'Checksum_',
            'exec':'Exec_',
            'sync':'Sync_',
            'compression':'Compression_',
            'compressratio':'Compressratio',
            'origin':'Origin',
            'quota':'Quota',
            'refquota':'Refquota',
            'reservation':'Reservation',
            'refreservation':'Refreservation',
            'copies':'Copies',
            'snapdir':'Snapdir_',
            'readonly':'Readonly_',
            'recordsize':'Recordsize',
            'sparse':'Sparse',
            'volsize':'Volsize',
            'volblocksize':'Volblocksize_',
            'key_format':'KeyFormat',
            'encryption_algorithm':'EncryptionAlgorithm',
            'used':'Used',
            'usedbychildren':'Usedbychildren',
            'usedbydataset':'Usedbydataset',
            'usedbyrefreservation':'Usedbyrefreservation',
            'usedbysnapshots':'Usedbysnapshots',
            'available':'Available',
            'special_small_block_size':'SpecialSmallBlockSize',
            'pbkdf2iters':'Pbkdf2iters',
            'creation':'Creation',
            'snapdev':'Snapdev_',
            'mountpoint':'typing.Optional[str]',
    })
    PoolDatasetEntry = typing.TypedDict('PoolDatasetEntry', {
            'id':'str',
            'type':'str',
            'name':'str',
            'pool':'str',
            'encrypted':'bool',
            'encryption_root':'typing.Optional[str]',
            'key_loaded':'typing.Optional[bool]',
            'children':'list',
            'user_properties':'dict[str]',
            'locked':'bool',
            'comments':'Comments',
            'quota_warning':'QuotaWarning',
            'quota_critical':'QuotaCritical',
            'refquota_warning':'RefquotaWarning',
            'refquota_critical':'RefquotaCritical',
            'managedby':'Managedby',
            'deduplication':'Deduplication_',
            'aclmode':'Aclmode_',
            'acltype':'Acltype_',
            'xattr':'Xattr_',
            'atime':'Atime_',
            'casesensitivity':'Casesensitivity_',
            'checksum':'Checksum_',
            'exec':'Exec_',
            'sync':'Sync_',
            'compression':'Compression_',
            'compressratio':'Compressratio',
            'origin':'Origin',
            'quota':'Quota',
            'refquota':'Refquota',
            'reservation':'Reservation',
            'refreservation':'Refreservation',
            'copies':'Copies',
            'snapdir':'Snapdir_',
            'readonly':'Readonly_',
            'recordsize':'Recordsize',
            'sparse':'Sparse',
            'volsize':'Volsize',
            'volblocksize':'Volblocksize_',
            'key_format':'KeyFormat',
            'encryption_algorithm':'EncryptionAlgorithm',
            'used':'Used',
            'usedbychildren':'Usedbychildren',
            'usedbydataset':'Usedbydataset',
            'usedbyrefreservation':'Usedbyrefreservation',
            'usedbysnapshots':'Usedbysnapshots',
            'available':'Available',
            'special_small_block_size':'SpecialSmallBlockSize',
            'pbkdf2iters':'Pbkdf2iters',
            'creation':'Creation',
            'snapdev':'Snapdev_',
            'mountpoint':'typing.Optional[str]',
    })
    PoolDatasetPermission = typing.TypedDict('PoolDatasetPermission', {
            'user':'str',
            'group':'str',
            'mode':'typing.Optional[str]',
            'acl':'typing.Union[list[Nfs4Ace], list[Posix1eAce]]',
            'options':'Options',
    })
    PoolDatasetUpdate = typing.TypedDict('PoolDatasetUpdate', {
            'volsize':'int',
            'force_size':'bool',
            'comments':'typing.Union[str, typing.Literal["INHERIT"]]',
            'sync':'Sync',
            'snapdev':'Snapdev',
            'compression':'Compression',
            'atime':'Atime',
            'exec':'Exec',
            'managedby':'typing.Union[str, typing.Literal["INHERIT"]]',
            'quota':'typing.Optional[int]',
            'quota_warning':'typing.Union[int, typing.Literal["INHERIT"]]',
            'quota_critical':'typing.Union[int, typing.Literal["INHERIT"]]',
            'refquota':'typing.Optional[int]',
            'refquota_warning':'typing.Union[int, typing.Literal["INHERIT"]]',
            'refquota_critical':'typing.Union[int, typing.Literal["INHERIT"]]',
            'reservation':'int',
            'refreservation':'int',
            'special_small_block_size':'typing.Union[int, typing.Literal["INHERIT"]]',
            'copies':'typing.Union[int, typing.Literal["INHERIT"]]',
            'snapdir':'Snapdir',
            'deduplication':'Deduplication',
            'checksum':'Checksum',
            'readonly':'Readonly',
            'recordsize':'typing.Union[str, typing.Literal["INHERIT"]]',
            'aclmode':'Aclmode',
            'acltype':'Acltype',
            'xattr':'Xattr',
            'user_properties':'list[UserProperty]',
            'create_ancestors':'bool',
            'user_properties_update':'list[UserProperty_]',
    })
    PoolDatasetUpdateReturns = typing.TypedDict('PoolDatasetUpdateReturns', {
            'id':'str',
            'type':'str',
            'name':'str',
            'pool':'str',
            'encrypted':'bool',
            'encryption_root':'typing.Optional[str]',
            'key_loaded':'typing.Optional[bool]',
            'children':'list',
            'user_properties':'dict[str]',
            'locked':'bool',
            'comments':'Comments',
            'quota_warning':'QuotaWarning',
            'quota_critical':'QuotaCritical',
            'refquota_warning':'RefquotaWarning',
            'refquota_critical':'RefquotaCritical',
            'managedby':'Managedby',
            'deduplication':'Deduplication_',
            'aclmode':'Aclmode_',
            'acltype':'Acltype_',
            'xattr':'Xattr_',
            'atime':'Atime_',
            'casesensitivity':'Casesensitivity_',
            'checksum':'Checksum_',
            'exec':'Exec_',
            'sync':'Sync_',
            'compression':'Compression_',
            'compressratio':'Compressratio',
            'origin':'Origin',
            'quota':'Quota',
            'refquota':'Refquota',
            'reservation':'Reservation',
            'refreservation':'Refreservation',
            'copies':'Copies',
            'snapdir':'Snapdir_',
            'readonly':'Readonly_',
            'recordsize':'Recordsize',
            'sparse':'Sparse',
            'volsize':'Volsize',
            'volblocksize':'Volblocksize_',
            'key_format':'KeyFormat',
            'encryption_algorithm':'EncryptionAlgorithm',
            'used':'Used',
            'usedbychildren':'Usedbychildren',
            'usedbydataset':'Usedbydataset',
            'usedbyrefreservation':'Usedbyrefreservation',
            'usedbysnapshots':'Usedbysnapshots',
            'available':'Available',
            'special_small_block_size':'SpecialSmallBlockSize',
            'pbkdf2iters':'Pbkdf2iters',
            'creation':'Creation',
            'snapdev':'Snapdev_',
            'mountpoint':'typing.Optional[str]',
    })
    Posix1eAce = typing.TypedDict('Posix1eAce', {
            'default':'bool',
            'tag':'Tag_',
            'id':'int',
            'perms':'Perms_',
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
    Quota = typing.TypedDict('Quota', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaCritical = typing.TypedDict('QuotaCritical', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaEntry = typing.TypedDict('QuotaEntry', {
            'quota_type':'QuotaType_',
            'id':'str',
            'quota_value':'typing.Optional[int]',
    })
    class QuotaType(str,Enum):
        USER = 'USER'
        GROUP = 'GROUP'
        DATASET = 'DATASET'
        PROJECT = 'PROJECT'
        ...
    class QuotaType_(str,Enum):
        DATASET = 'DATASET'
        USER = 'USER'
        USEROBJ = 'USEROBJ'
        GROUP = 'GROUP'
        GROUPOBJ = 'GROUPOBJ'
        ...
    QuotaWarning = typing.TypedDict('QuotaWarning', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Readonly(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    Readonly_ = typing.TypedDict('Readonly_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Recordsize = typing.TypedDict('Recordsize', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refquota = typing.TypedDict('Refquota', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaCritical = typing.TypedDict('RefquotaCritical', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaWarning = typing.TypedDict('RefquotaWarning', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refreservation = typing.TypedDict('Refreservation', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Reservation = typing.TypedDict('Reservation', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class ShareType(str,Enum):
        GENERIC = 'GENERIC'
        SMB = 'SMB'
        APPS = 'APPS'
        ...
    class Snapdev(str,Enum):
        HIDDEN = 'HIDDEN'
        VISIBLE = 'VISIBLE'
        INHERIT = 'INHERIT'
        ...
    Snapdev_ = typing.TypedDict('Snapdev_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Snapdir(str,Enum):
        VISIBLE = 'VISIBLE'
        HIDDEN = 'HIDDEN'
        INHERIT = 'INHERIT'
        ...
    Snapdir_ = typing.TypedDict('Snapdir_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SnapshotSpec = typing.TypedDict('SnapshotSpec', {
            'start':'str',
            'end':'str',
    })
    Snapshots = typing.TypedDict('Snapshots', {
            'all':'bool',
            'recursive':'bool',
            'snapshots':'list[SnapshotSpec]',
    })
    Sparse = typing.TypedDict('Sparse', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SpecialSmallBlockSize = typing.TypedDict('SpecialSmallBlockSize', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Sync(str,Enum):
        STANDARD = 'STANDARD'
        ALWAYS = 'ALWAYS'
        DISABLED = 'DISABLED'
        INHERIT = 'INHERIT'
        ...
    Sync_ = typing.TypedDict('Sync_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Tag(str,Enum):
        Owner = 'owner@'
        Group = 'group@'
        Everyone = 'everyone@'
        USER = 'USER'
        GROUP = 'GROUP'
        ...
    class Tag_(str,Enum):
        USEROBJ = 'USER_OBJ'
        GROUPOBJ = 'GROUP_OBJ'
        USER = 'USER'
        GROUP = 'GROUP'
        OTHER = 'OTHER'
        MASK = 'MASK'
        ...
    class Type(str,Enum):
        FILESYSTEM = 'FILESYSTEM'
        VOLUME = 'VOLUME'
        ...
    class Type_(str,Enum):
        ALLOW = 'ALLOW'
        DENY = 'DENY'
        ...
    Unlock = typing.TypedDict('Unlock', {
            'unlocked':'list[str]',
            'failed':'dict[str]',
    })
    UnlockOptions = typing.TypedDict('UnlockOptions', {
            'force':'bool',
            'key_file':'bool',
            'recursive':'bool',
            'toggle_attachments':'bool',
            'datasets':'list[Dataset_]',
    })
    Used = typing.TypedDict('Used', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbychildren = typing.TypedDict('Usedbychildren', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbydataset = typing.TypedDict('Usedbydataset', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbyrefreservation = typing.TypedDict('Usedbyrefreservation', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbysnapshots = typing.TypedDict('Usedbysnapshots', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    UserProperty = typing.TypedDict('UserProperty', {
            'key':'str',
            'value':'str',
    })
    UserProperty_ = typing.TypedDict('UserProperty_', {
            'key':'str',
            'value':'str',
            'remove':'bool',
    })
    class Volblocksize(str,Enum):
        _512 = '512'
        _512B = '512B'
        _1K = '1K'
        _2K = '2K'
        _4K = '4K'
        _8K = '8K'
        _16K = '16K'
        _32K = '32K'
        _64K = '64K'
        _128K = '128K'
        ...
    Volblocksize_ = typing.TypedDict('Volblocksize_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volsize = typing.TypedDict('Volsize', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Xattr(str,Enum):
        ON = 'ON'
        SA = 'SA'
        INHERIT = 'INHERIT'
        ...
    Xattr_ = typing.TypedDict('Xattr_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
