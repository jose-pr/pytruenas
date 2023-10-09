
from pytruenas import TrueNASClient
from pytruenas.base import Namespace

import typing
class NetworkGeneral(
    Namespace
    ):
    _namespace:typing.Literal['network.general']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def summary(self, 
    /) -> 'NetworkSummary': 
        """
        Retrieve general information for current Network.
        
        Returns a dictionary. For example:

        Parameters
        ----------
        Returns
        -------
        NetworkSummary:
            network_summary
        """
        ...
    NetworkSummary = typing.TypedDict('NetworkSummary', {
            'ips':'dict[str]',
            'default_routes':'list[str]',
            'nameservers':'list[str]',
    })

