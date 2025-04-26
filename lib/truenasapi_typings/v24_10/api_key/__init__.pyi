from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Api_key(_NS):
    
    def create(self,
        api_key_create:api_key_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Api_keyCreate:
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
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> Api_keyGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def my_keys(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ApiKeyEntry]:
        """Get the existing API keys for the currently-authenticated user"""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ApiKeyQueryResultItem]|ApiKeyQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        api_key_update:api_key_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ApiKeyEntryWithKey|ApiKeyEntry:
        """Update API Key `id`.

Specify `reset: true` to reset this API Key."""
        ...
api_key_create = _ty.TypedDict('api_key_create', {
    'name': str,
    'username': str|str,
    'expires_at': _ty.NotRequired[str|None], 
})
Api_keyCreate = _ty.TypedDict('Api_keyCreate', {
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
Api_keyGet_instance = _ty.TypedDict('Api_keyGet_instance', {
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
ApiKeyEntry = _ty.TypedDict('ApiKeyEntry', {
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
ApiKeyQueryResultItem = _ty.TypedDict('ApiKeyQueryResultItem', {
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
api_key_update = _ty.TypedDict('api_key_update', {
    'name': _ty.NotRequired[str],
    'expires_at': _ty.NotRequired[str|None],
    'reset': _ty.NotRequired[bool], 
})
ApiKeyEntryWithKey = _ty.TypedDict('ApiKeyEntryWithKey', {
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