from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Resilver(_NS):
    
    def _update(self,
        __selector:_jsonschema.JsonValue=None,
        **fields:_ty.Unpack[Data],
    ) -> UpdateReturn:
        """"""
        ...
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
        """Configure Pool Resilver Priority.

If `begin` time is greater than `end` time it means it will rollover the day, e.g. begin = "19:00", end = "05:00" will increase pool resilver priority from 19:00 of one day until 05:00 of the next day.

`weekday` follows crontab(5) values 0-7 (0 or 7 is Sun)."""
        ...
Data = _ty.TypedDict('Data', {
    'begin': _ty.NotRequired[str],
    'end': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'weekday': _ty.NotRequired[list[int]], 
})
ConfigReturn = _ty.TypedDict('ConfigReturn', {
    'id': int,
    'begin': _ty.NotRequired[str],
    'end': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'weekday': _ty.NotRequired[list[int]], 
})
UpdateData = _ty.TypedDict('UpdateData', {
    'begin': _ty.NotRequired[str],
    'end': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'weekday': _ty.NotRequired[list[int]], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'begin': _ty.NotRequired[str],
    'end': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'weekday': _ty.NotRequired[list[int]], 
})