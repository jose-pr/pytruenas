
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class ClusterUtils(Namespace):
    _namespace:_ty.Literal['cluster.utils']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
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
