from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .authenticator import AcmeDnsAuthenticator 
class AcmeDns(_NS):
    
    authenticator: AcmeDnsAuthenticator