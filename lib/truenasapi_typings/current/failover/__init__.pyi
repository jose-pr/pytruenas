from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .reboot import Reboot 
class Failover(_NS):
    
    reboot: Reboot