from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .device import Device
from .global import Global
from .instance import Instance
from .volume import Volume 
class Virt(_NS):
    
    device: Device
    global: Global
    instance: Instance
    volume: Volume