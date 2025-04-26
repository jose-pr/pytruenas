from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class AppImage(_NS):
    
    def delete(self,
        image_id:str,
        options:options={'force': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete docker image `image_id`.

`options.force` when set will force delete the image regardless of the state of containers and should be used cautiously."""
        ...
    def dockerhub_rate_limit(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppImageDockerhub_rate_limit:
        """Returns the current rate limit information for Docker Hub registry.

Please refer to https://docs.docker.com/docker-hub/download-rate-limit/ for more information."""
        ...
    def get_instance(self,
        id:str,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppImageGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def pull(self,
        image_pull:image_pull,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """`image` is the name of the image to pull. Format for the name is "registry/repo/image:v1.2.3" where registry may be omitted and it will default to docker registry in this case. It can or cannot contain the tag - this will be passed as is to docker so this should be analogous to what `docker pull` expects.

`auth_config` should be specified if image to be retrieved is under a private repository."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AppImageQueryResultItem]|AppImageQueryResultItem|int:
        """Query all docker images with `query-filters` and `query-options`.

`query-options.extra.parse_tags` is a boolean which when set will have normalized tags to be retrieved."""
        ...
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
AppImageDockerhub_rate_limit = _ty.TypedDict('AppImageDockerhub_rate_limit', {
    'total_pull_limit': _ty.NotRequired[int|None],
    'total_time_limit_in_secs': _ty.NotRequired[int|None],
    'remaining_pull_limit': _ty.NotRequired[int|None],
    'remaining_time_limit_in_secs': _ty.NotRequired[int|None],
    'error': _ty.NotRequired[str|None], 
})
AppImageGet_instance = _ty.TypedDict('AppImageGet_instance', {
    'id': str,
    'repo_tags': list[str],
    'repo_digests': list[str],
    'size': int,
    'dangling': bool,
    'update_available': bool,
    'created': str,
    'author': str,
    'comment': str,
    'parsed_repo_tags': _ty.NotRequired[_jsonschema.JsonArray|None], 
})
image_pull = _ty.TypedDict('image_pull', {
    'auth_config': _ty.NotRequired[_jsonschema.JsonValue|None],
    'image': str, 
})
AppImageQueryResultItem = _ty.TypedDict('AppImageQueryResultItem', {
    'id': _ty.NotRequired[str],
    'repo_tags': _ty.NotRequired[list[str]],
    'repo_digests': _ty.NotRequired[list[str]],
    'size': _ty.NotRequired[int],
    'dangling': _ty.NotRequired[bool],
    'update_available': _ty.NotRequired[bool],
    'created': _ty.NotRequired[str],
    'author': _ty.NotRequired[str],
    'comment': _ty.NotRequired[str],
    'parsed_repo_tags': _ty.NotRequired[_jsonschema.JsonArray|None], 
})