from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Catalog(_NS):
    
    def apps(self,
        catalog_apps_options:catalog_apps_options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Retrieve apps details for `label` catalog.

`options.cache` is a boolean which when set will try to get apps details for `label` catalog from cache if available.

`options.cache_only` is a boolean which when set will force usage of cache only for retrieving catalog information. If the content for the catalog in question is not cached, no content would be returned. If `options.cache` is unset, this attribute has no effect.

`options.retrieve_all_trains` is a boolean value which when set will retrieve information for all the trains present in the catalog ( it is set by default ).

`options.trains` is a list of train name(s) which will allow selective filtering to retrieve only information of desired trains in a catalog. If `options.retrieve_all_trains` is set, it has precedence over `options.train`."""
        ...
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CatalogConfig:
        """"""
        ...
    def get_app_details(self,
        app_name:str,
        app_version_details:app_version_details,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CatalogGet_app_details:
        """Retrieve information of `app_name` `app_version_details.catalog` catalog app."""
        ...
    def sync(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Sync truenas catalog to retrieve latest changes from upstream."""
        ...
    def trains(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[str]:
        """Retrieve available trains."""
        ...
    def update(self,
        catalog_update:catalog_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CatalogUpdate:
        """Update catalog preferences."""
        ...
catalog_apps_options = _ty.TypedDict('catalog_apps_options', {
    'cache': _ty.NotRequired[bool],
    'cache_only': _ty.NotRequired[bool],
    'retrieve_all_trains': _ty.NotRequired[bool],
    'trains': _ty.NotRequired[list[str]], 
})
CatalogConfig = _ty.TypedDict('CatalogConfig', {
    'id': str,
    'label': str,
    'preferred_trains': list[str],
    'location': str, 
})
app_version_details = _ty.TypedDict('app_version_details', {
    'train': str, 
})
CatalogGet_app_details = _ty.TypedDict('CatalogGet_app_details', {
    'app_readme': str|None,
    'categories': list[str],
    'description': str,
    'healthy': bool,
    'healthy_error': _ty.NotRequired[str|None],
    'home': str,
    'location': str,
    'latest_version': str|None,
    'latest_app_version': str|None,
    'latest_human_version': str|None,
    'last_update': str|None,
    'name': str,
    'recommended': bool,
    'title': str,
    'maintainers': _jsonschema.JsonArray,
    'tags': list[str],
    'screenshots': list[str],
    'sources': list[str],
    'icon_url': _ty.NotRequired[str|None], 
})
catalog_update = _ty.TypedDict('catalog_update', {
    'preferred_trains': _ty.NotRequired[list[str]], 
})
CatalogUpdate = _ty.TypedDict('CatalogUpdate', {
    'id': str,
    'label': str,
    'preferred_trains': list[str],
    'location': str, 
})