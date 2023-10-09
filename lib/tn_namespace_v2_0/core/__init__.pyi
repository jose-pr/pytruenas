
from pytruenas import Namespace, TrueNASClient
import typing
class Core(Namespace):
    _namespace:typing.Literal['core']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def bulk(self, 
        method:'str',
        params:'list'=[],
        description:'typing.Optional[str]'=None,
    /) -> None: 
        """
        Will sequentially call `method` with arguments from the `params` list. For example, running
        
            call("core.bulk", "zfs.snapshot.delete", [["tank@snap-1", true], ["tank@snap-2", false]])
        
        will call
        
            call("zfs.snapshot.delete", "tank@snap-1", true)
            call("zfs.snapshot.delete", "tank@snap-2", false)
        
        If the first call fails and the seconds succeeds (returning `true`), the result of the overall call will be:
        
            [
                {"result": null, "error": "Error deleting snapshot"},
                {"result": true, "error": null}
            ]
        
        Important note: the execution status of `core.bulk` will always be a `SUCCESS` (unless an unlikely internal
        error occurs). Caller must check for individual call results to ensure the absence of any call errors.
        
        `description` contains format string for job progress (e.g. "Deleting snapshot {0[dataset]}@{0[name]}")

        Parameters
        ----------
        method:
            Will sequentially call `method` with arguments from the `params` list. For example, running
        params:
            Will sequentially call `method` with arguments from the `params` list. For example, running
        description:
            description
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def debug(self, 
        options:'Options'={},
    /) -> None: 
        """
        Setup middlewared for remote debugging.
        
        engine currently used:
          - REMOTE_PDB: Remote vanilla PDB (over TCP sockets)
        
        options:
            - bind_address: local ip address to bind the remote debug session to
            - bind_port: local port to listen on
            - threaded: run debugger in a new thread instead of the main event loop

        Parameters
        ----------
        options:
            options
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def debug_mode_enabled(self, 
    /) -> 'bool': 
        """
        

        Parameters
        ----------
        Returns
        -------
        bool:
            debug_mode_enabled
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def download(self, 
        method:'str',
        args:'list'=[],
        filename:'str',
        buffered:'bool'=False,
    /) -> None: 
        """
        Core helper to call a job marked for download.
        
        Non-`buffered` downloads will allow job to write to pipe as soon as download URL is requested, job will stay
        blocked meanwhile. `buffered` downloads must wait for job to complete before requesting download URL, job's
        pipe output will be buffered to ramfs.
        
        Returns the job id and the URL for download.

        Parameters
        ----------
        method:
            method
        args:
            args
        filename:
            filename
        buffered:
            Non-`buffered` downloads will allow job to write to pipe as soon as download URL is requested, job will stay
            blocked meanwhile. `buffered` downloads must wait for job to complete before requesting download URL, job's
            pipe output will be buffered to ramfs.
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def get_events(self, 
    /) -> None: 
        """
        Returns metadata for every possible event emitted from websocket server.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def get_jobs(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[int, ForwardRef(Job), list[Job_]]': 
        """
        Get the long running jobs.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[int, ForwardRef(Job), list[Job_]]:
            
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def job_abort(self, 
        id:'int',
    /) -> None: 
        """
        

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def job_update(self, 
        id:'int',
        job_update:'JobUpdate'={},
    /) -> None: 
        """
        

        Parameters
        ----------
        id:
            id
        job_update:
            job-update
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def job_wait(self, 
        id:'int',
    /) -> None: 
        """
        

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def ping(self, 
    /) -> None: 
        """
        Utility method which just returns "pong".
        Can be used to keep connection/authtoken alive instead of using
        "ping" protocol message.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def ping_remote(self, 
        options:'Options_'={},
    /) -> None: 
        """
        Method that will send an ICMP echo request to "hostname"
        and will wait up to "timeout" for a reply.

        Parameters
        ----------
        options:
            options
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def resize_shell(self, 
        id:'str',
        cols:'int',
        rows:'int',
    /) -> None: 
        """
        Resize terminal session (/websocket/shell) to cols x rows

        Parameters
        ----------
        id:
            id
        cols:
            cols
        rows:
            rows
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def sessions(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions_'={},
    /) -> 'typing.Union[int, ForwardRef(Session), list[Session]]': 
        """
        Get currently open websocket sessions.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[int, ForwardRef(Session), list[Session]]:
            
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    @typing.overload
    def set_debug_mode(self, 
        debug_mode:'bool',
    /) -> None: 
        """
        Set `debug_mode` for middleware.

        Parameters
        ----------
        debug_mode:
            debug_mode
        Returns
        -------
        """
        ...
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'str',
            'hostname':'str',
            'timeout':'int',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })

