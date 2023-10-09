
from pytruenas import Namespace
import typing
class Replication(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'replication')

    CountEligibleManualSnapshots = typing.TypedDict('CountEligibleManualSnapshots', {
            'datasets':'list[str]',
            'naming_schema':'list[str]',
            'name_regex':'typing.Optional[str]',
            'transport':'str',
            'ssh_credentials':'typing.Optional[int]',
    })
    CountEligibleManualSnapshots_ = typing.TypedDict('CountEligibleManualSnapshots_', {
            'total':'int',
            'eligible':'int',
    })
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
            'begin':'str',
            'end':'str',
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
    Schedule_ = typing.TypedDict('Schedule_', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    Lifetime = typing.TypedDict('Lifetime', {
            'schedule':'Schedule_',
            'lifetime_value':'int',
            'lifetime_unit':'str',
    })
    ReplicationCreate = typing.TypedDict('ReplicationCreate', {
            'name':'str',
            'direction':'str',
            'transport':'str',
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
            'readonly':'str',
            'hold_pending_snapshots':'bool',
            'retention_policy':'str',
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
    ReplicationRestore = typing.TypedDict('ReplicationRestore', {
            'name':'str',
            'target_dataset':'str',
    })
    RestrictSchedule_ = typing.TypedDict('RestrictSchedule_', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
            'begin':'str',
            'end':'str',
    })
    Schedule__ = typing.TypedDict('Schedule__', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    Lifetime_ = typing.TypedDict('Lifetime_', {
            'schedule':'Schedule__',
            'lifetime_value':'int',
            'lifetime_unit':'str',
    })
    ReplicationRunOnetime = typing.TypedDict('ReplicationRunOnetime', {
            'direction':'str',
            'transport':'str',
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
            'restrict_schedule':'RestrictSchedule_',
            'allow_from_scratch':'bool',
            'readonly':'str',
            'hold_pending_snapshots':'bool',
            'retention_policy':'str',
            'lifetime_value':'typing.Optional[int]',
            'lifetime_unit':'typing.Optional[str]',
            'lifetimes':'list[Lifetime_]',
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
    Schedule___ = typing.TypedDict('Schedule___', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
            'begin':'str',
            'end':'str',
    })
    RestrictSchedule__ = typing.TypedDict('RestrictSchedule__', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
            'begin':'str',
            'end':'str',
    })
    Schedule____ = typing.TypedDict('Schedule____', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    Lifetime__ = typing.TypedDict('Lifetime__', {
            'schedule':'Schedule____',
            'lifetime_value':'int',
            'lifetime_unit':'str',
    })
    ReplicationUpdate = typing.TypedDict('ReplicationUpdate', {
            'name':'str',
            'direction':'str',
            'transport':'str',
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
            'schedule':'Schedule___',
            'restrict_schedule':'RestrictSchedule__',
            'only_matching_schedule':'bool',
            'allow_from_scratch':'bool',
            'readonly':'str',
            'hold_pending_snapshots':'bool',
            'retention_policy':'str',
            'lifetime_value':'typing.Optional[int]',
            'lifetime_unit':'typing.Optional[str]',
            'lifetimes':'list[Lifetime__]',
            'compression':'typing.Optional[str]',
            'speed_limit':'typing.Optional[int]',
            'large_block':'bool',
            'embed':'bool',
            'compressed':'bool',
            'retries':'int',
            'logging_level':'typing.Optional[str]',
            'enabled':'bool',
    })
