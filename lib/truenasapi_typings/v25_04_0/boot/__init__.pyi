from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .environment import BootEnvironment 
class Boot(_NS):
    
    environment: BootEnvironment