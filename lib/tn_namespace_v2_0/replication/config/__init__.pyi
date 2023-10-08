
from pytruenas import Namespace, TrueNASClient
import typing
class ReplicationConfig(Namespace):
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

class ReplicationConfigUpdate(typing.TypedDict):
        max_parallel_replication_tasks:'typing.Optional[int]'
        ...
