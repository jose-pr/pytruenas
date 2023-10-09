
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class PoolDataset(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['pool.dataset']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def attachments(self, 
        id:'str',
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
        id:'str',
        change_key_options:'ChangeKeyOptions'={},
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
        pool_dataset_create:'PoolDatasetCreate'={},
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
        id:'str',
        dataset_delete:'DatasetDelete'={},
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
        name:'str',
        snapshots:'Snapshots'={},
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
        id:'str',
        encryption_root_summary_options:'EncryptionRootSummaryOptions'={},
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
        id:'str',
        download:'bool'=False,
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
        id:'str',
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
        id:'int',
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
    @typing.overload
    def get_quota(self, 
        ds:'str',
        quota_type:'QuotaType',
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
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
        id:'str',
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
        id:'str',
        lock_options:'LockOptions'={},
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
        dataset:'str',
        raise:'bool'=True,
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
        id:'str',
        pool_dataset_permission:'PoolDatasetPermission'={},
    /) -> 'PoolDatasetPermission_': 
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
        PoolDatasetPermission_:
            pool_dataset_permission
        """
        ...
    @typing.overload
    def processes(self, 
        id:'str',
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
        id:'str',
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
        query_filters:'list[list]'=[],
        query_options:'QueryOptions_'={},
    /) -> 'typing.Union[list[PoolDatasetEntry], PoolDatasetEntry_, int, PoolDatasetEntry__]': 
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
        typing.Union[list[PoolDatasetEntry], PoolDatasetEntry_, int, PoolDatasetEntry__]:
            
        """
        ...
    @typing.overload
    def recommended_zvol_blocksize(self, 
        pool:'str',
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
        pool_name:'typing.Optional[str]'=None,
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
        ds:'str',
        quotas:'list[QuotaEntry]'=[{"quota_type": "USER", "id": "0", "quota_value": 0}],
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
        dataset:'str',
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
        id:'str',
        unlock_options:'UnlockOptions'={},
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
        dataset:'str',
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
        id:'str',
        pool_dataset_update:'PoolDatasetUpdate'={},
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
    Attachment = typing.TypedDict('Attachment', {
            'type':'str',
            'service':'typing.Optional[str]',
            'attachments':'list[str]',
    })
    ChangeKeyOptions = typing.TypedDict('ChangeKeyOptions', {
            'generate_key':'bool',
            'key_file':'bool',
            'pbkdf2iters':'int',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    class ON(str,Enum):
        ON = 'ON'
        ...
    class FLETCHER2(str,Enum):
        FLETCHER2 = 'FLETCHER2'
        ...
    class FLETCHER4(str,Enum):
        FLETCHER4 = 'FLETCHER4'
        ...
    class SHA256(str,Enum):
        SHA256 = 'SHA256'
        ...
    class SHA512(str,Enum):
        SHA512 = 'SHA512'
        ...
    class SKEIN(str,Enum):
        SKEIN = 'SKEIN'
        ...
    class EDONR(str,Enum):
        EDONR = 'EDONR'
        ...
    ChecksumChoices = typing.TypedDict('ChecksumChoices', {
            'ON':'ON',
            'FLETCHER2':'FLETCHER2',
            'FLETCHER4':'FLETCHER4',
            'SHA256':'SHA256',
            'SHA512':'SHA512',
            'SKEIN':'SKEIN',
            'EDONR':'EDONR',
    })
    class OFF(str,Enum):
        OFF = 'OFF'
        ...
    class LZ4(str,Enum):
        LZ4 = 'LZ4'
        ...
    class GZIP(str,Enum):
        GZIP = 'GZIP'
        ...
    class GZIP1(str,Enum):
        GZIP1 = 'GZIP-1'
        ...
    class GZIP9(str,Enum):
        GZIP9 = 'GZIP-9'
        ...
    class ZSTD(str,Enum):
        ZSTD = 'ZSTD'
        ...
    class ZSTDFAST(str,Enum):
        ZSTDFAST = 'ZSTD-FAST'
        ...
    class ZLE(str,Enum):
        ZLE = 'ZLE'
        ...
    class LZJB(str,Enum):
        LZJB = 'LZJB'
        ...
    class ZSTD1(str,Enum):
        ZSTD1 = 'ZSTD-1'
        ...
    class ZSTD2(str,Enum):
        ZSTD2 = 'ZSTD-2'
        ...
    class ZSTD3(str,Enum):
        ZSTD3 = 'ZSTD-3'
        ...
    class ZSTD4(str,Enum):
        ZSTD4 = 'ZSTD-4'
        ...
    class ZSTD5(str,Enum):
        ZSTD5 = 'ZSTD-5'
        ...
    class ZSTD6(str,Enum):
        ZSTD6 = 'ZSTD-6'
        ...
    class ZSTD7(str,Enum):
        ZSTD7 = 'ZSTD-7'
        ...
    class ZSTD8(str,Enum):
        ZSTD8 = 'ZSTD-8'
        ...
    class ZSTD9(str,Enum):
        ZSTD9 = 'ZSTD-9'
        ...
    class ZSTD10(str,Enum):
        ZSTD10 = 'ZSTD-10'
        ...
    class ZSTD11(str,Enum):
        ZSTD11 = 'ZSTD-11'
        ...
    class ZSTD12(str,Enum):
        ZSTD12 = 'ZSTD-12'
        ...
    class ZSTD13(str,Enum):
        ZSTD13 = 'ZSTD-13'
        ...
    class ZSTD14(str,Enum):
        ZSTD14 = 'ZSTD-14'
        ...
    class ZSTD15(str,Enum):
        ZSTD15 = 'ZSTD-15'
        ...
    class ZSTD16(str,Enum):
        ZSTD16 = 'ZSTD-16'
        ...
    class ZSTD17(str,Enum):
        ZSTD17 = 'ZSTD-17'
        ...
    class ZSTD18(str,Enum):
        ZSTD18 = 'ZSTD-18'
        ...
    class ZSTD19(str,Enum):
        ZSTD19 = 'ZSTD-19'
        ...
    class ZSTDFAST1(str,Enum):
        ZSTDFAST1 = 'ZSTD-FAST-1'
        ...
    class ZSTDFAST2(str,Enum):
        ZSTDFAST2 = 'ZSTD-FAST-2'
        ...
    class ZSTDFAST3(str,Enum):
        ZSTDFAST3 = 'ZSTD-FAST-3'
        ...
    class ZSTDFAST4(str,Enum):
        ZSTDFAST4 = 'ZSTD-FAST-4'
        ...
    class ZSTDFAST5(str,Enum):
        ZSTDFAST5 = 'ZSTD-FAST-5'
        ...
    class ZSTDFAST6(str,Enum):
        ZSTDFAST6 = 'ZSTD-FAST-6'
        ...
    class ZSTDFAST7(str,Enum):
        ZSTDFAST7 = 'ZSTD-FAST-7'
        ...
    class ZSTDFAST8(str,Enum):
        ZSTDFAST8 = 'ZSTD-FAST-8'
        ...
    class ZSTDFAST9(str,Enum):
        ZSTDFAST9 = 'ZSTD-FAST-9'
        ...
    class ZSTDFAST10(str,Enum):
        ZSTDFAST10 = 'ZSTD-FAST-10'
        ...
    class ZSTDFAST20(str,Enum):
        ZSTDFAST20 = 'ZSTD-FAST-20'
        ...
    class ZSTDFAST30(str,Enum):
        ZSTDFAST30 = 'ZSTD-FAST-30'
        ...
    class ZSTDFAST40(str,Enum):
        ZSTDFAST40 = 'ZSTD-FAST-40'
        ...
    class ZSTDFAST50(str,Enum):
        ZSTDFAST50 = 'ZSTD-FAST-50'
        ...
    class ZSTDFAST60(str,Enum):
        ZSTDFAST60 = 'ZSTD-FAST-60'
        ...
    class ZSTDFAST70(str,Enum):
        ZSTDFAST70 = 'ZSTD-FAST-70'
        ...
    class ZSTDFAST80(str,Enum):
        ZSTDFAST80 = 'ZSTD-FAST-80'
        ...
    class ZSTDFAST90(str,Enum):
        ZSTDFAST90 = 'ZSTD-FAST-90'
        ...
    class ZSTDFAST100(str,Enum):
        ZSTDFAST100 = 'ZSTD-FAST-100'
        ...
    class ZSTDFAST500(str,Enum):
        ZSTDFAST500 = 'ZSTD-FAST-500'
        ...
    class ZSTDFAST1000(str,Enum):
        ZSTDFAST1000 = 'ZSTD-FAST-1000'
        ...
    CompressionChoices = typing.TypedDict('CompressionChoices', {
            'OFF':'OFF',
            'LZ4':'LZ4',
            'GZIP':'GZIP',
            'GZIP-1':'GZIP1',
            'GZIP-9':'GZIP9',
            'ZSTD':'ZSTD',
            'ZSTD-FAST':'ZSTDFAST',
            'ZLE':'ZLE',
            'LZJB':'LZJB',
            'ZSTD-1':'ZSTD1',
            'ZSTD-2':'ZSTD2',
            'ZSTD-3':'ZSTD3',
            'ZSTD-4':'ZSTD4',
            'ZSTD-5':'ZSTD5',
            'ZSTD-6':'ZSTD6',
            'ZSTD-7':'ZSTD7',
            'ZSTD-8':'ZSTD8',
            'ZSTD-9':'ZSTD9',
            'ZSTD-10':'ZSTD10',
            'ZSTD-11':'ZSTD11',
            'ZSTD-12':'ZSTD12',
            'ZSTD-13':'ZSTD13',
            'ZSTD-14':'ZSTD14',
            'ZSTD-15':'ZSTD15',
            'ZSTD-16':'ZSTD16',
            'ZSTD-17':'ZSTD17',
            'ZSTD-18':'ZSTD18',
            'ZSTD-19':'ZSTD19',
            'ZSTD-FAST-1':'ZSTDFAST1',
            'ZSTD-FAST-2':'ZSTDFAST2',
            'ZSTD-FAST-3':'ZSTDFAST3',
            'ZSTD-FAST-4':'ZSTDFAST4',
            'ZSTD-FAST-5':'ZSTDFAST5',
            'ZSTD-FAST-6':'ZSTDFAST6',
            'ZSTD-FAST-7':'ZSTDFAST7',
            'ZSTD-FAST-8':'ZSTDFAST8',
            'ZSTD-FAST-9':'ZSTDFAST9',
            'ZSTD-FAST-10':'ZSTDFAST10',
            'ZSTD-FAST-20':'ZSTDFAST20',
            'ZSTD-FAST-30':'ZSTDFAST30',
            'ZSTD-FAST-40':'ZSTDFAST40',
            'ZSTD-FAST-50':'ZSTDFAST50',
            'ZSTD-FAST-60':'ZSTDFAST60',
            'ZSTD-FAST-70':'ZSTDFAST70',
            'ZSTD-FAST-80':'ZSTDFAST80',
            'ZSTD-FAST-90':'ZSTDFAST90',
            'ZSTD-FAST-100':'ZSTDFAST100',
            'ZSTD-FAST-500':'ZSTDFAST500',
            'ZSTD-FAST-1000':'ZSTDFAST1000',
    })
    class Type(str,Enum):
        FILESYSTEM = 'FILESYSTEM'
        VOLUME = 'VOLUME'
        ...
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
    class Object(str,Enum):
        INHERIT = 'INHERIT'
        ...
    class Sync(str,Enum):
        STANDARD = 'STANDARD'
        ALWAYS = 'ALWAYS'
        DISABLED = 'DISABLED'
        ...
    class Snapdev(str,Enum):
        HIDDEN = 'HIDDEN'
        VISIBLE = 'VISIBLE'
        ...
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
        ...
    class Atime(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        ...
    class Exec(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        ...
    class Snapdir(str,Enum):
        VISIBLE = 'VISIBLE'
        HIDDEN = 'HIDDEN'
        ...
    class Deduplication(str,Enum):
        ON = 'ON'
        VERIFY = 'VERIFY'
        OFF = 'OFF'
        ...
    class Checksum(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        FLETCHER2 = 'FLETCHER2'
        FLETCHER4 = 'FLETCHER4'
        SHA256 = 'SHA256'
        SHA512 = 'SHA512'
        SKEIN = 'SKEIN'
        EDONR = 'EDONR'
        ...
    class Readonly(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        ...
    class Casesensitivity(str,Enum):
        SENSITIVE = 'SENSITIVE'
        INSENSITIVE = 'INSENSITIVE'
        ...
    class Aclmode(str,Enum):
        PASSTHROUGH = 'PASSTHROUGH'
        RESTRICTED = 'RESTRICTED'
        DISCARD = 'DISCARD'
        ...
    class Acltype(str,Enum):
        OFF = 'OFF'
        NFSV4 = 'NFSV4'
        POSIX = 'POSIX'
        ...
    class ShareType(str,Enum):
        GENERIC = 'GENERIC'
        SMB = 'SMB'
        APPS = 'APPS'
        ...
    class Xattr(str,Enum):
        ON = 'ON'
        SA = 'SA'
        ...
    class Algorithm(str,Enum):
        AES128CCM = 'AES-128-CCM'
        AES192CCM = 'AES-192-CCM'
        AES256CCM = 'AES-256-CCM'
        AES128GCM = 'AES-128-GCM'
        AES192GCM = 'AES-192-GCM'
        AES256GCM = 'AES-256-GCM'
        ...
    EncryptionOptions = typing.TypedDict('EncryptionOptions', {
            'generate_key':'bool',
            'pbkdf2iters':'int',
            'algorithm':'Algorithm',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    UserProperty = typing.TypedDict('UserProperty', {
            'key':'str',
            'value':'str',
    })
    PoolDatasetCreate = typing.TypedDict('PoolDatasetCreate', {
            'name':'str',
            'type':'Type',
            'volsize':'int',
            'volblocksize':'Volblocksize',
            'sparse':'bool',
            'force_size':'bool',
            'comments':'typing.Union[str, Object]',
            'sync':'typing.Union[str, Object]',
            'snapdev':'typing.Union[str, Object]',
            'compression':'typing.Union[str, Object]',
            'atime':'typing.Union[str, Object]',
            'exec':'typing.Union[str, Object]',
            'managedby':'typing.Union[str, Object]',
            'quota':'typing.Optional[int]',
            'quota_warning':'typing.Union[int, Object]',
            'quota_critical':'typing.Union[int, Object]',
            'refquota':'typing.Optional[int]',
            'refquota_warning':'typing.Union[int, Object]',
            'refquota_critical':'typing.Union[int, Object]',
            'reservation':'int',
            'refreservation':'int',
            'special_small_block_size':'typing.Union[int, Object]',
            'copies':'typing.Union[int, Object]',
            'snapdir':'typing.Union[str, Object]',
            'deduplication':'typing.Union[str, Object]',
            'checksum':'typing.Union[str, Object]',
            'readonly':'typing.Union[str, Object]',
            'recordsize':'typing.Union[str, Object]',
            'casesensitivity':'typing.Union[str, Object]',
            'aclmode':'typing.Union[str, Object]',
            'acltype':'typing.Union[str, Object]',
            'share_type':'ShareType',
            'xattr':'typing.Union[str, Object]',
            'encryption_options':'EncryptionOptions',
            'encryption':'bool',
            'inherit_encryption':'bool',
            'user_properties':'list[UserProperty]',
            'create_ancestors':'bool',
    })
    Comments = typing.TypedDict('Comments', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaWarning = typing.TypedDict('QuotaWarning', {
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
    RefquotaWarning = typing.TypedDict('RefquotaWarning', {
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
    Managedby = typing.TypedDict('Managedby', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Deduplication_ = typing.TypedDict('Deduplication_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Aclmode_ = typing.TypedDict('Aclmode_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Acltype_ = typing.TypedDict('Acltype_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Xattr_ = typing.TypedDict('Xattr_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Atime_ = typing.TypedDict('Atime_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Casesensitivity_ = typing.TypedDict('Casesensitivity_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Checksum_ = typing.TypedDict('Checksum_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Exec_ = typing.TypedDict('Exec_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sync_ = typing.TypedDict('Sync_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
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
    Origin = typing.TypedDict('Origin', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Quota = typing.TypedDict('Quota', {
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
    Reservation = typing.TypedDict('Reservation', {
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
    Copies = typing.TypedDict('Copies', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdir_ = typing.TypedDict('Snapdir_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
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
    Sparse = typing.TypedDict('Sparse', {
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
    Volblocksize_ = typing.TypedDict('Volblocksize_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    KeyFormat = typing.TypedDict('KeyFormat', {
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
    Available = typing.TypedDict('Available', {
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
    Pbkdf2iters = typing.TypedDict('Pbkdf2iters', {
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
    Snapdev_ = typing.TypedDict('Snapdev_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
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
    DatasetDelete = typing.TypedDict('DatasetDelete', {
            'recursive':'bool',
            'force':'bool',
    })
    SnapshotSpec = typing.TypedDict('SnapshotSpec', {
            'start':'str',
            'end':'str',
    })
    Snapshots = typing.TypedDict('Snapshots', {
            'all':'bool',
            'recursive':'bool',
            'snapshots':'list[typing.Union[SnapshotSpec, str]]',
    })
    class AES128CCM(str,Enum):
        AES128CCM = 'AES-128-CCM'
        ...
    class AES192CCM(str,Enum):
        AES192CCM = 'AES-192-CCM'
        ...
    class AES256CCM(str,Enum):
        AES256CCM = 'AES-256-CCM'
        ...
    class AES128GCM(str,Enum):
        AES128GCM = 'AES-128-GCM'
        ...
    class AES192GCM(str,Enum):
        AES192GCM = 'AES-192-GCM'
        ...
    class AES256GCM(str,Enum):
        AES256GCM = 'AES-256-GCM'
        ...
    EncryptionAlgorithmChoices = typing.TypedDict('EncryptionAlgorithmChoices', {
            'AES-128-CCM':'AES128CCM',
            'AES-192-CCM':'AES192CCM',
            'AES-256-CCM':'AES256CCM',
            'AES-128-GCM':'AES128GCM',
            'AES-192-GCM':'AES192GCM',
            'AES-256-GCM':'AES256GCM',
    })
    Dataset = typing.TypedDict('Dataset', {
            'force':'bool',
            'name':'str',
            'key':'str',
            'passphrase':'str',
    })
    EncryptionRootSummaryOptions = typing.TypedDict('EncryptionRootSummaryOptions', {
            'key_file':'bool',
            'force':'bool',
            'datasets':'list[Dataset]',
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
    class QuotaType(str,Enum):
        USER = 'USER'
        GROUP = 'GROUP'
        DATASET = 'DATASET'
        PROJECT = 'PROJECT'
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
    LockOptions = typing.TypedDict('LockOptions', {
            'force_umount':'bool',
    })
    class Tag(str,Enum):
        Owner = 'owner@'
        Group = 'group@'
        Everyone = 'everyone@'
        USER = 'USER'
        GROUP = 'GROUP'
        ...
    class Type_(str,Enum):
        ALLOW = 'ALLOW'
        DENY = 'DENY'
        ...
    class BASIC(str,Enum):
        FULLCONTROL = 'FULL_CONTROL'
        MODIFY = 'MODIFY'
        READ = 'READ'
        TRAVERSE = 'TRAVERSE'
        ...
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
    class BASIC_(str,Enum):
        INHERIT = 'INHERIT'
        NOINHERIT = 'NOINHERIT'
        ...
    Flags = typing.TypedDict('Flags', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'BASIC_',
    })
    Nfs4Ace = typing.TypedDict('Nfs4Ace', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type_',
            'perms':'Perms',
            'flags':'Flags',
    })
    class Tag_(str,Enum):
        USEROBJ = 'USER_OBJ'
        GROUPOBJ = 'GROUP_OBJ'
        USER = 'USER'
        GROUP = 'GROUP'
        OTHER = 'OTHER'
        MASK = 'MASK'
        ...
    Perms_ = typing.TypedDict('Perms_', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Posix1eAce = typing.TypedDict('Posix1eAce', {
            'default':'bool',
            'tag':'Tag_',
            'id':'int',
            'perms':'Perms_',
    })
    Options = typing.TypedDict('Options', {
            'set_default_acl':'bool',
            'stripacl':'bool',
            'recursive':'bool',
            'traverse':'bool',
    })
    PoolDatasetPermission = typing.TypedDict('PoolDatasetPermission', {
            'user':'str',
            'group':'str',
            'mode':'typing.Optional[str]',
            'acl':'typing.Union[list[Nfs4Ace], list[Posix1eAce]]',
            'options':'Options',
    })
    Nfs4Ace_ = typing.TypedDict('Nfs4Ace_', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type_',
            'perms':'Perms',
            'flags':'Flags',
    })
    PoolDatasetPermission_ = typing.TypedDict('PoolDatasetPermission_', {
            'user':'str',
            'group':'str',
            'mode':'typing.Optional[str]',
            'acl':'typing.Union[list[Nfs4Ace_], list[Posix1eAce]]',
            'options':'Options',
    })
    Process = typing.TypedDict('Process', {
            'pid':'int',
            'name':'str',
            'service':'str',
            'cmdline':'str',
    })
    QueryOptions_ = typing.TypedDict('QueryOptions_', {
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
    Comments_ = typing.TypedDict('Comments_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaWarning_ = typing.TypedDict('QuotaWarning_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaCritical_ = typing.TypedDict('QuotaCritical_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaWarning_ = typing.TypedDict('RefquotaWarning_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaCritical_ = typing.TypedDict('RefquotaCritical_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Managedby_ = typing.TypedDict('Managedby_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Deduplication__ = typing.TypedDict('Deduplication__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Aclmode__ = typing.TypedDict('Aclmode__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Acltype__ = typing.TypedDict('Acltype__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Xattr__ = typing.TypedDict('Xattr__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Atime__ = typing.TypedDict('Atime__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Casesensitivity__ = typing.TypedDict('Casesensitivity__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Checksum__ = typing.TypedDict('Checksum__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Exec__ = typing.TypedDict('Exec__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sync__ = typing.TypedDict('Sync__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compression__ = typing.TypedDict('Compression__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compressratio_ = typing.TypedDict('Compressratio_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Origin_ = typing.TypedDict('Origin_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Quota_ = typing.TypedDict('Quota_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refquota_ = typing.TypedDict('Refquota_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Reservation_ = typing.TypedDict('Reservation_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refreservation_ = typing.TypedDict('Refreservation_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Copies_ = typing.TypedDict('Copies_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdir__ = typing.TypedDict('Snapdir__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Readonly__ = typing.TypedDict('Readonly__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Recordsize_ = typing.TypedDict('Recordsize_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sparse_ = typing.TypedDict('Sparse_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volsize_ = typing.TypedDict('Volsize_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volblocksize__ = typing.TypedDict('Volblocksize__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    KeyFormat_ = typing.TypedDict('KeyFormat_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithm_ = typing.TypedDict('EncryptionAlgorithm_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Used_ = typing.TypedDict('Used_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbychildren_ = typing.TypedDict('Usedbychildren_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbydataset_ = typing.TypedDict('Usedbydataset_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbyrefreservation_ = typing.TypedDict('Usedbyrefreservation_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbysnapshots_ = typing.TypedDict('Usedbysnapshots_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Available_ = typing.TypedDict('Available_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SpecialSmallBlockSize_ = typing.TypedDict('SpecialSmallBlockSize_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Pbkdf2iters_ = typing.TypedDict('Pbkdf2iters_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Creation_ = typing.TypedDict('Creation_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdev__ = typing.TypedDict('Snapdev__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
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
            'comments':'Comments_',
            'quota_warning':'QuotaWarning_',
            'quota_critical':'QuotaCritical_',
            'refquota_warning':'RefquotaWarning_',
            'refquota_critical':'RefquotaCritical_',
            'managedby':'Managedby_',
            'deduplication':'Deduplication__',
            'aclmode':'Aclmode__',
            'acltype':'Acltype__',
            'xattr':'Xattr__',
            'atime':'Atime__',
            'casesensitivity':'Casesensitivity__',
            'checksum':'Checksum__',
            'exec':'Exec__',
            'sync':'Sync__',
            'compression':'Compression__',
            'compressratio':'Compressratio_',
            'origin':'Origin_',
            'quota':'Quota_',
            'refquota':'Refquota_',
            'reservation':'Reservation_',
            'refreservation':'Refreservation_',
            'copies':'Copies_',
            'snapdir':'Snapdir__',
            'readonly':'Readonly__',
            'recordsize':'Recordsize_',
            'sparse':'Sparse_',
            'volsize':'Volsize_',
            'volblocksize':'Volblocksize__',
            'key_format':'KeyFormat_',
            'encryption_algorithm':'EncryptionAlgorithm_',
            'used':'Used_',
            'usedbychildren':'Usedbychildren_',
            'usedbydataset':'Usedbydataset_',
            'usedbyrefreservation':'Usedbyrefreservation_',
            'usedbysnapshots':'Usedbysnapshots_',
            'available':'Available_',
            'special_small_block_size':'SpecialSmallBlockSize_',
            'pbkdf2iters':'Pbkdf2iters_',
            'creation':'Creation_',
            'snapdev':'Snapdev__',
            'mountpoint':'typing.Optional[str]',
    })
    Comments__ = typing.TypedDict('Comments__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaWarning__ = typing.TypedDict('QuotaWarning__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaCritical__ = typing.TypedDict('QuotaCritical__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaWarning__ = typing.TypedDict('RefquotaWarning__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaCritical__ = typing.TypedDict('RefquotaCritical__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Managedby__ = typing.TypedDict('Managedby__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Deduplication___ = typing.TypedDict('Deduplication___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Aclmode___ = typing.TypedDict('Aclmode___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Acltype___ = typing.TypedDict('Acltype___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Xattr___ = typing.TypedDict('Xattr___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Atime___ = typing.TypedDict('Atime___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Casesensitivity___ = typing.TypedDict('Casesensitivity___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Checksum___ = typing.TypedDict('Checksum___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Exec___ = typing.TypedDict('Exec___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sync___ = typing.TypedDict('Sync___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compression___ = typing.TypedDict('Compression___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compressratio__ = typing.TypedDict('Compressratio__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Origin__ = typing.TypedDict('Origin__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Quota__ = typing.TypedDict('Quota__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refquota__ = typing.TypedDict('Refquota__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Reservation__ = typing.TypedDict('Reservation__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refreservation__ = typing.TypedDict('Refreservation__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Copies__ = typing.TypedDict('Copies__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdir___ = typing.TypedDict('Snapdir___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Readonly___ = typing.TypedDict('Readonly___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Recordsize__ = typing.TypedDict('Recordsize__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sparse__ = typing.TypedDict('Sparse__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volsize__ = typing.TypedDict('Volsize__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volblocksize___ = typing.TypedDict('Volblocksize___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    KeyFormat__ = typing.TypedDict('KeyFormat__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithm__ = typing.TypedDict('EncryptionAlgorithm__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Used__ = typing.TypedDict('Used__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbychildren__ = typing.TypedDict('Usedbychildren__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbydataset__ = typing.TypedDict('Usedbydataset__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbyrefreservation__ = typing.TypedDict('Usedbyrefreservation__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbysnapshots__ = typing.TypedDict('Usedbysnapshots__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Available__ = typing.TypedDict('Available__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SpecialSmallBlockSize__ = typing.TypedDict('SpecialSmallBlockSize__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Pbkdf2iters__ = typing.TypedDict('Pbkdf2iters__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Creation__ = typing.TypedDict('Creation__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdev___ = typing.TypedDict('Snapdev___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    PoolDatasetEntry_ = typing.TypedDict('PoolDatasetEntry_', {
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
            'comments':'Comments__',
            'quota_warning':'QuotaWarning__',
            'quota_critical':'QuotaCritical__',
            'refquota_warning':'RefquotaWarning__',
            'refquota_critical':'RefquotaCritical__',
            'managedby':'Managedby__',
            'deduplication':'Deduplication___',
            'aclmode':'Aclmode___',
            'acltype':'Acltype___',
            'xattr':'Xattr___',
            'atime':'Atime___',
            'casesensitivity':'Casesensitivity___',
            'checksum':'Checksum___',
            'exec':'Exec___',
            'sync':'Sync___',
            'compression':'Compression___',
            'compressratio':'Compressratio__',
            'origin':'Origin__',
            'quota':'Quota__',
            'refquota':'Refquota__',
            'reservation':'Reservation__',
            'refreservation':'Refreservation__',
            'copies':'Copies__',
            'snapdir':'Snapdir___',
            'readonly':'Readonly___',
            'recordsize':'Recordsize__',
            'sparse':'Sparse__',
            'volsize':'Volsize__',
            'volblocksize':'Volblocksize___',
            'key_format':'KeyFormat__',
            'encryption_algorithm':'EncryptionAlgorithm__',
            'used':'Used__',
            'usedbychildren':'Usedbychildren__',
            'usedbydataset':'Usedbydataset__',
            'usedbyrefreservation':'Usedbyrefreservation__',
            'usedbysnapshots':'Usedbysnapshots__',
            'available':'Available__',
            'special_small_block_size':'SpecialSmallBlockSize__',
            'pbkdf2iters':'Pbkdf2iters__',
            'creation':'Creation__',
            'snapdev':'Snapdev___',
            'mountpoint':'typing.Optional[str]',
    })
    Comments___ = typing.TypedDict('Comments___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaWarning___ = typing.TypedDict('QuotaWarning___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaCritical___ = typing.TypedDict('QuotaCritical___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaWarning___ = typing.TypedDict('RefquotaWarning___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaCritical___ = typing.TypedDict('RefquotaCritical___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Managedby___ = typing.TypedDict('Managedby___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Deduplication____ = typing.TypedDict('Deduplication____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Aclmode____ = typing.TypedDict('Aclmode____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Acltype____ = typing.TypedDict('Acltype____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Xattr____ = typing.TypedDict('Xattr____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Atime____ = typing.TypedDict('Atime____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Casesensitivity____ = typing.TypedDict('Casesensitivity____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Checksum____ = typing.TypedDict('Checksum____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Exec____ = typing.TypedDict('Exec____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sync____ = typing.TypedDict('Sync____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compression____ = typing.TypedDict('Compression____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compressratio___ = typing.TypedDict('Compressratio___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Origin___ = typing.TypedDict('Origin___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Quota___ = typing.TypedDict('Quota___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refquota___ = typing.TypedDict('Refquota___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Reservation___ = typing.TypedDict('Reservation___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refreservation___ = typing.TypedDict('Refreservation___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Copies___ = typing.TypedDict('Copies___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdir____ = typing.TypedDict('Snapdir____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Readonly____ = typing.TypedDict('Readonly____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Recordsize___ = typing.TypedDict('Recordsize___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sparse___ = typing.TypedDict('Sparse___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volsize___ = typing.TypedDict('Volsize___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volblocksize____ = typing.TypedDict('Volblocksize____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    KeyFormat___ = typing.TypedDict('KeyFormat___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithm___ = typing.TypedDict('EncryptionAlgorithm___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Used___ = typing.TypedDict('Used___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbychildren___ = typing.TypedDict('Usedbychildren___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbydataset___ = typing.TypedDict('Usedbydataset___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbyrefreservation___ = typing.TypedDict('Usedbyrefreservation___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbysnapshots___ = typing.TypedDict('Usedbysnapshots___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Available___ = typing.TypedDict('Available___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SpecialSmallBlockSize___ = typing.TypedDict('SpecialSmallBlockSize___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Pbkdf2iters___ = typing.TypedDict('Pbkdf2iters___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Creation___ = typing.TypedDict('Creation___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdev____ = typing.TypedDict('Snapdev____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    PoolDatasetEntry__ = typing.TypedDict('PoolDatasetEntry__', {
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
            'comments':'Comments___',
            'quota_warning':'QuotaWarning___',
            'quota_critical':'QuotaCritical___',
            'refquota_warning':'RefquotaWarning___',
            'refquota_critical':'RefquotaCritical___',
            'managedby':'Managedby___',
            'deduplication':'Deduplication____',
            'aclmode':'Aclmode____',
            'acltype':'Acltype____',
            'xattr':'Xattr____',
            'atime':'Atime____',
            'casesensitivity':'Casesensitivity____',
            'checksum':'Checksum____',
            'exec':'Exec____',
            'sync':'Sync____',
            'compression':'Compression____',
            'compressratio':'Compressratio___',
            'origin':'Origin___',
            'quota':'Quota___',
            'refquota':'Refquota___',
            'reservation':'Reservation___',
            'refreservation':'Refreservation___',
            'copies':'Copies___',
            'snapdir':'Snapdir____',
            'readonly':'Readonly____',
            'recordsize':'Recordsize___',
            'sparse':'Sparse___',
            'volsize':'Volsize___',
            'volblocksize':'Volblocksize____',
            'key_format':'KeyFormat___',
            'encryption_algorithm':'EncryptionAlgorithm___',
            'used':'Used___',
            'usedbychildren':'Usedbychildren___',
            'usedbydataset':'Usedbydataset___',
            'usedbyrefreservation':'Usedbyrefreservation___',
            'usedbysnapshots':'Usedbysnapshots___',
            'available':'Available___',
            'special_small_block_size':'SpecialSmallBlockSize___',
            'pbkdf2iters':'Pbkdf2iters___',
            'creation':'Creation___',
            'snapdev':'Snapdev____',
            'mountpoint':'typing.Optional[str]',
    })
    class QuotaType_(str,Enum):
        DATASET = 'DATASET'
        USER = 'USER'
        USEROBJ = 'USEROBJ'
        GROUP = 'GROUP'
        GROUPOBJ = 'GROUPOBJ'
        ...
    QuotaEntry = typing.TypedDict('QuotaEntry', {
            'quota_type':'QuotaType_',
            'id':'str',
            'quota_value':'typing.Optional[int]',
    })
    Dataset_ = typing.TypedDict('Dataset_', {
            'force':'bool',
            'name':'str',
            'key':'str',
            'passphrase':'str',
            'recursive':'bool',
    })
    UnlockOptions = typing.TypedDict('UnlockOptions', {
            'force':'bool',
            'key_file':'bool',
            'recursive':'bool',
            'toggle_attachments':'bool',
            'datasets':'list[Dataset_]',
    })
    Unlock = typing.TypedDict('Unlock', {
            'unlocked':'list[str]',
            'failed':'dict[str]',
    })
    UserProperty_ = typing.TypedDict('UserProperty_', {
            'key':'str',
            'value':'str',
            'remove':'bool',
    })
    PoolDatasetUpdate = typing.TypedDict('PoolDatasetUpdate', {
            'volsize':'int',
            'force_size':'bool',
            'comments':'typing.Union[str, Object]',
            'sync':'typing.Union[str, Object]',
            'snapdev':'typing.Union[str, Object]',
            'compression':'typing.Union[str, Object]',
            'atime':'typing.Union[str, Object]',
            'exec':'typing.Union[str, Object]',
            'managedby':'typing.Union[str, Object]',
            'quota':'typing.Optional[int]',
            'quota_warning':'typing.Union[int, Object]',
            'quota_critical':'typing.Union[int, Object]',
            'refquota':'typing.Optional[int]',
            'refquota_warning':'typing.Union[int, Object]',
            'refquota_critical':'typing.Union[int, Object]',
            'reservation':'int',
            'refreservation':'int',
            'special_small_block_size':'typing.Union[int, Object]',
            'copies':'typing.Union[int, Object]',
            'snapdir':'typing.Union[str, Object]',
            'deduplication':'typing.Union[str, Object]',
            'checksum':'typing.Union[str, Object]',
            'readonly':'typing.Union[str, Object]',
            'recordsize':'typing.Union[str, Object]',
            'aclmode':'typing.Union[str, Object]',
            'acltype':'typing.Union[str, Object]',
            'xattr':'typing.Union[str, Object]',
            'user_properties':'list[UserProperty]',
            'create_ancestors':'bool',
            'user_properties_update':'list[UserProperty_]',
    })
    Comments____ = typing.TypedDict('Comments____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaWarning____ = typing.TypedDict('QuotaWarning____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaCritical____ = typing.TypedDict('QuotaCritical____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaWarning____ = typing.TypedDict('RefquotaWarning____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaCritical____ = typing.TypedDict('RefquotaCritical____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Managedby____ = typing.TypedDict('Managedby____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Deduplication_____ = typing.TypedDict('Deduplication_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Aclmode_____ = typing.TypedDict('Aclmode_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Acltype_____ = typing.TypedDict('Acltype_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Xattr_____ = typing.TypedDict('Xattr_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Atime_____ = typing.TypedDict('Atime_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Casesensitivity_____ = typing.TypedDict('Casesensitivity_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Checksum_____ = typing.TypedDict('Checksum_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Exec_____ = typing.TypedDict('Exec_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sync_____ = typing.TypedDict('Sync_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compression_____ = typing.TypedDict('Compression_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compressratio____ = typing.TypedDict('Compressratio____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Origin____ = typing.TypedDict('Origin____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Quota____ = typing.TypedDict('Quota____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refquota____ = typing.TypedDict('Refquota____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Reservation____ = typing.TypedDict('Reservation____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refreservation____ = typing.TypedDict('Refreservation____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Copies____ = typing.TypedDict('Copies____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdir_____ = typing.TypedDict('Snapdir_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Readonly_____ = typing.TypedDict('Readonly_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Recordsize____ = typing.TypedDict('Recordsize____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sparse____ = typing.TypedDict('Sparse____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volsize____ = typing.TypedDict('Volsize____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volblocksize_____ = typing.TypedDict('Volblocksize_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    KeyFormat____ = typing.TypedDict('KeyFormat____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithm____ = typing.TypedDict('EncryptionAlgorithm____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Used____ = typing.TypedDict('Used____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbychildren____ = typing.TypedDict('Usedbychildren____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbydataset____ = typing.TypedDict('Usedbydataset____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbyrefreservation____ = typing.TypedDict('Usedbyrefreservation____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbysnapshots____ = typing.TypedDict('Usedbysnapshots____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Available____ = typing.TypedDict('Available____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SpecialSmallBlockSize____ = typing.TypedDict('SpecialSmallBlockSize____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Pbkdf2iters____ = typing.TypedDict('Pbkdf2iters____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Creation____ = typing.TypedDict('Creation____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdev_____ = typing.TypedDict('Snapdev_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
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
            'comments':'Comments____',
            'quota_warning':'QuotaWarning____',
            'quota_critical':'QuotaCritical____',
            'refquota_warning':'RefquotaWarning____',
            'refquota_critical':'RefquotaCritical____',
            'managedby':'Managedby____',
            'deduplication':'Deduplication_____',
            'aclmode':'Aclmode_____',
            'acltype':'Acltype_____',
            'xattr':'Xattr_____',
            'atime':'Atime_____',
            'casesensitivity':'Casesensitivity_____',
            'checksum':'Checksum_____',
            'exec':'Exec_____',
            'sync':'Sync_____',
            'compression':'Compression_____',
            'compressratio':'Compressratio____',
            'origin':'Origin____',
            'quota':'Quota____',
            'refquota':'Refquota____',
            'reservation':'Reservation____',
            'refreservation':'Refreservation____',
            'copies':'Copies____',
            'snapdir':'Snapdir_____',
            'readonly':'Readonly_____',
            'recordsize':'Recordsize____',
            'sparse':'Sparse____',
            'volsize':'Volsize____',
            'volblocksize':'Volblocksize_____',
            'key_format':'KeyFormat____',
            'encryption_algorithm':'EncryptionAlgorithm____',
            'used':'Used____',
            'usedbychildren':'Usedbychildren____',
            'usedbydataset':'Usedbydataset____',
            'usedbyrefreservation':'Usedbyrefreservation____',
            'usedbysnapshots':'Usedbysnapshots____',
            'available':'Available____',
            'special_small_block_size':'SpecialSmallBlockSize____',
            'pbkdf2iters':'Pbkdf2iters____',
            'creation':'Creation____',
            'snapdev':'Snapdev_____',
            'mountpoint':'typing.Optional[str]',
    })
