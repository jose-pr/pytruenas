
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Initshutdownscript(Namespace):
    _namespace:_ty.Literal['initshutdownscript']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        init_shutdown_script_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            initshutdownscript_create_returns
        """
        ...
    @_ty.overload
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
    def update(self, 
        id:'int',
        initshutdownscript_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            initshutdownscript_update_returns
        """
        ...
