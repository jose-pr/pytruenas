from pytruenas import Namespace as _NS
import typing as _ty 
class Disk(_NS):
    
    def temperature_alerts(self,
        names,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> DiskTemperature_alerts:
        """Returns existing temperature alerts for specified disk `names.`"""
        ...
class DiskTemperature_alerts(_ty.TypedDict):
    ... 