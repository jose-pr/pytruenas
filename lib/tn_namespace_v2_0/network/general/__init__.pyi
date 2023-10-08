
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class NetworkGeneral(Namespace):
    _namespace:_ty.Literal['network.general']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def summary(self, 
    /) -> 'dict[str]': 
        """
        Retrieve general information for current Network.
        
        Returns a dictionary. For example:

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            network_summary
        """
        ...
