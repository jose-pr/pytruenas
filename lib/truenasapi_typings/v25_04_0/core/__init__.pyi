from pytruenas import Namespace as _NS
import typing as _ty 
class Core(_NS):
    
    def ping(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CorePing:
        """Utility method which just returns "pong". Can be used to keep connection/authtoken alive instead of using "ping" protocol message."""
        ...
    def set_options(self,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CoreSet_options:
        """"""
        ...
    def subscribe(self,
        event,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CoreSubscribe:
        """"""
        ...
    def unsubscribe(self,
        id_,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CoreUnsubscribe:
        """"""
        ...
class CorePing(_ty.TypedDict):
    ...
class CoreSet_options(_ty.TypedDict):
    ...
class CoreSubscribe(_ty.TypedDict):
    ...
class CoreUnsubscribe(_ty.TypedDict):
    ... 