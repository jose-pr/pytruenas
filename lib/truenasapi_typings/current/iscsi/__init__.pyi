from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .auth import Auth
from .extent import Extent
from .global import Global
from .initiator import Initiator
from .portal import Portal
from .target import Target
from .targetextent import Targetextent 
class Iscsi(_NS):
    
    auth: Auth
    extent: Extent
    global: Global
    initiator: Initiator
    portal: Portal
    target: Target
    targetextent: Targetextent