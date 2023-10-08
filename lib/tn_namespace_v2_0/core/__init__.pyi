
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Core(Namespace):
    _namespace:_ty.Literal['core']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def bulk(self, 
        method:'str',
        params:'list'=[],
        description:'str|None'=None,
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
    @_ty.overload
    def debug(self, 
        options:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def get_jobs(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
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
        int:
            
        dict[str]:
            
        list:
            
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def job_update(self, 
        id:'int',
        job_update:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def ping_remote(self, 
        options:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
    def sessions(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
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
        int:
            
        dict[str]:
            
        list:
            
        """
        ...
    @_ty.overload
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
