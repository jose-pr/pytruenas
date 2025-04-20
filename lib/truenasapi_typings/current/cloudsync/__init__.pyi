from pytruenas import Namespace as _NS

from .credentials import CloudsyncCredentials
 
class Cloudsync(_NS):
    
    def onedrive_list_drives(
        
    ) -> CloudsyncOnedrive_list_drives:
        ...
     
    
    credentials: CloudsyncCredentials
     



class CloudsyncOnedrive_list_drives:
    ...
 