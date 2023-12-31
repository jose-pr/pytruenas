
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class IpmiSel(
    Namespace
    ):
    _namespace:typing.Literal['ipmi.sel']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def clear(self, 
    /) -> None: 
        """
        

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def elist(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[int, dict[str], list]': 
        """
        Query IPMI System Event Log (SEL) extended list

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[int, dict[str], list]:
            
        """
        ...
    @typing.overload
    def info(self, 
    /) -> 'dict[str]': 
        """
        Query General information about the IPMI System Event Log

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            ipmi_sel_info
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
