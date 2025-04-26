from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .dns import AcmeDns 
class Acme(_NS):
    
    dns: AcmeDns