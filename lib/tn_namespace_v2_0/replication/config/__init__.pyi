
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class ReplicationConfig(Namespace):
    _namespace:_ty.Literal['replication.config']
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
            replication_config_entry
        """
        ...
    @_ty.overload
    def update(self, 
        replication_config_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        `max_parallel_replication_tasks` represents a maximum number of parallel replication tasks running.

        Parameters
        ----------
        replication_config_update:
            replication_config_update
        Returns
        -------
        dict[str]:
            replication_config_update_returns
        """
        ...
