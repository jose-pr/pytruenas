
from pytruenas.base import Namespace

import typing
from enum import Enum

class App(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'app')

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
