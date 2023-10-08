
from pytruenas import Namespace, TrueNASClient
import typing
class Cronjob(Namespace):
    _namespace:typing.Literal['cronjob']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        cron_job_create:'CronJobCreate'={},
    /) -> 'CronjobCreateReturns': 
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
        CronjobCreateReturns:
            cronjob_create_returns
        """
        ...
    @typing.overload
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
    @typing.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
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
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[CronJobEntry]|CronJobEntry|int|CronJobEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[CronJobEntry]:
            
        CronJobEntry:
            
        int:
            
        CronJobEntry:
            
        """
        ...
    @typing.overload
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
    @typing.overload
    def update(self, 
        id:'int',
        cronjob_update:'CronjobUpdate'={},
    /) -> 'CronjobUpdateReturns': 
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
        CronjobUpdateReturns:
            cronjob_update_returns
        """
        ...

class CronJobCreate(typing.TypedDict):
        enabled:'bool'
        stderr:'bool'
        stdout:'bool'
        schedule:'Schedule'
        command:'str'
        description:'str'
        user:'str'
        ...
class Schedule(typing.TypedDict):
        minute:'str'
        hour:'str'
        dom:'str'
        month:'str'
        dow:'str'
        ...
class CronjobCreateReturns(typing.TypedDict):
        enabled:'bool'
        stderr:'bool'
        stdout:'bool'
        schedule:'Schedule'
        command:'str'
        description:'str'
        user:'str'
        id:'int'
        ...
class QueryOptionsGetInstance(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class CronJobEntry(typing.TypedDict):
        enabled:'bool'
        stderr:'bool'
        stdout:'bool'
        schedule:'Schedule'
        command:'str'
        description:'str'
        user:'str'
        id:'int'
        ...
class CronjobUpdate(typing.TypedDict):
        enabled:'bool'
        stderr:'bool'
        stdout:'bool'
        schedule:'Schedule'
        command:'str'
        description:'str'
        user:'str'
        ...
class CronjobUpdateReturns(typing.TypedDict):
        enabled:'bool'
        stderr:'bool'
        stdout:'bool'
        schedule:'Schedule'
        command:'str'
        description:'str'
        user:'str'
        id:'int'
        ...