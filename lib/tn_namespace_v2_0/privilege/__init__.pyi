
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Privilege(Namespace):
    _namespace:_ty.Literal['privilege']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        privilege_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Creates a privilege.
        
        `name` is a name for privilege (must be unique).
        
        `local_groups` is a list of local user account group GIDs that gain this privilege.
        
        `ds_groups` is list of Directory Service group GIDs that will gain this privilege.
        
        `allowlist` is a list of API endpoints allowed for this privilege.
        
        `web_shell` controls whether users with this privilege are allowed to log in to the Web UI.

        Parameters
        ----------
        privilege_create:
            privilege_create
        Returns
        -------
        dict[str]:
            privilege_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete the privilege `id`.

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
        privilege_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update the privilege `id`.

        Parameters
        ----------
        id:
            Update the privilege `id`.
            Creates a privilege.
        privilege_update:
            privilege_update
        Returns
        -------
        dict[str]:
            privilege_update_returns
        """
        ...
