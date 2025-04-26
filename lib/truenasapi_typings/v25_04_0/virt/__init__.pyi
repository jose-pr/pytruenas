from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .device import VirtDevice
from .global_ import VirtGlobal
from .instance import VirtInstance
from .volume import VirtVolume 
class Virt(_NS):
    
    device: VirtDevice
    global_: VirtGlobal
    instance: VirtInstance
    volume: VirtVolume