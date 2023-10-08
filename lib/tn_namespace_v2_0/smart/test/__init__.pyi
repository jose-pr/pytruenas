
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class SmartTest(Namespace):
    _namespace:_ty.Literal['smart.test']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        smart_task_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            smart_test_create_returns
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
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
    @_ty.overload
    def manual_test(self, 
        disks:'list'=[],
    /) -> 'list': 
        """
        Run manual SMART tests for `disks`.
        
        `type` indicates what type of SMART test will be ran and must be specified.

        Parameters
        ----------
        disks:
            Run manual SMART tests for `disks`.
        Returns
        -------
        list:
            smart_manual_test
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def results(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
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
        int:
            
        dict[str]:
            
        list:
            
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        smart_test_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            smart_test_update_returns
        """
        ...
