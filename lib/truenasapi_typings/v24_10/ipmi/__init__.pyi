from pytruenas import Namespace as _NS
import typing as _ty 
class Ipmi(_NS):
    
    def is_loaded(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> IpmiIs_loaded:
        """Returns a boolean value indicating if /dev/ipmi0 is loaded."""
        ...
class IpmiIs_loaded(_ty.TypedDict):
    ... 