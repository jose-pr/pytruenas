
from pytruenas import Namespace
import typing
class PoolScrub(Namespace):
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
    Schedule_ = typing.TypedDict('Schedule_', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    PoolScrubCreateReturns = typing.TypedDict('PoolScrubCreateReturns', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule_',
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
    Schedule__ = typing.TypedDict('Schedule__', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    PoolScrubEntry_ = typing.TypedDict('PoolScrubEntry_', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule__',
            'enabled':'bool',
            'id':'int',
            'pool_name':'str',
    })
    Schedule___ = typing.TypedDict('Schedule___', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    PoolScrubEntry__ = typing.TypedDict('PoolScrubEntry__', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule___',
            'enabled':'bool',
            'id':'int',
            'pool_name':'str',
    })
    Schedule____ = typing.TypedDict('Schedule____', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    PoolScrubEntry___ = typing.TypedDict('PoolScrubEntry___', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule____',
            'enabled':'bool',
            'id':'int',
            'pool_name':'str',
    })
    Schedule_____ = typing.TypedDict('Schedule_____', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    PoolScrubUpdate = typing.TypedDict('PoolScrubUpdate', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule_____',
            'enabled':'bool',
            'pool_name':'str',
    })
    Schedule______ = typing.TypedDict('Schedule______', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    PoolScrubUpdateReturns = typing.TypedDict('PoolScrubUpdateReturns', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule______',
            'enabled':'bool',
            'id':'int',
            'pool_name':'str',
    })
