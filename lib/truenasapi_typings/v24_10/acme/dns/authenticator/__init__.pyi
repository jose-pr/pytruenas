from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class AcmeDnsAuthenticator(_NS):
    
    def authenticator_schemas(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ACMEDNSAuthenticatorSchema]:
        """Get the schemas for all DNS providers we support for ACME DNS Challenge and the respective attributes required for connecting to them while validating a DNS Challenge"""
        ...
    def create(self,
        dns_authenticator_create:dns_authenticator_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AcmeDnsAuthenticatorCreate:
        """Create a DNS Authenticator

Create a specific DNS Authenticator containing required authentication details for the said provider to successfully connect with it"""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete DNS Authenticator of `id`"""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AcmeDnsAuthenticatorGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ACMEDNSAuthenticatorQueryResultItem]|ACMEDNSAuthenticatorQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        dns_authenticator_update:dns_authenticator_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AcmeDnsAuthenticatorUpdate:
        """Update DNS Authenticator of `id`"""
        ...
ACMEDNSAuthenticatorSchema = _ty.TypedDict('ACMEDNSAuthenticatorSchema', {
    'key': str,
    'schema': _jsonschema.JsonValue, 
})
dns_authenticator_create = _ty.TypedDict('dns_authenticator_create', {
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue,
    'name': str, 
})
AcmeDnsAuthenticatorCreate = _ty.TypedDict('AcmeDnsAuthenticatorCreate', {
    'id': int,
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue,
    'name': str, 
})
options = _ty.TypedDict('options', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
AcmeDnsAuthenticatorGet_instance = _ty.TypedDict('AcmeDnsAuthenticatorGet_instance', {
    'id': int,
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue,
    'name': str, 
})
ACMEDNSAuthenticatorQueryResultItem = _ty.TypedDict('ACMEDNSAuthenticatorQueryResultItem', {
    'id': _ty.NotRequired[int],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue],
    'name': _ty.NotRequired[str], 
})
dns_authenticator_update = _ty.TypedDict('dns_authenticator_update', {
    'attributes': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue],
    'name': _ty.NotRequired[str], 
})
AcmeDnsAuthenticatorUpdate = _ty.TypedDict('AcmeDnsAuthenticatorUpdate', {
    'id': int,
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue,
    'name': str, 
})