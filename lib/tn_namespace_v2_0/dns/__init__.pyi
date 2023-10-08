
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Dns(Namespace):
    _namespace:_ty.Literal['dns']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
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
            
        dict[str]:
            
        list:
            
        """
        ...
