
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class IscsiAuth(Namespace):
    _namespace:_ty.Literal['iscsi.auth']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        iscsi_auth_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create an iSCSI Authorized Access.
        
        `tag` should be unique among all configured iSCSI Authorized Accesses.
        
        `secret` and `peersecret` should have length between 12-16 letters inclusive.
        
        `peeruser` and `peersecret` are provided only when configuring mutual CHAP. `peersecret` should not be
        similar to `secret`.

        Parameters
        ----------
        iscsi_auth_create:
            iscsi_auth_create
        Returns
        -------
        dict[str]:
            iscsi_auth_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete iSCSI Authorized Access of `id`.

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
        iscsi_auth_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update iSCSI Authorized Access of `id`.

        Parameters
        ----------
        id:
            Update iSCSI Authorized Access of `id`.
            Create an iSCSI Authorized Access.
        iscsi_auth_update:
            iscsi_auth_update
        Returns
        -------
        dict[str]:
            iscsi_auth_update_returns
        """
        ...
