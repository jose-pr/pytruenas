
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Replication(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'replication')

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
