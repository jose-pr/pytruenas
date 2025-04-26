from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Device(_NS):
    
    def get_info(self,
        data:DeviceGetInfoDisk|DeviceGetInfoOther,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject|_jsonschema.JsonObject|list[SerialInfo]|list[GPUInfo]:
        """Get info for `type` device."""
        ...
DeviceGetInfoDisk = _ty.TypedDict('DeviceGetInfoDisk', {
    'type': str,
    'get_partitions': _ty.NotRequired[bool],
    'serials_only': _ty.NotRequired[bool], 
})
DeviceGetInfoOther = _ty.TypedDict('DeviceGetInfoOther', {
    'type': str, 
})
SerialInfo = _ty.TypedDict('SerialInfo', {
    'name': str,
    'location': str,
    'drivername': str,
    'start': str,
    'size': int,
    'description': str, 
})
GPUInfo = _ty.TypedDict('GPUInfo', {
    'addr': _jsonschema.JsonValue,
    'description': str,
    'devices': _jsonschema.JsonArray,
    'vendor': str|None,
    'available_to_host': bool,
    'uses_system_critical_devices': bool,
    'critical_reason': str|None, 
})