
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class IpmiSensors(
    Namespace
    ):
    _namespace:typing.Literal['ipmi.sensors']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[int, list[dict[str]], list[list[dict[str]]]]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[int, list[dict[str]], list[list[dict[str]]]]:
            
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
