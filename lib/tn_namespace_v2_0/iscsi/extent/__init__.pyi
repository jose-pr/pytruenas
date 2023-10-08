
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class IscsiExtent(Namespace):
    _namespace:_ty.Literal['iscsi.extent']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        iscsi_extent_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create an iSCSI Extent.
        
        When `type` is set to FILE, attribute `filesize` is used and it represents number of bytes. `filesize` if
        not zero should be a multiple of `blocksize`. `path` is a required attribute with `type` set as FILE.
        
        With `type` being set to DISK, a valid ZFS volume is required.
        
        `insecure_tpc` when enabled allows an initiator to bypass normal access control and access any scannable
        target. This allows xcopy operations otherwise blocked by access control.
        
        `xen` is a boolean value which is set to true if Xen is being used as the iSCSI initiator.
        
        `ro` when set to true prevents the initiator from writing to this LUN.

        Parameters
        ----------
        iscsi_extent_create:
            iscsi_extent_create
        Returns
        -------
        dict[str]:
            iscsi_extent_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
        remove:'bool'=False,
        force:'bool'=False,
    /) -> 'bool': 
        """
        Delete iSCSI Extent of `id`.
        
        If `id` iSCSI Extent's `type` was configured to FILE, `remove` can be set to remove the configured file.

        Parameters
        ----------
        id:
            Delete iSCSI Extent of `id`.
        remove:
            remove
        force:
            force
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @_ty.overload
    def disk_choices(self, 
    /) -> None: 
        """
        Return a dict of available zvols that can be used
        when creating an extent.

        Parameters
        ----------
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
        iscsi_extent_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update iSCSI Extent of `id`.

        Parameters
        ----------
        id:
            Update iSCSI Extent of `id`.
            Create an iSCSI Extent.
        iscsi_extent_update:
            iscsi_extent_update
        Returns
        -------
        dict[str]:
            iscsi_extent_update_returns
        """
        ...
