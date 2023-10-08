
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Tunable(Namespace):
    _namespace:_ty.Literal['tunable']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        tunable_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a tunable.
        
        If `type` is `SYSCTL` then `var` is a sysctl name (e.g. `kernel.watchdog`) and `value` is its corresponding
        value (e.g. `0`).
        
        If `type` is `UDEV` then `var` is an udev rules file name (e.g. `10-disable-usb`, `.rules` suffix will be
        appended automatically) and `value` is its contents (e.g. `BUS=="usb", OPTIONS+="ignore_device"`).
        
        If `type` is `ZFS` then `var` is a ZFS kernel module parameter name (e.g. `zfs_dirty_data_max_max`) and `value`
        is its value (e.g. `783091712`).
        
        If `update_initramfs` is `false` then initramfs will not be updated after creating a ZFS tunable and you will
        need to run `system boot update_initramfs` manually.

        Parameters
        ----------
        tunable_create:
            tunable_create
        Returns
        -------
        dict[str]:
            tunable_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete Tunable of `id`.

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
    def tunable_type_choices(self, 
    /) -> 'dict[str]': 
        """
        Retrieve the supported tunable types that can be changed.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            tunable_type_choices
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        tunable_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update Tunable of `id`.

        Parameters
        ----------
        id:
            Update Tunable of `id`.
            Create a tunable.
        tunable_update:
            tunable_update
        Returns
        -------
        dict[str]:
            tunable_update_returns
        """
        ...
