
from pytruenas.base import Namespace

import typing
from enum import Enum

class Boot(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'boot')

    Options = typing.TypedDict('Options', {
            'expand':'bool',
    })
    Topology = typing.TypedDict('Topology', {
            'data':'list',
            'log':'list',
            'cache':'list',
            'spare':'list',
            'special':'list',
            'dedup':'list',
    })
    GetState = typing.TypedDict('GetState', {
            'name':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology',
    })
