
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Core(
    Namespace
    ):
    _namespace:typing.Literal['core']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def bulk(self, 
        _method:'str',
        _params:'list',
        _description:'typing.Optional[str]',
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
    @typing.overload
    def debug(self, 
        _options:'Options',
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
    @typing.overload
    def download(self, 
        _method:'str',
        _args:'list',
        _filename:'str',
        _buffered:'bool',
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
    @typing.overload
    def get_jobs(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[int, Job, list[Job]]': 
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
        typing.Union[int, Job, list[Job]]:
            
        """
        ...
    @typing.overload
    def job_abort(self, 
        _id:'int',
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
    @typing.overload
    def job_update(self, 
        _id:'int',
        _job_update:'JobUpdate',
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
    @typing.overload
    def job_wait(self, 
        _id:'int',
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
    @typing.overload
    def ping_remote(self, 
        _options:'Options_',
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
    @typing.overload
    def resize_shell(self, 
        _id:'str',
        _cols:'int',
        _rows:'int',
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
    @typing.overload
    def sessions(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[int, Session, list[Session]]': 
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
        typing.Union[int, Session, list[Session]]:
            
        """
        ...
    @typing.overload
    def set_debug_mode(self, 
        _debug_mode:'bool',
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
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
    })
    Options_ = typing.TypedDict('Options_', {
            'type':'Type',
            'hostname':'str',
            'timeout':'int',
    })
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
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
    Session = typing.TypedDict('Session', {
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
    class Type(str,Enum):
        ICMP = 'ICMP'
        ICMPV4 = 'ICMPV4'
        ICMPV6 = 'ICMPV6'
        ...
