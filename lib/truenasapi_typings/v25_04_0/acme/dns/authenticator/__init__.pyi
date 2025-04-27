from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Authenticator(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[DnsAuthenticatorCreate],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[DnsAuthenticatorUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[DnsAuthenticatorUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def authenticator_schemas(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AuthenticatorSchemasACMEDNSAuthenticatorSchema]:
        """Get the schemas for all DNS providers we support for ACME DNS Challenge and the respective attributes required for connecting to them while validating a DNS Challenge"""
        ...
    def create(self,
        dns_authenticator_create:CreateDnsAuthenticatorCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
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
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryACMEDNSAuthenticatorQueryResultItem]|QueryACMEDNSAuthenticatorQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        dns_authenticator_update:UpdateDnsAuthenticatorUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update DNS Authenticator of `id`"""
        ...
DnsAuthenticatorCreate = _ty.TypedDict('DnsAuthenticatorCreate', {
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue,
    'name': str, 
})
DnsAuthenticatorUpdate = _ty.TypedDict('DnsAuthenticatorUpdate', {
    'attributes': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue],
    'name': _ty.NotRequired[str], 
})
AuthenticatorSchemasACMEDNSAuthenticatorSchema = _ty.TypedDict('AuthenticatorSchemasACMEDNSAuthenticatorSchema', {
    'key': str,
    'schema': _jsonschema.JsonValue, 
})
CreateDnsAuthenticatorCreate = _ty.TypedDict('CreateDnsAuthenticatorCreate', {
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue,
    'name': str, 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue,
    'name': str, 
})
GetInstanceOptions = _ty.TypedDict('GetInstanceOptions', {
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
GetInstanceReturn = _ty.TypedDict('GetInstanceReturn', {
    'id': int,
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue,
    'name': str, 
})
QueryOptions = _ty.TypedDict('QueryOptions', {
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
QueryACMEDNSAuthenticatorQueryResultItem = _ty.TypedDict('QueryACMEDNSAuthenticatorQueryResultItem', {
    'id': _ty.NotRequired[int],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue],
    'name': _ty.NotRequired[str], 
})
UpdateDnsAuthenticatorUpdate = _ty.TypedDict('UpdateDnsAuthenticatorUpdate', {
    'attributes': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue],
    'name': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'attributes': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue,
    'name': str, 
})