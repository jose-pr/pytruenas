from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .dns import Dns 
class Acme(_NS):
    
    dns: Dns