
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class PoolScrub(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.scrub')

    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    PoolScrubEntry = typing.TypedDict('PoolScrubEntry', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule',
            'enabled':'bool',
    })
    PoolScrubCreateReturns = typing.TypedDict('PoolScrubCreateReturns', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule',
            'enabled':'bool',
            'id':'int',
            'pool_name':'str',
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
    PoolScrubEntry_ = typing.TypedDict('PoolScrubEntry_', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule',
            'enabled':'bool',
            'id':'int',
            'pool_name':'str',
    })
    class Action(str,Enum):
        START = 'START'
        STOP = 'STOP'
        PAUSE = 'PAUSE'
        ...
    PoolScrubUpdate = typing.TypedDict('PoolScrubUpdate', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule',
            'enabled':'bool',
            'pool_name':'str',
    })
    PoolScrubUpdateReturns = typing.TypedDict('PoolScrubUpdateReturns', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule',
            'enabled':'bool',
            'id':'int',
            'pool_name':'str',
    })
