from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .nfs import SharingNfs
from .smb import SharingSmb 
class Sharing(_NS):
    
    nfs: SharingNfs
    smb: SharingSmb