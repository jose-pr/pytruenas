from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Dataset(_NS):
    
    def details(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[_jsonschema.JsonObject]:
        """Retrieve all dataset(s) details outlining any services/tasks which might be consuming them."""
        ...
    def snapshot_count(self,
        dataset:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Returns snapshot count for specified `dataset`."""
        ...