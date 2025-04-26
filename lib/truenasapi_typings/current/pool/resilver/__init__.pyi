from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class PoolResilver(_NS):
    
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolResilverConfig:
        """"""
        ...
    def update(self,
        data:data,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> PoolResilverUpdate:
        """Configure Pool Resilver Priority.

If `begin` time is greater than `end` time it means it will rollover the day, e.g. begin = "19:00", end = "05:00" will increase pool resilver priority from 19:00 of one day until 05:00 of the next day.

`weekday` follows crontab(5) values 0-7 (0 or 7 is Sun)."""
        ...
PoolResilverConfig = _ty.TypedDict('PoolResilverConfig', {
    'id': int,
    'begin': _ty.NotRequired[str],
    'end': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'weekday': _ty.NotRequired[list[int]], 
})
data = _ty.TypedDict('data', {
    'begin': _ty.NotRequired[str],
    'end': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'weekday': _ty.NotRequired[list[int]], 
})
PoolResilverUpdate = _ty.TypedDict('PoolResilverUpdate', {
    'id': int,
    'begin': _ty.NotRequired[str],
    'end': _ty.NotRequired[str],
    'enabled': _ty.NotRequired[bool],
    'weekday': _ty.NotRequired[list[int]], 
})