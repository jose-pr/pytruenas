from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .nfs import Nfs
from .smb import Smb 
class Sharing(_NS):
    
    nfs: Nfs
    smb: Smb