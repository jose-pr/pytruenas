from pytruenas import Namespace as _NS
import typing as _ty 
class Catalog(_NS):
    
    def apps(self,
        catalog_apps_options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CatalogApps:
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
        app_name,
        app_version_details,
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
    ) -> CatalogSync:
        """Sync truenas catalog to retrieve latest changes from upstream."""
        ...
    def trains(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CatalogTrains:
        """Retrieve available trains."""
        ...
    def update(self,
        catalog_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CatalogUpdate:
        """Update catalog preferences."""
        ...
class CatalogApps(_ty.TypedDict):
    ...
class CatalogConfig(_ty.TypedDict):
    ...
class CatalogGet_app_details(_ty.TypedDict):
    ...
class CatalogSync(_ty.TypedDict):
    ...
class CatalogTrains(_ty.TypedDict):
    ...
class CatalogUpdate(_ty.TypedDict):
    ... 