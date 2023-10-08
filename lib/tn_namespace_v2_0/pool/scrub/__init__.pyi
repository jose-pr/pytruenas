
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class PoolScrub(Namespace):
    _namespace:_ty.Literal['pool.scrub']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        pool_scrub_entry:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a scrub task for a pool.
        
        `threshold` refers to the minimum amount of time in days has to be passed before
        a scrub can run again.

        Parameters
        ----------
        pool_scrub_entry:
            pool_scrub_entry
        Returns
        -------
        dict[str]:
            pool_scrub_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete scrub task of `id`.

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
    def run(self, 
        name:'str',
        threshold:'int'=35,
    /) -> None: 
        """
        Initiate a scrub of a pool `name` if last scrub was performed more than `threshold` days before.

        Parameters
        ----------
        name:
            name
        threshold:
            threshold
        Returns
        -------
        """
        ...
    @_ty.overload
    def scrub(self, 
        name:'str',
        action:'str'="START",
    /) -> None: 
        """
        Start/Stop/Pause a scrub on pool `name`.

        Parameters
        ----------
        name:
            name
        action:
            action
        Returns
        -------
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        pool_scrub_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update scrub task of `id`.

        Parameters
        ----------
        id:
            Update scrub task of `id`.
            Create a scrub task for a pool.
        pool_scrub_update:
            pool_scrub_update
        Returns
        -------
        dict[str]:
            pool_scrub_update_returns
        """
        ...
