from pytruenas import Namespace as _NS 
class Catalog(_NS):
    
    def apps(
        catalog_apps_options,
    ) -> CatalogApps:
        """Retrieve apps details for `label` catalog.

`options.cache` is a boolean which when set will try to get apps details for `label` catalog from cache if available.

`options.cache_only` is a boolean which when set will force usage of cache only for retrieving catalog information. If the content for the catalog in question is not cached, no content would be returned. If `options.cache` is unset, this attribute has no effect.

`options.retrieve_all_trains` is a boolean value which when set will retrieve information for all the trains present in the catalog ( it is set by default ).

`options.trains` is a list of train name(s) which will allow selective filtering to retrieve only information of desired trains in a catalog. If `options.retrieve_all_trains` is set, it has precedence over `options.train`."""
        ...
    def config(
    ) -> CatalogConfig:
        """"""
        ...
    def get_app_details(
        app_name,
        app_version_details,
    ) -> CatalogGet_app_details:
        """Retrieve information of `app_name` `app_version_details.catalog` catalog app."""
        ...
    def sync(
    ) -> CatalogSync:
        """Sync truenas catalog to retrieve latest changes from upstream."""
        ...
    def trains(
    ) -> CatalogTrains:
        """Retrieve available trains."""
        ...
    def update(
        catalog_update,
    ) -> CatalogUpdate:
        """Update catalog preferences."""
        ...
class CatalogApps:
    ...
class CatalogConfig:
    ...
class CatalogGet_app_details:
    ...
class CatalogSync:
    ...
class CatalogTrains:
    ...
class CatalogUpdate:
    ... 