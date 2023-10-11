
from pytruenas.base import Namespace

import typing
from enum import Enum

class PoolSnapshottask(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.snapshottask')

    class LifetimeUnit(str,Enum):
        HOUR = 'HOUR'
        DAY = 'DAY'
        WEEK = 'WEEK'
        MONTH = 'MONTH'
        YEAR = 'YEAR'
        ...
    Options = typing.TypedDict('Options', {
            'fixate_removal_date':'bool',
    })
    PeriodicSnapshotCreate = typing.TypedDict('PeriodicSnapshotCreate', {
            'dataset':'str',
            'recursive':'bool',
            'exclude':'list[str]',
            'lifetime_value':'int',
            'lifetime_unit':'LifetimeUnit',
            'naming_schema':'str',
            'schedule':'Schedule',
            'allow_empty':'bool',
            'enabled':'bool',
    })
    PeriodicSnapshotForeseenCount = typing.TypedDict('PeriodicSnapshotForeseenCount', {
            'lifetime_value':'int',
            'lifetime_unit':'LifetimeUnit',
            'schedule':'Schedule',
    })
    PeriodicSnapshotUpdate = typing.TypedDict('PeriodicSnapshotUpdate', {
            'dataset':'str',
            'recursive':'bool',
            'exclude':'list[str]',
            'lifetime_value':'int',
            'lifetime_unit':'LifetimeUnit',
            'naming_schema':'str',
            'schedule':'Schedule',
            'allow_empty':'bool',
            'enabled':'bool',
            'fixate_removal_date':'bool',
    })
    PeriodicSnapshotUpdateWillChangeRetention = typing.TypedDict('PeriodicSnapshotUpdateWillChangeRetention', {
            'dataset':'str',
            'recursive':'bool',
            'exclude':'list[str]',
            'lifetime_value':'int',
            'lifetime_unit':'LifetimeUnit',
            'naming_schema':'str',
            'schedule':'Schedule',
            'allow_empty':'bool',
            'enabled':'bool',
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
            'begin':'str',
            'end':'str',
    })
