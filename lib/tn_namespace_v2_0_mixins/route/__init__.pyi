
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Route(
    Namespace
    ):
    _namespace:typing.Literal['route']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
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
    @typing.overload
    def system_routes(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[int, SystemRoute, list[SystemRoute_]]': 
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
        typing.Union[int, SystemRoute, list[SystemRoute_]]:
            
        """
        ...
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    SystemRoute = typing.TypedDict('SystemRoute', {
            'network':'str',
            'netmask':'str',
            'gateway':'typing.Optional[str]',
            'interface':'str',
            'flags':'list',
            'table_id':'int',
            'scope':'int',
            'preferred_source':'typing.Optional[str]',
    })
    SystemRoute_ = typing.TypedDict('SystemRoute_', {
            'network':'str',
            'netmask':'str',
            'gateway':'typing.Optional[str]',
            'interface':'str',
            'flags':'list',
            'table_id':'int',
            'scope':'int',
            'preferred_source':'typing.Optional[str]',
    })
