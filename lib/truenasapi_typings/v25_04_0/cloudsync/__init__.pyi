from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .credentials import CloudsyncCredentials 
class Cloudsync(_NS):
    
    def onedrive_list_drives(self,
        onedrive_list_drives:onedrive_list_drives,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[CloudSyncOneDriveListDrivesDrive]:
        """Lists all available drives and their types for given Microsoft OneDrive credentials."""
        ...
    credentials: CloudsyncCredentials
onedrive_list_drives = _ty.TypedDict('onedrive_list_drives', {
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str, 
})
CloudSyncOneDriveListDrivesDrive = _ty.TypedDict('CloudSyncOneDriveListDrivesDrive', {
    'drive_id': str,
    'drive_type': str,
    'name': str,
    'description': str, 
})