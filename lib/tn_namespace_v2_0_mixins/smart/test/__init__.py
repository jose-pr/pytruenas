
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class SmartTest(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'smart.test')

    SmartTaskCreate = typing.TypedDict('SmartTaskCreate', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'Type',
    })
    Schedule = typing.TypedDict('Schedule', {
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    class Type(str,Enum):
        LONG = 'LONG'
        SHORT = 'SHORT'
        CONVEYANCE = 'CONVEYANCE'
        OFFLINE = 'OFFLINE'
        ...
    SmartTestCreateReturns = typing.TypedDict('SmartTestCreateReturns', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'Type',
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
    DiskRun = typing.TypedDict('DiskRun', {
            'identifier':'str',
            'mode':'Mode',
            'type':'Type',
    })
    class Mode(str,Enum):
        FOREGROUND = 'FOREGROUND'
        BACKGROUND = 'BACKGROUND'
        ...
    SmartManualTestDiskResponse = typing.TypedDict('SmartManualTestDiskResponse', {
            'disk':'str',
            'identifier':'str',
            'error':'typing.Optional[str]',
            'expected_result_time':'str',
            'job':'int',
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
    SmartTaskEntry = typing.TypedDict('SmartTaskEntry', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'Type',
            'id':'int',
    })
    DiskSmartTestResult = typing.TypedDict('DiskSmartTestResult', {
            'disk':'str',
            'tests':'list[TestResult]',
            'current_test':'CurrentTest',
    })
    TestResult = typing.TypedDict('TestResult', {
            'num':'int',
            'description':'str',
            'status':'str',
            'status_verbose':'str',
            'remaining':'float',
            'lifetime':'int',
            'lba_of_first_error':'typing.Optional[str]',
    })
    CurrentTest = typing.TypedDict('CurrentTest', {
            'progress':'int',
    })
    SmartTestUpdate = typing.TypedDict('SmartTestUpdate', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'Type',
    })
    SmartTestUpdateReturns = typing.TypedDict('SmartTestUpdateReturns', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'Type',
            'id':'int',
    })
