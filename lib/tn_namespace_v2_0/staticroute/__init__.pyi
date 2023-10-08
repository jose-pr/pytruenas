
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Staticroute(Namespace):
    _namespace:_ty.Literal['staticroute']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        staticroute_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a Static Route.
        
        Address families of `gateway` and `destination` should match when creating a static route.
        
        `description` is an optional attribute for any notes regarding the static route.

        Parameters
        ----------
        staticroute_create:
            staticroute_create
        Returns
        -------
        dict[str]:
            staticroute_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete Static Route of `id`.

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
        staticroute_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update Static Route of `id`.

        Parameters
        ----------
        id:
            Update Static Route of `id`.
            Create a Static Route.
        staticroute_update:
            staticroute_update
        Returns
        -------
        dict[str]:
            staticroute_update_returns
        """
        ...
