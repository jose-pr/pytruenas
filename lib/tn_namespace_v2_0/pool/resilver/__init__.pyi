
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class PoolResilver(
    Namespace
    ):
    _namespace:typing.Literal['pool.resilver']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'PoolResilverEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        PoolResilverEntry:
            pool_resilver_entry
        """
        ...
    @typing.overload
    def update(self, 
        _pool_resilver_update:'PoolResilverUpdate',
    /) -> 'PoolResilverUpdateReturns': 
        """
        Configure Pool Resilver Priority.
        
        If `begin` time is greater than `end` time it means it will rollover the day, e.g.
        begin = "19:00", end = "05:00" will increase pool resilver priority from 19:00 of one day
        until 05:00 of the next day.
        
        `weekday` follows crontab(5) values 0-7 (0 or 7 is Sun).

        Parameters
        ----------
        pool_resilver_update:
            pool_resilver_update
        Returns
        -------
        PoolResilverUpdateReturns:
            pool_resilver_update_returns
        """
        ...
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
