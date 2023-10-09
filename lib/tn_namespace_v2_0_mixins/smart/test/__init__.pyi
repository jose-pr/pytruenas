
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class SmartTest(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['smart.test']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        smart_task_create:'SmartTaskCreate'={},
    /) -> 'SmartTestCreateReturns': 
        """
        Create a SMART Test Task.
        
        `disks` is a list of valid disks which should be monitored in this task.
        
        `type` is specified to represent the type of SMART test to be executed.
        
        `all_disks` when enabled sets the task to cover all disks in which case `disks` is not required.

        Parameters
        ----------
        smart_task_create:
            smart_task_create
        Returns
        -------
        SmartTestCreateReturns:
            smart_test_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete SMART Test Task of `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def disk_choices(self, 
        full_disk:'bool'=False,
    /) -> None: 
        """
        Returns disk choices for S.M.A.R.T. test.
        
        `full_disk` will return full disk objects instead of just names.

        Parameters
        ----------
        full_disk:
            full_disk
        Returns
        -------
        """
        ...
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance'={},
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
    def manual_test(self, 
        disks:'list[DiskRun]'=[],
    /) -> 'list[SmartManualTestDiskResponse]': 
        """
        Run manual SMART tests for `disks`.
        
        `type` indicates what type of SMART test will be ran and must be specified.

        Parameters
        ----------
        disks:
            Run manual SMART tests for `disks`.
        Returns
        -------
        list[SmartManualTestDiskResponse]:
            smart_manual_test
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[SmartTaskEntry], SmartTaskEntry_, int, SmartTaskEntry__]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[SmartTaskEntry], SmartTaskEntry_, int, SmartTaskEntry__]:
            
        """
        ...
    @typing.overload
    def query_for_disk(self, 
        disk:'str',
    /) -> None: 
        """
        Query S.M.A.R.T. tests for the specified disk.

        Parameters
        ----------
        disk:
            disk
        Returns
        -------
        """
        ...
    @typing.overload
    def results(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions_'={},
    /) -> 'typing.Union[int, DiskSmartTestResult, list[DiskSmartTestResult_]]': 
        """
        Get disk(s) S.M.A.R.T. test(s) results.
        
        `options.extra.tests_filter` is an optional filter for tests results.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[int, DiskSmartTestResult, list[DiskSmartTestResult_]]:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        smart_test_update:'SmartTestUpdate'={},
    /) -> 'SmartTestUpdateReturns': 
        """
        Update SMART Test Task of `id`.

        Parameters
        ----------
        id:
            Update SMART Test Task of `id`.
            Create a SMART Test Task.
        smart_test_update:
            smart_test_update
        Returns
        -------
        SmartTestUpdateReturns:
            smart_test_update_returns
        """
        ...
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
    SmartTaskCreate = typing.TypedDict('SmartTaskCreate', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'Type',
    })
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
    class Mode(str,Enum):
        FOREGROUND = 'FOREGROUND'
        BACKGROUND = 'BACKGROUND'
        ...
    DiskRun = typing.TypedDict('DiskRun', {
            'identifier':'str',
            'mode':'Mode',
            'type':'Type',
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
            'type':'Type',
            'id':'int',
    })
    SmartTaskEntry_ = typing.TypedDict('SmartTaskEntry_', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'Type',
            'id':'int',
    })
    SmartTaskEntry__ = typing.TypedDict('SmartTaskEntry__', {
            'schedule':'Schedule',
            'desc':'str',
            'all_disks':'bool',
            'disks':'list[str]',
            'type':'Type',
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
