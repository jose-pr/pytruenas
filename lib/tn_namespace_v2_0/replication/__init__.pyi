
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Replication(Namespace):
    _namespace:_ty.Literal['replication']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def count_eligible_manual_snapshots(self, 
        count_eligible_manual_snapshots:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Count how many existing snapshots of `dataset` match `naming_schema`.

        Parameters
        ----------
        count_eligible_manual_snapshots:
            count_eligible_manual_snapshots
        Returns
        -------
        dict[str]:
            count_eligible_manual_snapshots
        """
        ...
    @_ty.overload
    def create(self, 
        replication_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a Replication Task
        
        Create a Replication Task that will push or pull ZFS snapshots to or from remote host..
        
        * `name` specifies a name for replication task
        * `direction` specifies whether task will `PUSH` or `PULL` snapshots
        * `transport` is a method of snapshots transfer:
          * `SSH` transfers snapshots via SSH connection. This method is supported everywhere but does not achieve
            great performance
            `ssh_credentials` is a required field for this transport (Keychain Credential ID of type `SSH_CREDENTIALS`)
          * `SSH+NETCAT` uses unencrypted connection for data transfer. This can only be used in trusted networks
            and requires a port (specified by range from `netcat_active_side_port_min` to `netcat_active_side_port_max`)
            to be open on `netcat_active_side`
            `ssh_credentials` is also required for control connection
          * `LOCAL` replicates to or from localhost
          `sudo` flag controls whether `SSH` and `SSH+NETCAT` transports should use sudo (which is expected to be
          passwordless) to run `zfs` command on the remote machine.
        * `source_datasets` is a non-empty list of datasets to replicate snapshots from
        * `target_dataset` is a dataset to put snapshots into. It must exist on target side
        * `recursive` and `exclude` have the same meaning as for Periodic Snapshot Task
        * `properties` control whether we should send dataset properties along with snapshots
        * `periodic_snapshot_tasks` is a list of periodic snapshot task IDs that are sources of snapshots for this
          replication task. Only push replication tasks can be bound to periodic snapshot tasks.
        * `naming_schema` is a list of naming schemas for pull replication
        * `also_include_naming_schema` is a list of naming schemas for push replication
        * `name_regex` will replicate all snapshots which names match specified regular expression
        * `auto` allows replication to run automatically on schedule or after bound periodic snapshot task
        * `schedule` is a schedule to run replication task. Only `auto` replication tasks without bound periodic
          snapshot tasks can have a schedule
        * `restrict_schedule` restricts when replication task with bound periodic snapshot tasks runs. For example,
          you can have periodic snapshot tasks that run every 15 minutes, but only run replication task every hour.
        * Enabling `only_matching_schedule` will only replicate snapshots that match `schedule` or
          `restrict_schedule`
        * `allow_from_scratch` will destroy all snapshots on target side and replicate everything from scratch if none
          of the snapshots on target side matches source snapshots
        * `readonly` controls destination datasets readonly property:
          * `SET` will set all destination datasets to readonly=on after finishing the replication
          * `REQUIRE` will require all existing destination datasets to have readonly=on property
          * `IGNORE` will avoid this kind of behavior
        * `hold_pending_snapshots` will prevent source snapshots from being deleted by retention of replication fails
          for some reason
        * `retention_policy` specifies how to delete old snapshots on target side:
          * `SOURCE` deletes snapshots that are absent on source side
          * `CUSTOM` deletes snapshots that are older than `lifetime_value` and `lifetime_unit`
          * `NONE` does not delete any snapshots
        * `compression` compresses SSH stream. Available only for SSH transport
        * `speed_limit` limits speed of SSH stream. Available only for SSH transport
        * `large_block`, `embed` and `compressed` are various ZFS stream flag documented in `man zfs send`
        * `retries` specifies number of retries before considering replication failed

        Parameters
        ----------
        replication_create:
            replication_create
        Returns
        -------
        dict[str]:
            replication_create_returns
        """
        ...
    @_ty.overload
    def create_dataset(self, 
        dataset:'str',
        transport:'str',
        ssh_credentials:'int|None'=None,
    /) -> None: 
        """
        Creates dataset on remote side
        
        Accepts `dataset` name, `transport` and SSH credentials ID (for non-local transport)

        Parameters
        ----------
        dataset:
            Accepts `dataset` name, `transport` and SSH credentials ID (for non-local transport)
        transport:
            Accepts `dataset` name, `transport` and SSH credentials ID (for non-local transport)
        ssh_credentials:
            ssh_credentials
        Returns
        -------
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete a Replication Task with specific `id`

        Parameters
        ----------
        id:
            Delete a Replication Task with specific `id`
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
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
    def list_datasets(self, 
        transport:'str',
        ssh_credentials:'int|None'=None,
    /) -> 'list': 
        """
        List datasets on remote side
        
        Accepts `transport` and SSH credentials ID (for non-local transport)

        Parameters
        ----------
        transport:
            Accepts `transport` and SSH credentials ID (for non-local transport)
        ssh_credentials:
            ssh_credentials
        Returns
        -------
        list:
            datasets
        """
        ...
    @_ty.overload
    def list_naming_schemas(self, 
    /) -> 'list': 
        """
        List all naming schemas used in periodic snapshot and replication tasks.

        Parameters
        ----------
        Returns
        -------
        list:
            naming_schemas
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
    def restore(self, 
        id:'int',
        replication_restore:'dict[str]'={},
    /) -> None: 
        """
        Create the opposite of replication task `id` (PULL if it was PUSH and vice versa).

        Parameters
        ----------
        id:
            id
        replication_restore:
            replication_restore
        Returns
        -------
        """
        ...
    @_ty.overload
    def run(self, 
        id:'int',
    /) -> None: 
        """
        Run Replication Task of `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @_ty.overload
    def run_onetime(self, 
        replication_run_onetime:'dict[str]'={},
    /) -> None: 
        """
        Run replication task without creating it.
        
        If `only_from_scratch` is `true` then replication will fail if target dataset already exists.

        Parameters
        ----------
        replication_run_onetime:
            replication_run_onetime
        Returns
        -------
        """
        ...
    @_ty.overload
    def target_unmatched_snapshots(self, 
        direction:'str',
        source_datasets:'list',
        target_dataset:'str',
        transport:'str',
        ssh_credentials:'int|None'=None,
    /) -> 'dict[str]': 
        """
        Check if target has any snapshots that do not exist on source. Returns these snapshots grouped by dataset.

        Parameters
        ----------
        direction:
            direction
        source_datasets:
            source_datasets
        target_dataset:
            target_dataset
        transport:
            transport
        ssh_credentials:
            ssh_credentials
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "backup/work": [
                    "auto-2019-10-15_13-00",
                    "auto-2019-10-15_09-00"
                ],
                "backup/games": [
                    "auto-2019-10-15_13-00"
                ]
            }
            ```
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        replication_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update a Replication Task with specific `id`
        
        See the documentation for `create` method for information on payload contents

        Parameters
        ----------
        id:
            Update a Replication Task with specific `id`
        replication_update:
            replication_update
        Returns
        -------
        dict[str]:
            replication_update_returns
        """
        ...
