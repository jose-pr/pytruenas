
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Catalog(Namespace):
    _namespace:_ty.Literal['catalog']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        catalog_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        `catalog_create.preferred_trains` specifies trains which will be displayed in the UI directly for a user.

        Parameters
        ----------
        catalog_create:
            catalog_create
        Returns
        -------
        dict[str]:
            catalog_create_returns
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
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
    @_ty.overload
    def get_item_details(self, 
        item_name:'str',
        item_version_details:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            item_details
        """
        ...
    @_ty.overload
    def items(self, 
        label:'str',
        options:'dict[str]'={},
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def update(self, 
        id:'str',
        catalog_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        id:
            id
        catalog_update:
            catalog_update
        Returns
        -------
        dict[str]:
            catalog_update_returns
        """
        ...
    @_ty.overload
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
