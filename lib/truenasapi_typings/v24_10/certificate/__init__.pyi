from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Certificate(_NS):
    
    def acme_server_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Dictionary of popular ACME Servers with their directory URI endpoints which we display automatically in the UI"""
        ...
    def country_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns country choices for creating a certificate/csr."""
        ...
    def ec_curve_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Dictionary of supported EC curves."""
        ...
    def extended_key_usage_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Dictionary of names that can be used in the ExtendedKeyUsage attribute of a certificate request."""
        ...