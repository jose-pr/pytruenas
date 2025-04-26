from pytruenas import Namespace as _NS
import typing as _ty 
class Device(_NS):
    
    def get_info(self,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DeviceGet_info:
        """Get info for `type` device."""
        ...
class DeviceGet_info(_ty.TypedDict):
    ... 