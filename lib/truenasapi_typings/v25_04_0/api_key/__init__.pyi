from pytruenas import Namespace as _NS 
class Api_key(_NS):
    
    def create(self,
        api_key_create,
    ) -> Api_keyCreate:
        """Creates API Key.

`name` is a user-readable name for key."""
        ...
    def delete(self,
        id,
    ) -> Api_keyDelete:
        """Delete API Key `id`."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> Api_keyGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def my_keys(self,
    ) -> Api_keyMy_keys:
        """Get the existing API keys for the currently-authenticated user"""
        ...
    def query(self,
        filters,
        options,
    ) -> Api_keyQuery:
        """"""
        ...
    def update(self,
        id,
        api_key_update,
    ) -> Api_keyUpdate:
        """Update API Key `id`.

Specify `reset: true` to reset this API Key."""
        ...
class Api_keyCreate:
    ...
class Api_keyDelete:
    ...
class Api_keyGet_instance:
    ...
class Api_keyMy_keys:
    ...
class Api_keyQuery:
    ...
class Api_keyUpdate:
    ... 