from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Alertclasses(_NS):
    
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ConfigReturn:
        """"""
        ...
    def update(self,
        data:UpdateData,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update default Alert settings."""
        ...
ConfigReturn = _ty.TypedDict('ConfigReturn', {
    'id': int,
    'classes': _jsonschema.JsonObject, 
})
UpdateData = _ty.TypedDict('UpdateData', {
    'classes': _ty.NotRequired[_jsonschema.JsonObject], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'classes': _jsonschema.JsonObject, 
})