from pytruenas import Namespace as _NS
import typing as _ty
from .authenticator import AcmeDnsAuthenticator 
class AcmeDns(_NS):
    
    authenticator: AcmeDnsAuthenticator 