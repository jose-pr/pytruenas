from pytruenas import Namespace as _NS
import typing as _ty
from .dns import AcmeDns 
class Acme(_NS):
    
    dns: AcmeDns 