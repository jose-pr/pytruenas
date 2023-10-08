
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class PoolResilver(Namespace):
    _namespace:_ty.Literal['pool.resilver']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            pool_resilver_entry
        """
        ...
    @_ty.overload
    def update(self, 
        pool_resilver_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            pool_resilver_update_returns
        """
        ...
