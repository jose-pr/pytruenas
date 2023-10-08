
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class PoolDataset(Namespace):
    _namespace:_ty.Literal['pool.dataset']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def attachments(self, 
        id:'str',
    /) -> 'list': 
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
        list:
            attachments
        """
        ...
    @_ty.overload
    def change_key(self, 
        id:'str',
        change_key_options:'dict[str]'={},
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
    @_ty.overload
    def checksum_choices(self, 
    /) -> 'dict[str]': 
        """
        Retrieve checksums supported for ZFS dataset.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            checksum_choices
        """
        ...
    @_ty.overload
    def compression_choices(self, 
    /) -> 'dict[str]': 
        """
        Retrieve compression algorithm supported by ZFS.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            compression_choices
        """
        ...
    @_ty.overload
    def create(self, 
        pool_dataset_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            pool_dataset_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'str',
        dataset_delete:'dict[str]'={},
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
    @_ty.overload
    def destroy_snapshots(self, 
        name:'str',
        snapshots:'dict[str]'={},
    /) -> 'list': 
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
        list:
            deleted_snapshots
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def encryption_algorithm_choices(self, 
    /) -> 'dict[str]': 
        """
        Retrieve encryption algorithms supported for ZFS dataset encryption.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            encryption_algorithm_choices
        """
        ...
    @_ty.overload
    def encryption_summary(self, 
        id:'str',
        encryption_root_summary_options:'dict[str]'={},
    /) -> 'list': 
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
        list:
            encryption_summary
        """
        ...
    @_ty.overload
    def export_key(self, 
        id:'str',
        download:'bool'=False,
    /) -> 'str|None': 
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
        str:
            key
        None:
            key
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    def get_quota(self, 
        ds:'str',
        quota_type:'str',
        query_filters:'list'=[],
        query_options:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
    def lock(self, 
        id:'str',
        lock_options:'dict[str]'={},
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
    @_ty.overload
    def mountpoint(self, 
        dataset:'str',
        raise:'bool'=True,
    /) -> 'str|None': 
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
        str:
            mountpoint
        None:
            mountpoint
        """
        ...
    @_ty.overload
    def permission(self, 
        id:'str',
        pool_dataset_permission:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            pool_dataset_permission
        """
        ...
    @_ty.overload
    def processes(self, 
        id:'str',
    /) -> 'list': 
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
        list:
            processes
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
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
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def recordsize_choices(self, 
        pool_name:'str|None'=None,
    /) -> 'list': 
        """
        Retrieve recordsize choices for datasets.

        Parameters
        ----------
        pool_name:
            pool_name
        Returns
        -------
        list:
            recordsize_choices
        """
        ...
    @_ty.overload
    def set_quota(self, 
        ds:'str',
        quotas:'list'=[{"quota_type": "USER", "id": "0", "quota_value": 0}],
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
    @_ty.overload
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
    @_ty.overload
    def unlock(self, 
        id:'str',
        unlock_options:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            unlock
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def update(self, 
        id:'str',
        pool_dataset_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            pool_dataset_update_returns
        """
        ...
