
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class SharingNfs(Namespace):
    _namespace:_ty.Literal['sharing.nfs']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        sharingnfs_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a NFS Share.
        
        `path` local path to be exported.
        
        `aliases` IGNORED, for now.
        
        `networks` is a list of authorized networks that are allowed to access the share having format
        "network/mask" CIDR notation. If empty, all networks are allowed.
        
        `hosts` is a list of IP's/hostnames which are allowed to access the share. If empty, all IP's/hostnames are
        allowed.

        Parameters
        ----------
        sharingnfs_create:
            sharingnfs_create
        Returns
        -------
        dict[str]:
            sharing_nfs_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> None: 
        """
        Delete NFS Share of `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
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
        sharingnfs_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update NFS Share of `id`.

        Parameters
        ----------
        id:
            Update NFS Share of `id`.
            Create a NFS Share.
        sharingnfs_update:
            sharingnfs_update
        Returns
        -------
        dict[str]:
            sharing_nfs_update_returns
        """
        ...
