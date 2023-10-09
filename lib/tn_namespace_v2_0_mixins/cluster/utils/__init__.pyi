
from pytruenas import TrueNASClient
from pytruenas.base import Namespace

import typing
class ClusterUtils(
    Namespace
    ):
    _namespace:typing.Literal['cluster.utils']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def is_clustered(self, 
    /) -> 'bool': 
        """
        Returns a boolean value on whether this system is clustered.
        `True` means this system is clustered
        `False` means this system is not clustered.

        Parameters
        ----------
        Returns
        -------
        bool:
            is_clustered
        """
        ...

