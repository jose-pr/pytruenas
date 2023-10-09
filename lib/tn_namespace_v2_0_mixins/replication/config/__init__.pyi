
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin
from enum import Enum
import typing
class ReplicationConfig(
    ConfigMixin,
    Namespace
    ):
    _namespace:typing.Literal['replication.config']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
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
    @typing.overload
    def update(self, 
        replication_config_update:'ReplicationConfigUpdate'={},
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
    ReplicationConfigUpdate = typing.TypedDict('ReplicationConfigUpdate', {
            'max_parallel_replication_tasks':'typing.Optional[int]',
    })
