from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class TnConnect(_NS):
    
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ConfigReturn:
        """"""
        ...
    def generate_claim_token(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str:
        """Generate a claim token for TrueNAS Connect.

This is used to claim the system with TrueNAS Connect. When this endpoint will be called, a token will be generated which will be used to assist with initial setup with truenas connect."""
        ...
    def get_registration_uri(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> str:
        """Return the registration URI for TrueNAS Connect.

Before this endpoint is called, tn_connect must be enabled and a claim token must be generated - based off which this endpoint will return the registration URI for TrueNAS Connect."""
        ...
    def ip_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns IP choices which can be used with TrueNAS Connect."""
        ...
    def update(self,
        tn_connect_update:UpdateTnConnectUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update TrueNAS Connect configuration."""
        ...
ConfigReturn = _ty.TypedDict('ConfigReturn', {
    'id': int,
    'enabled': bool,
    'registration_details': _jsonschema.JsonObject,
    'ips': list[str],
    'status': str,
    'status_reason': str,
    'certificate': int|None,
    'account_service_base_url': str,
    'leca_service_base_url': str,
    'tnc_base_url': str,
    'heartbeat_url': str, 
})
UpdateTnConnectUpdate = _ty.TypedDict('UpdateTnConnectUpdate', {
    'enabled': _ty.NotRequired[bool],
    'ips': _ty.NotRequired[list[str]],
    'account_service_base_url': _ty.NotRequired[str],
    'leca_service_base_url': _ty.NotRequired[str],
    'tnc_base_url': _ty.NotRequired[str],
    'heartbeat_url': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'enabled': bool,
    'registration_details': _jsonschema.JsonObject,
    'ips': list[str],
    'status': str,
    'status_reason': str,
    'certificate': int|None,
    'account_service_base_url': str,
    'leca_service_base_url': str,
    'tnc_base_url': str,
    'heartbeat_url': str, 
})