from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Disk(_NS):
    
    def temperature_alerts(self,
        names:list[str],
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[TemperatureAlertsAlert]:
        """Returns existing temperature alerts for specified disk `names.`"""
        ...
TemperatureAlertsAlert = _ty.TypedDict('TemperatureAlertsAlert', {
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