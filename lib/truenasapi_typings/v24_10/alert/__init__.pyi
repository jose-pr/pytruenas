from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Alert(_NS):
    
    def dismiss(self,
        uuid:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Dismiss `id` alert."""
        ...
    def list(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[Alert]:
        """List all types of alerts including active/dismissed currently in the system."""
        ...
    def list_categories(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AlertCategory]:
        """List all types of alerts which the system can issue."""
        ...
    def list_policies(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[str]:
        """List all alert policies which indicate the frequency of the alerts."""
        ...
    def restore(self,
        uuid:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Restore `id` alert which had been dismissed."""
        ...
Alert = _ty.TypedDict('Alert', {
    'uuid': str,
    'source': str,
    'klass': str,
    'args': _jsonschema.JsonValue,
    'node': str,
    'key': str,
    'datetime': str,
    'last_occurrence': str,
    'dismissed': bool,
    'mail': _jsonschema.JsonValue,
    'text': str,
    'id': str,
    'level': str,
    'formatted': str|None,
    'one_shot': bool, 
})
AlertCategory = _ty.TypedDict('AlertCategory', {
    'id': str,
    'title': str,
    'classes': _jsonschema.JsonArray, 
})