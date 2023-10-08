
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class IscsiPortal(Namespace):
    _namespace:_ty.Literal['iscsi.portal']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        iscsiportal_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a new iSCSI Portal.
        
        `discovery_authgroup` is required for CHAP and CHAP_MUTUAL.

        Parameters
        ----------
        iscsiportal_create:
            iscsiportal_create
        Returns
        -------
        dict[str]:
            iscsi_portal_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete iSCSI Portal `id`.

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
    def listen_ip_choices(self, 
    /) -> None: 
        """
        Returns possible choices for `listen.ip` attribute of portal create and update.

        Parameters
        ----------
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
        iscsiportal_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update iSCSI Portal `id`.

        Parameters
        ----------
        id:
            Update iSCSI Portal `id`.
            Create a new iSCSI Portal.
        iscsiportal_update:
            iscsiportal_update
        Returns
        -------
        dict[str]:
            iscsi_portal_update_returns
        """
        ...
