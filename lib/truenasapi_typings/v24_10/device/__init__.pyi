from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Device(_NS):
    
    def get_info(self,
        data:GetInfoDeviceGetInfoDisk|GetInfoDeviceGetInfoOther,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject|_jsonschema.JsonObject|list[GetInfoSerialInfo]|list[GetInfoGPUInfo]:
        """Get info for `type` device."""
        ...
GetInfoDeviceGetInfoDisk = _ty.TypedDict('GetInfoDeviceGetInfoDisk', {
    'type': str,
    'get_partitions': _ty.NotRequired[bool],
    'serials_only': _ty.NotRequired[bool], 
})
GetInfoDeviceGetInfoOther = _ty.TypedDict('GetInfoDeviceGetInfoOther', {
    'type': str, 
})
GetInfoSerialInfo = _ty.TypedDict('GetInfoSerialInfo', {
    'name': str,
    'location': str,
    'drivername': str,
    'start': str,
    'size': int,
    'description': str, 
})
GetInfoGPUInfo = _ty.TypedDict('GetInfoGPUInfo', {
    'addr': _jsonschema.JsonValue,
    'description': str,
    'devices': _jsonschema.JsonArray,
    'vendor': str|None,
    'available_to_host': bool,
    'uses_system_critical_devices': bool,
    'critical_reason': str|None, 
})