
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Replication(
    Namespace
    ):
    _namespace:typing.Literal['replication']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def count_eligible_manual_snapshots(self, 
        count_eligible_manual_snapshots:'CountEligibleManualSnapshots',
    /) -> 'CountEligibleManualSnapshots_': 
        """
        Count how many existing snapshots of `dataset` match `naming_schema`.

        Parameters
        ----------
        count_eligible_manual_snapshots:
            count_eligible_manual_snapshots
        Returns
        -------
        CountEligibleManualSnapshots_:
            count_eligible_manual_snapshots
        """
        ...
    @typing.overload
    def create(self, 
        replication_create:'ReplicationCreate',
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
    @typing.overload
    def create_dataset(self, 
        dataset:'str',
        transport:'Transport',
        ssh_credentials:'typing.Optional[int]',
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
    @typing.overload
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
    def list_datasets(self, 
        transport:'Transport',
        ssh_credentials:'typing.Optional[int]',
    /) -> 'list[str]': 
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
        list[str]:
            datasets
        """
        ...
    @typing.overload
    def list_naming_schemas(self, 
    /) -> 'list[str]': 
        """
        List all naming schemas used in periodic snapshot and replication tasks.

        Parameters
        ----------
        Returns
        -------
        list[str]:
            naming_schemas
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
    def restore(self, 
        id:'int',
        replication_restore:'ReplicationRestore',
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
    @typing.overload
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
    @typing.overload
    def run_onetime(self, 
        replication_run_onetime:'ReplicationRunOnetime',
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
    @typing.overload
    def target_unmatched_snapshots(self, 
        direction:'Direction',
        source_datasets:'list[str]',
        target_dataset:'str',
        transport:'Transport_',
        ssh_credentials:'typing.Optional[int]',
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
    @typing.overload
    def update(self, 
        id:'int',
        replication_update:'ReplicationUpdate',
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
    CountEligibleManualSnapshots = typing.TypedDict('CountEligibleManualSnapshots', {
            'datasets':'list[str]',
            'naming_schema':'list[str]',
            'name_regex':'typing.Optional[str]',
            'transport':'Transport',
            'ssh_credentials':'typing.Optional[int]',
    })
    CountEligibleManualSnapshots_ = typing.TypedDict('CountEligibleManualSnapshots_', {
            'total':'int',
            'eligible':'int',
    })
    class Direction(str,Enum):
        PUSH = 'PUSH'
        PULL = 'PULL'
        ...
    Lifetime = typing.TypedDict('Lifetime', {
            'schedule':'Schedule_',
            'lifetime_value':'int',
            'lifetime_unit':'LifetimeUnit',
    })
    class LifetimeUnit(str,Enum):
        HOUR = 'HOUR'
        DAY = 'DAY'
        WEEK = 'WEEK'
        MONTH = 'MONTH'
        YEAR = 'YEAR'
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
    class Readonly(str,Enum):
        SET = 'SET'
        REQUIRE = 'REQUIRE'
        IGNORE = 'IGNORE'
        ...
    ReplicationCreate = typing.TypedDict('ReplicationCreate', {
            'name':'str',
            'direction':'Direction',
            'transport':'Transport',
            'ssh_credentials':'typing.Optional[int]',
            'netcat_active_side':'typing.Optional[str]',
            'netcat_active_side_listen_address':'typing.Optional[str]',
            'netcat_active_side_port_min':'typing.Optional[int]',
            'netcat_active_side_port_max':'typing.Optional[int]',
            'netcat_passive_side_connect_address':'typing.Optional[str]',
            'sudo':'bool',
            'source_datasets':'list[str]',
            'target_dataset':'str',
            'recursive':'bool',
            'exclude':'list[str]',
            'properties':'bool',
            'properties_exclude':'list[str]',
            'properties_override':'dict[str]',
            'replicate':'bool',
            'encryption':'bool',
            'encryption_inherit':'typing.Optional[bool]',
            'encryption_key':'typing.Optional[str]',
            'encryption_key_format':'typing.Optional[str]',
            'encryption_key_location':'typing.Optional[str]',
            'periodic_snapshot_tasks':'list[int]',
            'naming_schema':'list[str]',
            'also_include_naming_schema':'list[str]',
            'name_regex':'typing.Optional[str]',
            'auto':'bool',
            'schedule':'Schedule',
            'restrict_schedule':'RestrictSchedule',
            'only_matching_schedule':'bool',
            'allow_from_scratch':'bool',
            'readonly':'Readonly',
            'hold_pending_snapshots':'bool',
            'retention_policy':'RetentionPolicy',
            'lifetime_value':'typing.Optional[int]',
            'lifetime_unit':'typing.Optional[str]',
            'lifetimes':'list[Lifetime]',
            'compression':'typing.Optional[str]',
            'speed_limit':'typing.Optional[int]',
            'large_block':'bool',
            'embed':'bool',
            'compressed':'bool',
            'retries':'int',
            'logging_level':'typing.Optional[str]',
            'enabled':'bool',
    })
    ReplicationRestore = typing.TypedDict('ReplicationRestore', {
            'name':'str',
            'target_dataset':'str',
    })
    ReplicationRunOnetime = typing.TypedDict('ReplicationRunOnetime', {
            'direction':'Direction',
            'transport':'Transport',
            'ssh_credentials':'typing.Optional[int]',
            'netcat_active_side':'typing.Optional[str]',
            'netcat_active_side_listen_address':'typing.Optional[str]',
            'netcat_active_side_port_min':'typing.Optional[int]',
            'netcat_active_side_port_max':'typing.Optional[int]',
            'netcat_passive_side_connect_address':'typing.Optional[str]',
            'sudo':'bool',
            'source_datasets':'list[str]',
            'target_dataset':'str',
            'recursive':'bool',
            'exclude':'list[str]',
            'properties':'bool',
            'properties_exclude':'list[str]',
            'properties_override':'dict[str]',
            'replicate':'bool',
            'encryption':'bool',
            'encryption_inherit':'typing.Optional[bool]',
            'encryption_key':'typing.Optional[str]',
            'encryption_key_format':'typing.Optional[str]',
            'encryption_key_location':'typing.Optional[str]',
            'periodic_snapshot_tasks':'list[int]',
            'naming_schema':'list[str]',
            'also_include_naming_schema':'list[str]',
            'name_regex':'typing.Optional[str]',
            'restrict_schedule':'RestrictSchedule',
            'allow_from_scratch':'bool',
            'readonly':'Readonly',
            'hold_pending_snapshots':'bool',
            'retention_policy':'RetentionPolicy',
            'lifetime_value':'typing.Optional[int]',
            'lifetime_unit':'typing.Optional[str]',
            'lifetimes':'list[Lifetime]',
            'compression':'typing.Optional[str]',
            'speed_limit':'typing.Optional[int]',
            'large_block':'bool',
            'embed':'bool',
            'compressed':'bool',
            'retries':'int',
            'logging_level':'typing.Optional[str]',
            'exclude_mountpoint_property':'bool',
            'only_from_scratch':'bool',
    })
    ReplicationUpdate = typing.TypedDict('ReplicationUpdate', {
            'name':'str',
            'direction':'Direction',
            'transport':'Transport',
            'ssh_credentials':'typing.Optional[int]',
            'netcat_active_side':'typing.Optional[str]',
            'netcat_active_side_listen_address':'typing.Optional[str]',
            'netcat_active_side_port_min':'typing.Optional[int]',
            'netcat_active_side_port_max':'typing.Optional[int]',
            'netcat_passive_side_connect_address':'typing.Optional[str]',
            'sudo':'bool',
            'source_datasets':'list[str]',
            'target_dataset':'str',
            'recursive':'bool',
            'exclude':'list[str]',
            'properties':'bool',
            'properties_exclude':'list[str]',
            'properties_override':'dict[str]',
            'replicate':'bool',
            'encryption':'bool',
            'encryption_inherit':'typing.Optional[bool]',
            'encryption_key':'typing.Optional[str]',
            'encryption_key_format':'typing.Optional[str]',
            'encryption_key_location':'typing.Optional[str]',
            'periodic_snapshot_tasks':'list[int]',
            'naming_schema':'list[str]',
            'also_include_naming_schema':'list[str]',
            'name_regex':'typing.Optional[str]',
            'auto':'bool',
            'schedule':'Schedule',
            'restrict_schedule':'RestrictSchedule',
            'only_matching_schedule':'bool',
            'allow_from_scratch':'bool',
            'readonly':'Readonly',
            'hold_pending_snapshots':'bool',
            'retention_policy':'RetentionPolicy',
            'lifetime_value':'typing.Optional[int]',
            'lifetime_unit':'typing.Optional[str]',
            'lifetimes':'list[Lifetime]',
            'compression':'typing.Optional[str]',
            'speed_limit':'typing.Optional[int]',
            'large_block':'bool',
            'embed':'bool',
            'compressed':'bool',
            'retries':'int',
            'logging_level':'typing.Optional[str]',
            'enabled':'bool',
    })
    RestrictSchedule = typing.TypedDict('RestrictSchedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
            'begin':'str',
            'end':'str',
    })
    class RetentionPolicy(str,Enum):
        SOURCE = 'SOURCE'
        CUSTOM = 'CUSTOM'
        NONE = 'NONE'
        ...
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
            'begin':'str',
            'end':'str',
    })
    Schedule_ = typing.TypedDict('Schedule_', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    class Transport(str,Enum):
        SSH = 'SSH'
        SSHPlusNETCAT = 'SSH+NETCAT'
        LOCAL = 'LOCAL'
        ...
    class Transport_(str,Enum):
        SSH = 'SSH'
        SSHPlusNETCAT = 'SSH+NETCAT'
        LOCAL = 'LOCAL'
        LEGACY = 'LEGACY'
        ...
