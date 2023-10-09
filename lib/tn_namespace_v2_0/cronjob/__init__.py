
from pytruenas import Namespace
import typing
class Cronjob(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cronjob')

    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    CronJobCreate = typing.TypedDict('CronJobCreate', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule',
            'command':'str',
            'description':'str',
            'user':'str',
    })
    Schedule_ = typing.TypedDict('Schedule_', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    CronjobCreateReturns = typing.TypedDict('CronjobCreateReturns', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule_',
            'command':'str',
            'description':'str',
            'user':'str',
            'id':'int',
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
    CronJobEntry = typing.TypedDict('CronJobEntry', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule__',
            'command':'str',
            'description':'str',
            'user':'str',
            'id':'int',
    })
    Schedule___ = typing.TypedDict('Schedule___', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    CronJobEntry_ = typing.TypedDict('CronJobEntry_', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule___',
            'command':'str',
            'description':'str',
            'user':'str',
            'id':'int',
    })
    Schedule____ = typing.TypedDict('Schedule____', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    CronJobEntry__ = typing.TypedDict('CronJobEntry__', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule____',
            'command':'str',
            'description':'str',
            'user':'str',
            'id':'int',
    })
    Schedule_____ = typing.TypedDict('Schedule_____', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    CronjobUpdate = typing.TypedDict('CronjobUpdate', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule_____',
            'command':'str',
            'description':'str',
            'user':'str',
    })
    Schedule______ = typing.TypedDict('Schedule______', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    CronjobUpdateReturns = typing.TypedDict('CronjobUpdateReturns', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule______',
            'command':'str',
            'description':'str',
            'user':'str',
            'id':'int',
    })
