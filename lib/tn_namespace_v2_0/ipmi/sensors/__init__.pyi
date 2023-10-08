
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class IpmiSensors(Namespace):
    _namespace:_ty.Literal['ipmi.sensors']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|list|list': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        int:
            
        list:
            
        list:
            
        """
        ...
