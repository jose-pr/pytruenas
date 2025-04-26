from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
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
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertclassesUpdate:
        """Update default Alert settings."""
        ...
AlertclassesConfig = _ty.TypedDict('AlertclassesConfig', {
    'id': int,
    'classes': _jsonschema.JsonObject, 
})
data = _ty.TypedDict('data', {
    'classes': _ty.NotRequired[_jsonschema.JsonObject], 
})
AlertclassesUpdate = _ty.TypedDict('AlertclassesUpdate', {
    'id': int,
    'classes': _jsonschema.JsonObject, 
})