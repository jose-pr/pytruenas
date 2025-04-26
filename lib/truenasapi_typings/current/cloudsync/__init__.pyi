from pytruenas import Namespace as _NS
import typing as _ty
from .credentials import CloudsyncCredentials 
class Cloudsync(_NS):
    
    def onedrive_list_drives(self,
        onedrive_list_drives,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncOnedrive_list_drives:
        """Lists all available drives and their types for given Microsoft OneDrive credentials."""
        ...
    credentials: CloudsyncCredentials
class CloudsyncOnedrive_list_drives(_ty.TypedDict):
    ... 