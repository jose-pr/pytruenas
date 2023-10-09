
from pytruenas.base import Namespace

import typing
from enum import Enum

class PoolDatasetUserprop(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.dataset.userprop')

    Property = typing.TypedDict('Property', {
            'name':'str',
            'value':'str',
    })
    DatasetUserPropCreate = typing.TypedDict('DatasetUserPropCreate', {
            'id':'str',
            'property':'Property',
    })
    PoolDatasetUserpropCreateReturns = typing.TypedDict('PoolDatasetUserpropCreateReturns', {
            'id':'str',
            'properties':'dict[str]',
    })
    DatasetUserPropDelete = typing.TypedDict('DatasetUserPropDelete', {
            'name':'str',
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
    PoolDatasetUserpropEntry = typing.TypedDict('PoolDatasetUserpropEntry', {
            'id':'str',
            'properties':'dict[str]',
    })
    DatasetUserPropUpdate = typing.TypedDict('DatasetUserPropUpdate', {
            'name':'str',
            'value':'str',
    })
    PoolDatasetUserpropUpdateReturns = typing.TypedDict('PoolDatasetUserpropUpdateReturns', {
            'id':'str',
            'properties':'dict[str]',
    })
