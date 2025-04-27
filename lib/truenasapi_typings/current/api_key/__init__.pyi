from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class ApiKey(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[ApiKeyCreate],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[ApiKeyUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def _upsert(self,
        __selector:int|_ty.Sequence[str],
        **fields:_ty.Unpack[ApiKeyUpdate],
    ) -> UpdateReturn:
        """"""
        ...
    def create(self,
        api_key_create:CreateApiKeyCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Creates API Key.

`name` is a user-readable name for key."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete API Key `id`."""
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
    def my_keys(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[MyKeysApiKeyEntry]:
        """Get the existing API keys for the currently-authenticated user"""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryApiKeyQueryResultItem]|QueryApiKeyQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        api_key_update:UpdateApiKeyUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateApiKeyEntryWithKey|UpdateApiKeyEntry:
        """Update API Key `id`.

Specify `reset: true` to reset this API Key."""
        ...
ApiKeyCreate = _ty.TypedDict('ApiKeyCreate', {
    'name': str,
    'username': str|str,
    'expires_at': _ty.NotRequired[str|None], 
})
ApiKeyUpdate = _ty.TypedDict('ApiKeyUpdate', {
    'name': _ty.NotRequired[str],
    'expires_at': _ty.NotRequired[str|None],
    'reset': _ty.NotRequired[bool], 
})
CreateApiKeyCreate = _ty.TypedDict('CreateApiKeyCreate', {
    'name': str,
    'username': str|str,
    'expires_at': _ty.NotRequired[str|None], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'name': str,
    'username': str|str,
    'user_identifier': int|str,
    'keyhash': str,
    'created_at': str,
    'expires_at': _ty.NotRequired[str|None],
    'local': bool,
    'revoked': bool,
    'key': str, 
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
    'name': str,
    'username': str|str,
    'user_identifier': int|str,
    'keyhash': str,
    'created_at': str,
    'expires_at': _ty.NotRequired[str|None],
    'local': bool,
    'revoked': bool, 
})
MyKeysApiKeyEntry = _ty.TypedDict('MyKeysApiKeyEntry', {
    'id': int,
    'name': str,
    'username': str|str,
    'user_identifier': int|str,
    'keyhash': str,
    'created_at': str,
    'expires_at': _ty.NotRequired[str|None],
    'local': bool,
    'revoked': bool, 
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
QueryApiKeyQueryResultItem = _ty.TypedDict('QueryApiKeyQueryResultItem', {
    'id': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'username': _ty.NotRequired[str|str],
    'user_identifier': _ty.NotRequired[int|str],
    'keyhash': _ty.NotRequired[str],
    'created_at': _ty.NotRequired[str],
    'expires_at': _ty.NotRequired[str|None],
    'local': _ty.NotRequired[bool],
    'revoked': _ty.NotRequired[bool], 
})
UpdateApiKeyUpdate = _ty.TypedDict('UpdateApiKeyUpdate', {
    'name': _ty.NotRequired[str],
    'expires_at': _ty.NotRequired[str|None],
    'reset': _ty.NotRequired[bool], 
})
UpdateApiKeyEntryWithKey = _ty.TypedDict('UpdateApiKeyEntryWithKey', {
    'id': int,
    'name': str,
    'username': str|str,
    'user_identifier': int|str,
    'keyhash': str,
    'created_at': str,
    'expires_at': _ty.NotRequired[str|None],
    'local': bool,
    'revoked': bool,
    'key': str, 
})
UpdateApiKeyEntry = _ty.TypedDict('UpdateApiKeyEntry', {
    'id': int,
    'name': str,
    'username': str|str,
    'user_identifier': int|str,
    'keyhash': str,
    'created_at': str,
    'expires_at': _ty.NotRequired[str|None],
    'local': bool,
    'revoked': bool, 
})