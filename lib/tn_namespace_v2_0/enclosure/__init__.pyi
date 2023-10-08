
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Enclosure(Namespace):
    _namespace:_ty.Literal['enclosure']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def set_slot_status(self, 
        enclosure_id:'str',
        slot:'int',
        status:'str',
    /) -> None: 
        """
        

        Parameters
        ----------
        enclosure_id:
            enclosure_id
        slot:
            slot
        status:
            status
        Returns
        -------
        """
        ...
    @_ty.overload
    def update(self, 
        id:'str',
        enclosure_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        id:
            id
        enclosure_update:
            enclosure_update
        Returns
        -------
        dict[str]:
            enclosure_update_returns
        """
        ...
