
from pytruenas import Namespace, TrueNASClient
import typing
class Dns(Namespace):
    _namespace:typing.Literal['dns']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'int|Nameserver|list[Nameserver]': 
        """
        Query Name Servers with `query-filters` and `query-options`.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        int:
            
        Nameserver:
            
        list[Nameserver]:
            
        """
        ...

class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class Nameserver(typing.TypedDict):
        nameserver:'str'
        ...
