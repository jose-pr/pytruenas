
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class SmartTest(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'smart.test')

    Schedule = typing.TypedDict('Schedule', {
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    SmartTaskCreate = typing.TypedDict('SmartTaskCreate', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'str',
    })
    SmartTestCreateReturns = typing.TypedDict('SmartTestCreateReturns', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'str',
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
            'mode':'str',
            'type':'str',
    })
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
            'type':'str',
            'id':'int',
    })
    SmartTaskEntry_ = typing.TypedDict('SmartTaskEntry_', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'str',
            'id':'int',
    })
    SmartTaskEntry__ = typing.TypedDict('SmartTaskEntry__', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'str',
            'id':'int',
    })
    QueryOptions_ = typing.TypedDict('QueryOptions_', {
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
    DiskSmartTestResult = typing.TypedDict('DiskSmartTestResult', {
            'disk':'str',
            'tests':'list[TestResult]',
            'current_test':'CurrentTest',
    })
    TestResult_ = typing.TypedDict('TestResult_', {
            'num':'int',
            'description':'str',
            'status':'str',
            'status_verbose':'str',
            'remaining':'float',
            'lifetime':'int',
            'lba_of_first_error':'typing.Optional[str]',
    })
    DiskSmartTestResult_ = typing.TypedDict('DiskSmartTestResult_', {
            'disk':'str',
            'tests':'list[TestResult_]',
            'current_test':'CurrentTest',
    })
    SmartTestUpdate = typing.TypedDict('SmartTestUpdate', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'str',
    })
    SmartTestUpdateReturns = typing.TypedDict('SmartTestUpdateReturns', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'str',
            'id':'int',
    })
