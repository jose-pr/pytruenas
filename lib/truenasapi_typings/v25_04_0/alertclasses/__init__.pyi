from pytruenas import Namespace as _NS
import typing as _ty 
class Alertclasses(_NS):
    
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertclassesConfig:
        """"""
        ...
    def update(self,
        data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertclassesUpdate:
        """Update default Alert settings."""
        ...
class AlertclassesConfig(_ty.TypedDict):
    ...
class AlertclassesUpdate(_ty.TypedDict):
    ... 