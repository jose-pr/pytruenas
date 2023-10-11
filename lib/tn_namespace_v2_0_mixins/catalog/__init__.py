
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Catalog(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'catalog')

    CachingProgress = typing.TypedDict('CachingProgress', {
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
            'percent':'typing.Optional[float]',
    })
    CatalogCreate = typing.TypedDict('CatalogCreate', {
            'label':'str',
            'repository':'str',
            'branch':'str',
            'preferred_trains':'list',
            'force':'bool',
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
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
    })
    CatalogUpdate = typing.TypedDict('CatalogUpdate', {
            'preferred_trains':'list',
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
            'caching_progress':'CachingProgress',
            'caching_job':'dict[str]',
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
    ItemVersionDetails = typing.TypedDict('ItemVersionDetails', {
            'cache':'bool',
            'catalog':'str',
            'train':'str',
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
