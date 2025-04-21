from pytruenas import Namespace as _NS
from .credentials import CloudsyncCredentials 
class Cloudsync(_NS):
    
    def onedrive_list_drives(
        onedrive_list_drives,
    ) -> CloudsyncOnedrive_list_drives:
        """Lists all available drives and their types for given Microsoft OneDrive credentials."""
        ...
    credentials: CloudsyncCredentials
class CloudsyncOnedrive_list_drives:
    ... 