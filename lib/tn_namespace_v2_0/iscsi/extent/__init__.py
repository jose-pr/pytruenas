
from pytruenas.base import Namespace

import typing
from enum import Enum

class IscsiExtent(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.extent')

    class Type(str,Enum):
        DISK = 'DISK'
        FILE = 'FILE'
        ...
    class Rpm(str,Enum):
        UNKNOWN = 'UNKNOWN'
        SSD = 'SSD'
        _5400 = '5400'
        _7200 = '7200'
        _10000 = '10000'
        _15000 = '15000'
        ...
    IscsiExtentCreate = typing.TypedDict('IscsiExtentCreate', {
            'name':'str',
            'type':'Type',
            'disk':'typing.Optional[str]',
            'serial':'typing.Optional[str]',
            'path':'typing.Optional[str]',
            'filesize':'int',
            'blocksize':'int',
            'pblocksize':'bool',
            'avail_threshold':'typing.Optional[int]',
            'comment':'str',
            'insecure_tpc':'bool',
            'xen':'bool',
            'rpm':'Rpm',
            'ro':'bool',
            'enabled':'bool',
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
    IscsiExtentUpdate = typing.TypedDict('IscsiExtentUpdate', {
            'name':'str',
            'type':'Type',
            'disk':'typing.Optional[str]',
            'serial':'typing.Optional[str]',
            'path':'typing.Optional[str]',
            'filesize':'int',
            'blocksize':'int',
            'pblocksize':'bool',
            'avail_threshold':'typing.Optional[int]',
            'comment':'str',
            'insecure_tpc':'bool',
            'xen':'bool',
            'rpm':'Rpm',
            'ro':'bool',
            'enabled':'bool',
    })
