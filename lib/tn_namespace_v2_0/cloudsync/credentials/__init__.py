
from pytruenas.base import Namespace

import typing
from enum import Enum

class CloudsyncCredentials(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cloudsync.credentials')

    CloudSyncCredentialsCreate = typing.TypedDict('CloudSyncCredentialsCreate', {
            'name':'str',
            'provider':'str',
            'attributes':'dict[str]',
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
    CloudSyncCredentialsUpdate = typing.TypedDict('CloudSyncCredentialsUpdate', {
            'name':'str',
            'provider':'str',
            'attributes':'dict[str]',
    })
    CloudSyncCredentialsVerify = typing.TypedDict('CloudSyncCredentialsVerify', {
            'provider':'str',
            'attributes':'dict[str]',
    })
