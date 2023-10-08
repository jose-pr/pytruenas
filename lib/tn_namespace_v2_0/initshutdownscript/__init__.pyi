
from pytruenas import Namespace, TrueNASClient
import typing
class Initshutdownscript(Namespace):
    _namespace:typing.Literal['initshutdownscript']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        init_shutdown_script_create:'InitShutdownScriptCreate'={},
    /) -> 'InitshutdownscriptCreateReturns': 
        """
        Create an initshutdown script task.
        
        `type` indicates if a command or script should be executed at `when`.
        
        There are three choices for `when`:
        
        1) PREINIT - This is early in the boot process before all the services / rc scripts have started
        2) POSTINIT - This is late in the boot process when most of the services / rc scripts have started
        3) SHUTDOWN - This is on shutdown
        
        `timeout` is an integer value which indicates time in seconds which the system should wait for the execution
        of script/command. It should be noted that a hard limit for a timeout is configured by the base OS, so when
        a script/command is set to execute on SHUTDOWN, the hard limit configured by the base OS is changed adding
        the timeout specified by script/command so it can be ensured that it executes as desired and is not interrupted
        by the base OS's limit.

        Parameters
        ----------
        init_shutdown_script_create:
            init_shutdown_script_create
        Returns
        -------
        InitshutdownscriptCreateReturns:
            initshutdownscript_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete init/shutdown task of `id`.

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
    /) -> 'list[InitShutdownScriptEntry]|InitShutdownScriptEntry|int|InitShutdownScriptEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[InitShutdownScriptEntry]:
            
        InitShutdownScriptEntry:
            
        int:
            
        InitShutdownScriptEntry:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        initshutdownscript_update:'InitshutdownscriptUpdate'={},
    /) -> 'InitshutdownscriptUpdateReturns': 
        """
        Update initshutdown script task of `id`.

        Parameters
        ----------
        id:
            Update initshutdown script task of `id`.
            Create an initshutdown script task.
        initshutdownscript_update:
            initshutdownscript_update
        Returns
        -------
        InitshutdownscriptUpdateReturns:
            initshutdownscript_update_returns
        """
        ...

class InitShutdownScriptCreate(typing.TypedDict):
        type:'str'
        command:'typing.Optional[str]'
        script_text:'typing.Optional[str]'
        script:'typing.Optional[str]'
        when:'str'
        enabled:'bool'
        timeout:'int'
        comment:'str'
        ...
class InitshutdownscriptCreateReturns(typing.TypedDict):
        type:'str'
        command:'typing.Optional[str]'
        script_text:'typing.Optional[str]'
        script:'typing.Optional[str]'
        when:'str'
        enabled:'bool'
        timeout:'int'
        comment:'str'
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
class InitShutdownScriptEntry(typing.TypedDict):
        type:'str'
        command:'typing.Optional[str]'
        script_text:'typing.Optional[str]'
        script:'typing.Optional[str]'
        when:'str'
        enabled:'bool'
        timeout:'int'
        comment:'str'
        id:'int'
        ...
class InitshutdownscriptUpdate(typing.TypedDict):
        type:'str'
        command:'typing.Optional[str]'
        script_text:'typing.Optional[str]'
        script:'typing.Optional[str]'
        when:'str'
        enabled:'bool'
        timeout:'int'
        comment:'str'
        ...
class InitshutdownscriptUpdateReturns(typing.TypedDict):
        type:'str'
        command:'typing.Optional[str]'
        script_text:'typing.Optional[str]'
        script:'typing.Optional[str]'
        when:'str'
        enabled:'bool'
        timeout:'int'
        comment:'str'
        id:'int'
        ...
