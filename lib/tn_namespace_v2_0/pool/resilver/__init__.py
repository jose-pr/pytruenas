
from pytruenas.base import Namespace

import typing
class PoolResilver(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.resilver')

    PoolResilverEntry = typing.TypedDict('PoolResilverEntry', {
            'id':'int',
            'begin':'str',
            'end':'str',
            'enabled':'bool',
            'weekday':'list[int]',
    })
    PoolResilverUpdate = typing.TypedDict('PoolResilverUpdate', {
            'begin':'str',
            'end':'str',
            'enabled':'bool',
            'weekday':'list[int]',
    })
    PoolResilverUpdateReturns = typing.TypedDict('PoolResilverUpdateReturns', {
            'id':'int',
            'begin':'str',
            'end':'str',
            'enabled':'bool',
            'weekday':'list[int]',
    })
