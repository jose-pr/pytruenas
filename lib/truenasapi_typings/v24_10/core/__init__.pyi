from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Core(_NS):
    
    def ping(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str:
        """Utility method which just returns "pong". Can be used to keep connection/authtoken alive instead of using "ping" protocol message."""
        ...
    def set_options(self,
        options:SetOptionsOptions,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """"""
        ...
    def subscribe(self,
        event:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str:
        """"""
        ...
    def unsubscribe(self,
        id_:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """"""
        ...
SetOptionsOptions = _ty.TypedDict('SetOptionsOptions', {
    'py_exceptions': _ty.NotRequired[bool], 
})