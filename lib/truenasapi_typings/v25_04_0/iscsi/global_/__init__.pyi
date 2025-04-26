from pytruenas import Namespace as _NS
import typing as _ty 
class IscsiGlobal(_NS):
    
    def alua_enabled(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiGlobalAlua_enabled:
        """Returns whether iSCSI ALUA is enabled or not."""
        ...
    def client_count(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiGlobalClient_count:
        """Return currently connected clients count."""
        ...
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiGlobalConfig:
        """"""
        ...
    def iser_enabled(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiGlobalIser_enabled:
        """Returns whether iSER is enabled or not."""
        ...
    def sessions(self,
        query_filters,
        query_options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiGlobalSessions:
        """Get a list of currently running iSCSI sessions. This includes initiator and target names and the unique connection IDs."""
        ...
    def update(self,
        iscsi_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IscsiGlobalUpdate:
        """`alua` is a no-op for FreeNAS."""
        ...
class IscsiGlobalAlua_enabled(_ty.TypedDict):
    ...
class IscsiGlobalClient_count(_ty.TypedDict):
    ...
class IscsiGlobalConfig(_ty.TypedDict):
    ...
class IscsiGlobalIser_enabled(_ty.TypedDict):
    ...
class IscsiGlobalSessions(_ty.TypedDict):
    ...
class IscsiGlobalUpdate(_ty.TypedDict):
    ... 