
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class App(
    Namespace
    ):
    _namespace:typing.Literal['app']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def available(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[int, AvailableApps, list[AvailableApps_]]': 
        """
        Retrieve all available applications from all configured catalogs.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[int, AvailableApps, list[AvailableApps_]]:
            
        """
        ...
    @typing.overload
    def categories(self, 
    /) -> 'list[str]': 
        """
        Retrieve list of valid categories which have associated applications.

        Parameters
        ----------
        Returns
        -------
        list[str]:
            categories
        """
        ...
    @typing.overload
    def latest(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions_'={},
    /) -> 'typing.Union[int, AvailableApps__, list[AvailableApps___]]': 
        """
        Retrieve latest updated apps.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[int, AvailableApps__, list[AvailableApps___]]:
            
        """
        ...
    @typing.overload
    def similar(self, 
        app_name:'str',
        catalog:'str',
        train:'str',
    /) -> 'list[AvailableApps____]': 
        """
        Retrieve applications which are similar to `app_name`.

        Parameters
        ----------
        app_name:
            app_name
        catalog:
            catalog
        train:
            train
        Returns
        -------
        list[AvailableApps____]:
            similar
        """
        ...
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
    AvailableApps = typing.TypedDict('AvailableApps', {
            'healthy':'bool',
            'installed':'bool',
            'categories':'list',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'name':'str',
            'title':'str',
            'description':'str',
            'app_readme':'str',
            'location':'str',
            'healthy_error':'typing.Optional[str]',
            'home':'str',
            'last_update':'str',
            'latest_version':'str',
            'latest_app_version':'str',
            'icon_url':'str',
            'train':'str',
            'catalog':'str',
    })
    AvailableApps_ = typing.TypedDict('AvailableApps_', {
            'healthy':'bool',
            'installed':'bool',
            'categories':'list',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'name':'str',
            'title':'str',
            'description':'str',
            'app_readme':'str',
            'location':'str',
            'healthy_error':'typing.Optional[str]',
            'home':'str',
            'last_update':'str',
            'latest_version':'str',
            'latest_app_version':'str',
            'icon_url':'str',
            'train':'str',
            'catalog':'str',
    })
    QueryOptions_ = typing.TypedDict('QueryOptions_', {
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
    AvailableApps__ = typing.TypedDict('AvailableApps__', {
            'healthy':'bool',
            'installed':'bool',
            'categories':'list',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'name':'str',
            'title':'str',
            'description':'str',
            'app_readme':'str',
            'location':'str',
            'healthy_error':'typing.Optional[str]',
            'home':'str',
            'last_update':'str',
            'latest_version':'str',
            'latest_app_version':'str',
            'icon_url':'str',
            'train':'str',
            'catalog':'str',
    })
    AvailableApps___ = typing.TypedDict('AvailableApps___', {
            'healthy':'bool',
            'installed':'bool',
            'categories':'list',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'name':'str',
            'title':'str',
            'description':'str',
            'app_readme':'str',
            'location':'str',
            'healthy_error':'typing.Optional[str]',
            'home':'str',
            'last_update':'str',
            'latest_version':'str',
            'latest_app_version':'str',
            'icon_url':'str',
            'train':'str',
            'catalog':'str',
    })
    AvailableApps____ = typing.TypedDict('AvailableApps____', {
            'healthy':'bool',
            'installed':'bool',
            'categories':'list',
            'maintainers':'list',
            'tags':'list',
            'screenshots':'list[str]',
            'sources':'list[str]',
            'name':'str',
            'title':'str',
            'description':'str',
            'app_readme':'str',
            'location':'str',
            'healthy_error':'typing.Optional[str]',
            'home':'str',
            'last_update':'str',
            'latest_version':'str',
            'latest_app_version':'str',
            'icon_url':'str',
            'train':'str',
            'catalog':'str',
    })
