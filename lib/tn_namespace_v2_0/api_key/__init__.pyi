
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Api_key(Namespace):
    _namespace:_ty.Literal['api_key']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        api_key_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Creates API Key.
        
        `name` is a user-readable name for key.

        Parameters
        ----------
        api_key_create:
            api_key_create
        Returns
        -------
        dict[str]:
            api_key_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete API Key `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
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
    def update(self, 
        id:'int',
        api_key_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update API Key `id`.
        
        Specify `reset: true` to reset this API Key.

        Parameters
        ----------
        id:
            Update API Key `id`.
        api_key_update:
            api_key_update
        Returns
        -------
        dict[str]:
            api_key_update_returns
        """
        ...
