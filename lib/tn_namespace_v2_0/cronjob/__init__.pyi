
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Cronjob(Namespace):
    _namespace:_ty.Literal['cronjob']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        cron_job_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a new cron job.
        
        `stderr` and `stdout` are boolean values which if `true`, represent that we would like to suppress
        standard error / standard output respectively.

        Parameters
        ----------
        cron_job_create:
            cron_job_create
        Returns
        -------
        dict[str]:
            cronjob_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete cronjob of `id`.

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
    def run(self, 
        id:'int',
        skip_disabled:'bool'=False,
    /) -> None: 
        """
        Job to run cronjob task of `id`.

        Parameters
        ----------
        id:
            id
        skip_disabled:
            skip_disabled
        Returns
        -------
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        cronjob_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update cronjob of `id`.

        Parameters
        ----------
        id:
            Update cronjob of `id`.
            Create a new cron job.
        cronjob_update:
            cronjob_update
        Returns
        -------
        dict[str]:
            cronjob_update_returns
        """
        ...
