from pytruenas import Namespace as _NS
from .nfs import SharingNfs
from .smb import SharingSmb 
class Sharing(_NS):
    
    nfs: SharingNfs
    smb: SharingSmb 