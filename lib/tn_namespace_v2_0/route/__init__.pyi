
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Route(Namespace):
    _namespace:_ty.Literal['route']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def ipv4gw_reachable(self, 
        ipv4_gateway:'str',
    /) -> 'bool': 
        """
        Get the IPv4 gateway and verify if it is reachable by any interface.
        
        Returns:
            bool: True if the gateway is reachable or otherwise False.

        Parameters
        ----------
        ipv4_gateway:
            ipv4_gateway
        Returns
        -------
        bool:
            ipv4gw_reachable
        """
        ...
    @_ty.overload
    def system_routes(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
        """
        Get current/applied network routes.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        int:
            
        dict[str]:
            
        list:
            
        """
        ...
