from pytruenas import Namespace as _NS
import typing as _ty 
class SystemReboot(_NS):
    
    def info(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SystemRebootInfo:
        """"""
        ...
class SystemRebootInfo(_ty.TypedDict):
    ... 