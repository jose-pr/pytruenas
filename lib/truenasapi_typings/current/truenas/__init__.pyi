from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Truenas(_NS):
    
    def accept_eula(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Accept TrueNAS EULA."""
        ...
    def get_chassis_hardware(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str:
        """Returns what type of hardware this is, detected from dmidecode."""
        ...
    def get_eula(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str|None:
        """Returns the TrueNAS End-User License Agreement (EULA)."""
        ...
    def is_eula_accepted(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Returns whether the EULA is accepted or not."""
        ...
    def is_ix_hardware(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Return a boolean value on whether this is hardware that iXsystems sells."""
        ...
    def is_production(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Returns if system is marked as production."""
        ...
    def managed_by_truecommand(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Returns whether TrueNAS is being managed by TrueCommand"""
        ...
    def set_production(self,
        production:bool,
        attach_debug:bool=False,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject|None:
        """Sets system production state and optionally sends initial debug."""
        ...