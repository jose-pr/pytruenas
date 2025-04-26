from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .credentials import Credentials 
class Cloudsync(_NS):
    
    def onedrive_list_drives(self,
        onedrive_list_drives:OnedriveListDrivesOnedriveListDrives,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[OnedriveListDrivesCloudSyncOneDriveListDrivesDrive]:
        """Lists all available drives and their types for given Microsoft OneDrive credentials."""
        ...
    credentials: Credentials
OnedriveListDrivesOnedriveListDrives = _ty.TypedDict('OnedriveListDrivesOnedriveListDrives', {
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str, 
})
OnedriveListDrivesCloudSyncOneDriveListDrivesDrive = _ty.TypedDict('OnedriveListDrivesCloudSyncOneDriveListDrivesDrive', {
    'drive_id': str,
    'drive_type': str,
    'name': str,
    'description': str, 
})