from pytruenas import Namespace as _NS
import typing as _ty 
class Truenas(_NS):
    
    def accept_eula(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> TruenasAccept_eula:
        """Accept TrueNAS EULA."""
        ...
    def get_chassis_hardware(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> TruenasGet_chassis_hardware:
        """Returns what type of hardware this is, detected from dmidecode."""
        ...
    def get_eula(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> TruenasGet_eula:
        """Returns the TrueNAS End-User License Agreement (EULA)."""
        ...
    def is_eula_accepted(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> TruenasIs_eula_accepted:
        """Returns whether the EULA is accepted or not."""
        ...
    def is_ix_hardware(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> TruenasIs_ix_hardware:
        """Return a boolean value on whether this is hardware that iXsystems sells."""
        ...
    def is_production(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> TruenasIs_production:
        """Returns if system is marked as production."""
        ...
    def managed_by_truecommand(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> TruenasManaged_by_truecommand:
        """Returns whether TrueNAS is being managed by TrueCommand"""
        ...
    def set_production(self,
        production,
        attach_debug,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> TruenasSet_production:
        """Sets system production state and optionally sends initial debug."""
        ...
class TruenasAccept_eula(_ty.TypedDict):
    ...
class TruenasGet_chassis_hardware(_ty.TypedDict):
    ...
class TruenasGet_eula(_ty.TypedDict):
    ...
class TruenasIs_eula_accepted(_ty.TypedDict):
    ...
class TruenasIs_ix_hardware(_ty.TypedDict):
    ...
class TruenasIs_production(_ty.TypedDict):
    ...
class TruenasManaged_by_truecommand(_ty.TypedDict):
    ...
class TruenasSet_production(_ty.TypedDict):
    ... 