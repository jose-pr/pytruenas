
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class IscsiTargetextent(Namespace):
    _namespace:_ty.Literal['iscsi.targetextent']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        iscsi_targetextent_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create an Associated Target.
        
        `lunid` will be automatically assigned if it is not provided based on the `target`.

        Parameters
        ----------
        iscsi_targetextent_create:
            iscsi_targetextent_create
        Returns
        -------
        dict[str]:
            iscsi_targetextent_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
        force:'bool'=False,
    /) -> 'bool': 
        """
        Delete Associated Target of `id`.

        Parameters
        ----------
        id:
            id
        force:
            force
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
        iscsi_targetextent_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update Associated Target of `id`.

        Parameters
        ----------
        id:
            Update Associated Target of `id`.
            Create an Associated Target.
        iscsi_targetextent_update:
            iscsi_targetextent_update
        Returns
        -------
        dict[str]:
            iscsi_targetextent_update_returns
        """
        ...
