from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class General(_NS):
    
    def country_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Return a dictionary whose keys represent the ISO 3166-1 alpha 2 country code and values represent the English short name (used in ISO 3166/MA)"""
        ...