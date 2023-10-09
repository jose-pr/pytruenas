
from pytruenas.base import Namespace

import typing
from enum import Enum

class Vmware(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'vmware')

    VmwareCreate = typing.TypedDict('VmwareCreate', {
            'datastore':'str',
            'filesystem':'str',
            'hostname':'str',
            'password':'str',
            'username':'str',
    })
    VmwareCreds = typing.TypedDict('VmwareCreds', {
            'hostname':'str',
            'username':'str',
            'password':'str',
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
    VmwareUpdate = typing.TypedDict('VmwareUpdate', {
            'datastore':'str',
            'filesystem':'str',
            'hostname':'str',
            'password':'str',
            'username':'str',
    })
