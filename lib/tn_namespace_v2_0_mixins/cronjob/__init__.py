
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Cronjob(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cronjob')

    CronJobCreate = typing.TypedDict('CronJobCreate', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule',
            'command':'str',
            'description':'str',
            'user':'str',
    })
    Schedule = typing.TypedDict('Schedule', {
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
            'schedule':'Schedule',
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
    CronJobEntry = typing.TypedDict('CronJobEntry', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule',
            'command':'str',
            'description':'str',
            'user':'str',
            'id':'int',
    })
    CronjobUpdate = typing.TypedDict('CronjobUpdate', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule',
            'command':'str',
            'description':'str',
            'user':'str',
    })
    CronjobUpdateReturns = typing.TypedDict('CronjobUpdateReturns', {
            'enabled':'bool',
            'stderr':'bool',
            'stdout':'bool',
            'schedule':'Schedule',
            'command':'str',
            'description':'str',
            'user':'str',
            'id':'int',
    })
