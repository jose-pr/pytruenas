from pytruenas import Namespace as _NS
import typing as _ty 
class Alert(_NS):
    
    def dismiss(self,
        uuid,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertDismiss:
        """Dismiss `id` alert."""
        ...
    def list(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertList:
        """List all types of alerts including active/dismissed currently in the system."""
        ...
    def list_categories(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertList_categories:
        """List all types of alerts which the system can issue."""
        ...
    def list_policies(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertList_policies:
        """List all alert policies which indicate the frequency of the alerts."""
        ...
    def restore(self,
        uuid,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertRestore:
        """Restore `id` alert which had been dismissed."""
        ...
class AlertDismiss(_ty.TypedDict):
    ...
class AlertList(_ty.TypedDict):
    ...
class AlertList_categories(_ty.TypedDict):
    ...
class AlertList_policies(_ty.TypedDict):
    ...
class AlertRestore(_ty.TypedDict):
    ... 