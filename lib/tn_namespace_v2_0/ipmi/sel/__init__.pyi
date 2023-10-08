
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class IpmiSel(Namespace):
    _namespace:_ty.Literal['ipmi.sel']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def clear(self, 
    /) -> None: 
        """
        

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def elist(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
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
        int:
            
        dict[str]:
            
        list:
            
        """
        ...
    @_ty.overload
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
