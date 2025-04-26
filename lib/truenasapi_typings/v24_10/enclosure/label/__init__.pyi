from pytruenas import Namespace as _NS
import typing as _ty 
class EnclosureLabel(_NS):
    
    def set(self,
        id,
        label,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> EnclosureLabelSet:
        """"""
        ...
class EnclosureLabelSet(_ty.TypedDict):
    ... 