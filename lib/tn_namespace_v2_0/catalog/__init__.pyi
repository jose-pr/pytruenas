
from pytruenas import TrueNASClient
from pytruenas.base import Namespace

import typing
class Catalog(
    Namespace
    ):
    _namespace:typing.Literal['catalog']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        catalog_create:'CatalogCreate'={},
    /) -> 'CatalogCreateReturns': 
        """
        `catalog_create.preferred_trains` specifies trains which will be displayed in the UI directly for a user.

        Parameters
        ----------
        catalog_create:
            catalog_create
        Returns
        -------
        CatalogCreateReturns:
            catalog_create_returns
        """
        ...
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
    })
    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreateReturns = typing.TypedDict('CatalogCreateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
    })
    ItemDetails = typing.TypedDict('ItemDetails', {
            'name':'str',
            'categories':'list[str]',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'app_readme':'typing.Optional[str]',
            'location':'str',
            'healthy':'bool',
            'recommended':'bool',
            'healthy_error':'typing.Optional[str]',
            'versions':'dict[str]',
            'latest_version':'typing.Optional[str]',
            'latest_app_version':'typing.Optional[str]',
            'latest_human_version':'typing.Optional[str]',
            'last_update':'typing.Optional[str]',
            'icon_url':'typing.Optional[str]',
            'home':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'bool',
            'cache_only':'bool',
            'retrieve_all_trains':'bool',
            'trains':'list[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    CachingProgress_ = typing.TypedDict('CachingProgress_', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry = typing.TypedDict('CatalogEntry', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress_',
            'caching_job':'dict[str]',
    })
    CachingProgress__ = typing.TypedDict('CachingProgress__', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry_ = typing.TypedDict('CatalogEntry_', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress__',
            'caching_job':'dict[str]',
    })
    CachingProgress___ = typing.TypedDict('CachingProgress___', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry__ = typing.TypedDict('CatalogEntry__', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress___',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
    })
    CachingProgress____ = typing.TypedDict('CachingProgress____', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogUpdateReturns = typing.TypedDict('CatalogUpdateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress____',
            'caching_job':'dict[str]',
    })
    @typing.overload
    def delete(self, 
        label:'str',
    /) -> 'bool': 
        """
        

        Parameters
        ----------
        label:
            label
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
    })
    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreateReturns = typing.TypedDict('CatalogCreateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
    })
    ItemDetails = typing.TypedDict('ItemDetails', {
            'name':'str',
            'categories':'list[str]',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'app_readme':'typing.Optional[str]',
            'location':'str',
            'healthy':'bool',
            'recommended':'bool',
            'healthy_error':'typing.Optional[str]',
            'versions':'dict[str]',
            'latest_version':'typing.Optional[str]',
            'latest_app_version':'typing.Optional[str]',
            'latest_human_version':'typing.Optional[str]',
            'last_update':'typing.Optional[str]',
            'icon_url':'typing.Optional[str]',
            'home':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'bool',
            'cache_only':'bool',
            'retrieve_all_trains':'bool',
            'trains':'list[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    CachingProgress_ = typing.TypedDict('CachingProgress_', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry = typing.TypedDict('CatalogEntry', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress_',
            'caching_job':'dict[str]',
    })
    CachingProgress__ = typing.TypedDict('CachingProgress__', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry_ = typing.TypedDict('CatalogEntry_', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress__',
            'caching_job':'dict[str]',
    })
    CachingProgress___ = typing.TypedDict('CachingProgress___', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry__ = typing.TypedDict('CatalogEntry__', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress___',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
    })
    CachingProgress____ = typing.TypedDict('CachingProgress____', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogUpdateReturns = typing.TypedDict('CatalogUpdateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress____',
            'caching_job':'dict[str]',
    })
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
    })
    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreateReturns = typing.TypedDict('CatalogCreateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
    })
    ItemDetails = typing.TypedDict('ItemDetails', {
            'name':'str',
            'categories':'list[str]',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'app_readme':'typing.Optional[str]',
            'location':'str',
            'healthy':'bool',
            'recommended':'bool',
            'healthy_error':'typing.Optional[str]',
            'versions':'dict[str]',
            'latest_version':'typing.Optional[str]',
            'latest_app_version':'typing.Optional[str]',
            'latest_human_version':'typing.Optional[str]',
            'last_update':'typing.Optional[str]',
            'icon_url':'typing.Optional[str]',
            'home':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'bool',
            'cache_only':'bool',
            'retrieve_all_trains':'bool',
            'trains':'list[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    CachingProgress_ = typing.TypedDict('CachingProgress_', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry = typing.TypedDict('CatalogEntry', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress_',
            'caching_job':'dict[str]',
    })
    CachingProgress__ = typing.TypedDict('CachingProgress__', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry_ = typing.TypedDict('CatalogEntry_', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress__',
            'caching_job':'dict[str]',
    })
    CachingProgress___ = typing.TypedDict('CachingProgress___', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry__ = typing.TypedDict('CatalogEntry__', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress___',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
    })
    CachingProgress____ = typing.TypedDict('CachingProgress____', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogUpdateReturns = typing.TypedDict('CatalogUpdateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress____',
            'caching_job':'dict[str]',
    })
    @typing.overload
    def get_item_details(self, 
        item_name:'str',
        item_version_details:'ItemVersionDetails'={},
    /) -> 'ItemDetails': 
        """
        Retrieve information of `item_name` `item_version_details.catalog` catalog item.

        Parameters
        ----------
        item_name:
            item_name
        item_version_details:
            item_version_details
        Returns
        -------
        ItemDetails:
            item_details
        """
        ...
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
    })
    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreateReturns = typing.TypedDict('CatalogCreateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
    })
    ItemDetails = typing.TypedDict('ItemDetails', {
            'name':'str',
            'categories':'list[str]',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'app_readme':'typing.Optional[str]',
            'location':'str',
            'healthy':'bool',
            'recommended':'bool',
            'healthy_error':'typing.Optional[str]',
            'versions':'dict[str]',
            'latest_version':'typing.Optional[str]',
            'latest_app_version':'typing.Optional[str]',
            'latest_human_version':'typing.Optional[str]',
            'last_update':'typing.Optional[str]',
            'icon_url':'typing.Optional[str]',
            'home':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'bool',
            'cache_only':'bool',
            'retrieve_all_trains':'bool',
            'trains':'list[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    CachingProgress_ = typing.TypedDict('CachingProgress_', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry = typing.TypedDict('CatalogEntry', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress_',
            'caching_job':'dict[str]',
    })
    CachingProgress__ = typing.TypedDict('CachingProgress__', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry_ = typing.TypedDict('CatalogEntry_', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress__',
            'caching_job':'dict[str]',
    })
    CachingProgress___ = typing.TypedDict('CachingProgress___', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry__ = typing.TypedDict('CatalogEntry__', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress___',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
    })
    CachingProgress____ = typing.TypedDict('CachingProgress____', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogUpdateReturns = typing.TypedDict('CatalogUpdateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress____',
            'caching_job':'dict[str]',
    })
    @typing.overload
    def items(self, 
        label:'str',
        options:'Options'={},
    /) -> 'dict[str]': 
        """
        Retrieve item details for `label` catalog.
        
        `options.cache` is a boolean which when set will try to get items details for `label` catalog from cache
        if available.
        
        `options.cache_only` is a boolean which when set will force usage of cache only for retrieving catalog
        information. If the content for the catalog in question is not cached, no content would be returned. If
        `options.cache` is unset, this attribute has no effect.
        
        `options.retrieve_all_trains` is a boolean value which when set will retrieve information for all the trains
        present in the catalog ( it is set by default ).
        
        `options.trains` is a list of train name(s) which will allow selective filtering to retrieve only information
        of desired trains in a catalog. If `options.retrieve_all_trains` is set, it has precedence over `options.train`.

        Parameters
        ----------
        label:
            Retrieve item details for `label` catalog.
            `options.cache` is a boolean which when set will try to get items details for `label` catalog from cache
            if available.
        options:
            options
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "charts": {
                    "chia": {
                        "name": "chia",
                        "categories": [
                            "storage",
                            "crypto"
                        ],
                        "app_readme": "app readme here",
                        "location": "/mnt/evo/ix-applications/catalogs/github_com_truenas_charts_git_master/charts/chia",
                        "healthy": true,
                        "healthy_error": null,
                        "latest_version": "1.2.0",
                        "latest_app_version": "1.1.6",
                        "last_update": "2023-02-01 22:55:31",
                        "icon_url": "https://www.chia.net/img/chia_logo.svg",
                        "recommended": false,
                        "title": "Chia",
                        "description": "App description here",
                        "maintainers": [],
                        "tags": [
                            "finance",
                            "crypto",
                            "blockchain"
                        ],
                        "home": "https://www.chia.net/",
                        "screenshots": [],
                        "sources": []
                    }
                }
            }
            ```
        """
        ...
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
    })
    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreateReturns = typing.TypedDict('CatalogCreateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
    })
    ItemDetails = typing.TypedDict('ItemDetails', {
            'name':'str',
            'categories':'list[str]',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'app_readme':'typing.Optional[str]',
            'location':'str',
            'healthy':'bool',
            'recommended':'bool',
            'healthy_error':'typing.Optional[str]',
            'versions':'dict[str]',
            'latest_version':'typing.Optional[str]',
            'latest_app_version':'typing.Optional[str]',
            'latest_human_version':'typing.Optional[str]',
            'last_update':'typing.Optional[str]',
            'icon_url':'typing.Optional[str]',
            'home':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'bool',
            'cache_only':'bool',
            'retrieve_all_trains':'bool',
            'trains':'list[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    CachingProgress_ = typing.TypedDict('CachingProgress_', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry = typing.TypedDict('CatalogEntry', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress_',
            'caching_job':'dict[str]',
    })
    CachingProgress__ = typing.TypedDict('CachingProgress__', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry_ = typing.TypedDict('CatalogEntry_', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress__',
            'caching_job':'dict[str]',
    })
    CachingProgress___ = typing.TypedDict('CachingProgress___', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry__ = typing.TypedDict('CatalogEntry__', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress___',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
    })
    CachingProgress____ = typing.TypedDict('CachingProgress____', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogUpdateReturns = typing.TypedDict('CatalogUpdateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress____',
            'caching_job':'dict[str]',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[CatalogEntry], ForwardRef(CatalogEntry_), int, ForwardRef(CatalogEntry__)]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[CatalogEntry], ForwardRef(CatalogEntry_), int, ForwardRef(CatalogEntry__)]:
            
        """
        ...
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
    })
    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreateReturns = typing.TypedDict('CatalogCreateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
    })
    ItemDetails = typing.TypedDict('ItemDetails', {
            'name':'str',
            'categories':'list[str]',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'app_readme':'typing.Optional[str]',
            'location':'str',
            'healthy':'bool',
            'recommended':'bool',
            'healthy_error':'typing.Optional[str]',
            'versions':'dict[str]',
            'latest_version':'typing.Optional[str]',
            'latest_app_version':'typing.Optional[str]',
            'latest_human_version':'typing.Optional[str]',
            'last_update':'typing.Optional[str]',
            'icon_url':'typing.Optional[str]',
            'home':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'bool',
            'cache_only':'bool',
            'retrieve_all_trains':'bool',
            'trains':'list[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    CachingProgress_ = typing.TypedDict('CachingProgress_', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry = typing.TypedDict('CatalogEntry', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress_',
            'caching_job':'dict[str]',
    })
    CachingProgress__ = typing.TypedDict('CachingProgress__', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry_ = typing.TypedDict('CatalogEntry_', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress__',
            'caching_job':'dict[str]',
    })
    CachingProgress___ = typing.TypedDict('CachingProgress___', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry__ = typing.TypedDict('CatalogEntry__', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress___',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
    })
    CachingProgress____ = typing.TypedDict('CachingProgress____', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogUpdateReturns = typing.TypedDict('CatalogUpdateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress____',
            'caching_job':'dict[str]',
    })
    @typing.overload
    def sync(self, 
        label:'str',
    /) -> None: 
        """
        Sync `label` catalog to retrieve latest changes from upstream.

        Parameters
        ----------
        label:
            label
        Returns
        -------
        """
        ...
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
    })
    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreateReturns = typing.TypedDict('CatalogCreateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
    })
    ItemDetails = typing.TypedDict('ItemDetails', {
            'name':'str',
            'categories':'list[str]',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'app_readme':'typing.Optional[str]',
            'location':'str',
            'healthy':'bool',
            'recommended':'bool',
            'healthy_error':'typing.Optional[str]',
            'versions':'dict[str]',
            'latest_version':'typing.Optional[str]',
            'latest_app_version':'typing.Optional[str]',
            'latest_human_version':'typing.Optional[str]',
            'last_update':'typing.Optional[str]',
            'icon_url':'typing.Optional[str]',
            'home':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'bool',
            'cache_only':'bool',
            'retrieve_all_trains':'bool',
            'trains':'list[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    CachingProgress_ = typing.TypedDict('CachingProgress_', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry = typing.TypedDict('CatalogEntry', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress_',
            'caching_job':'dict[str]',
    })
    CachingProgress__ = typing.TypedDict('CachingProgress__', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry_ = typing.TypedDict('CatalogEntry_', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress__',
            'caching_job':'dict[str]',
    })
    CachingProgress___ = typing.TypedDict('CachingProgress___', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry__ = typing.TypedDict('CatalogEntry__', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress___',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
    })
    CachingProgress____ = typing.TypedDict('CachingProgress____', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogUpdateReturns = typing.TypedDict('CatalogUpdateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress____',
            'caching_job':'dict[str]',
    })
    @typing.overload
    def sync_all(self, 
    /) -> None: 
        """
        Refresh all available catalogs from upstream.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
    })
    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreateReturns = typing.TypedDict('CatalogCreateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
    })
    ItemDetails = typing.TypedDict('ItemDetails', {
            'name':'str',
            'categories':'list[str]',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'app_readme':'typing.Optional[str]',
            'location':'str',
            'healthy':'bool',
            'recommended':'bool',
            'healthy_error':'typing.Optional[str]',
            'versions':'dict[str]',
            'latest_version':'typing.Optional[str]',
            'latest_app_version':'typing.Optional[str]',
            'latest_human_version':'typing.Optional[str]',
            'last_update':'typing.Optional[str]',
            'icon_url':'typing.Optional[str]',
            'home':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'bool',
            'cache_only':'bool',
            'retrieve_all_trains':'bool',
            'trains':'list[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    CachingProgress_ = typing.TypedDict('CachingProgress_', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry = typing.TypedDict('CatalogEntry', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress_',
            'caching_job':'dict[str]',
    })
    CachingProgress__ = typing.TypedDict('CachingProgress__', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry_ = typing.TypedDict('CatalogEntry_', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress__',
            'caching_job':'dict[str]',
    })
    CachingProgress___ = typing.TypedDict('CachingProgress___', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry__ = typing.TypedDict('CatalogEntry__', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress___',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
    })
    CachingProgress____ = typing.TypedDict('CachingProgress____', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogUpdateReturns = typing.TypedDict('CatalogUpdateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress____',
            'caching_job':'dict[str]',
    })
    @typing.overload
    def update(self, 
        id:'str',
        catalog_update:'CatalogUpdate'={},
    /) -> 'CatalogUpdateReturns': 
        """
        

        Parameters
        ----------
        id:
            id
        catalog_update:
            catalog_update
        Returns
        -------
        CatalogUpdateReturns:
            catalog_update_returns
        """
        ...
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
    })
    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreateReturns = typing.TypedDict('CatalogCreateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
    })
    ItemDetails = typing.TypedDict('ItemDetails', {
            'name':'str',
            'categories':'list[str]',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'app_readme':'typing.Optional[str]',
            'location':'str',
            'healthy':'bool',
            'recommended':'bool',
            'healthy_error':'typing.Optional[str]',
            'versions':'dict[str]',
            'latest_version':'typing.Optional[str]',
            'latest_app_version':'typing.Optional[str]',
            'latest_human_version':'typing.Optional[str]',
            'last_update':'typing.Optional[str]',
            'icon_url':'typing.Optional[str]',
            'home':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'bool',
            'cache_only':'bool',
            'retrieve_all_trains':'bool',
            'trains':'list[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    CachingProgress_ = typing.TypedDict('CachingProgress_', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry = typing.TypedDict('CatalogEntry', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress_',
            'caching_job':'dict[str]',
    })
    CachingProgress__ = typing.TypedDict('CachingProgress__', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry_ = typing.TypedDict('CatalogEntry_', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress__',
            'caching_job':'dict[str]',
    })
    CachingProgress___ = typing.TypedDict('CachingProgress___', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry__ = typing.TypedDict('CatalogEntry__', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress___',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
    })
    CachingProgress____ = typing.TypedDict('CachingProgress____', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogUpdateReturns = typing.TypedDict('CatalogUpdateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress____',
            'caching_job':'dict[str]',
    })
    @typing.overload
    def validate(self, 
        label:'str',
    /) -> None: 
        """
        Validates `label` catalog format which includes validating trains and applications with their versions.
        
        This does not test if an app version is valid in terms of kubernetes resources but instead ensures it has
        the correct format and files necessary for TrueNAS to use it.

        Parameters
        ----------
        label:
            Validates `label` catalog format which includes validating trains and applications with their versions.
        Returns
        -------
        """
        ...
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
    })
    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreateReturns = typing.TypedDict('CatalogCreateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
    })
    ItemDetails = typing.TypedDict('ItemDetails', {
            'name':'str',
            'categories':'list[str]',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'app_readme':'typing.Optional[str]',
            'location':'str',
            'healthy':'bool',
            'recommended':'bool',
            'healthy_error':'typing.Optional[str]',
            'versions':'dict[str]',
            'latest_version':'typing.Optional[str]',
            'latest_app_version':'typing.Optional[str]',
            'latest_human_version':'typing.Optional[str]',
            'last_update':'typing.Optional[str]',
            'icon_url':'typing.Optional[str]',
            'home':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'bool',
            'cache_only':'bool',
            'retrieve_all_trains':'bool',
            'trains':'list[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    CachingProgress_ = typing.TypedDict('CachingProgress_', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry = typing.TypedDict('CatalogEntry', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress_',
            'caching_job':'dict[str]',
    })
    CachingProgress__ = typing.TypedDict('CachingProgress__', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry_ = typing.TypedDict('CatalogEntry_', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress__',
            'caching_job':'dict[str]',
    })
    CachingProgress___ = typing.TypedDict('CachingProgress___', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogEntry__ = typing.TypedDict('CatalogEntry__', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress___',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
    })
    CachingProgress____ = typing.TypedDict('CachingProgress____', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogUpdateReturns = typing.TypedDict('CatalogUpdateReturns', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'location':'str',
            'id':'str',
            'preferred_trains':'list',
            'trains':'dict[str]',
            'healthy':'bool',
            'error':'bool',
            'builtin':'bool',
            'cached':'bool',
            'caching_progress':'CachingProgress____',
            'caching_job':'dict[str]',
    })

