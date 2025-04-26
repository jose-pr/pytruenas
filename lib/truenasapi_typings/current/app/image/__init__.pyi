from pytruenas import Namespace as _NS
import typing as _ty 
class AppImage(_NS):
    
    def delete(self,
        image_id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppImageDelete:
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
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppImageGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def pull(self,
        image_pull,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppImagePull:
        """`image` is the name of the image to pull. Format for the name is "registry/repo/image:v1.2.3" where registry may be omitted and it will default to docker registry in this case. It can or cannot contain the tag - this will be passed as is to docker so this should be analogous to what `docker pull` expects.

`auth_config` should be specified if image to be retrieved is under a private repository."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppImageQuery:
        """Query all docker images with `query-filters` and `query-options`.

`query-options.extra.parse_tags` is a boolean which when set will have normalized tags to be retrieved."""
        ...
class AppImageDelete(_ty.TypedDict):
    ...
class AppImageDockerhub_rate_limit(_ty.TypedDict):
    ...
class AppImageGet_instance(_ty.TypedDict):
    ...
class AppImagePull(_ty.TypedDict):
    ...
class AppImageQuery(_ty.TypedDict):
    ... 