
from pytruenas import Namespace, TrueNASClient
import typing
class Tunable(Namespace):
    _namespace:typing.Literal['tunable']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        tunable_create:'TunableCreate'={},
    /) -> 'TunableCreateReturns': 
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
        TunableCreateReturns:
            tunable_create_returns
        """
        ...
    @typing.overload
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
    @typing.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'QueryOptionsGetInstance'={},
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
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[TunableEntry]|TunableEntry|int|TunableEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[TunableEntry]:
            
        TunableEntry:
            
        int:
            
        TunableEntry:
            
        """
        ...
    @typing.overload
    def tunable_type_choices(self, 
    /) -> 'TunableTypeChoices': 
        """
        Retrieve the supported tunable types that can be changed.

        Parameters
        ----------
        Returns
        -------
        TunableTypeChoices:
            tunable_type_choices
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        tunable_update:'TunableUpdate'={},
    /) -> 'TunableUpdateReturns': 
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
        TunableUpdateReturns:
            tunable_update_returns
        """
        ...

class TunableCreate(typing.TypedDict):
        type:'str'
        var:'str'
        value:'str'
        comment:'str'
        enabled:'bool'
        update_initramfs:'bool'
        ...
class TunableCreateReturns(typing.TypedDict):
        type:'str'
        var:'str'
        value:'str'
        comment:'str'
        enabled:'bool'
        update_initramfs:'bool'
        id:'int'
        ...
class QueryOptionsGetInstance(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class TunableEntry(typing.TypedDict):
        type:'str'
        var:'str'
        value:'str'
        comment:'str'
        enabled:'bool'
        update_initramfs:'bool'
        id:'int'
        ...
class TunableTypeChoices(typing.TypedDict):
        SYSCTL:'str'
        UDEV:'str'
        ZFS:'str'
        ...
class TunableUpdate(typing.TypedDict):
        value:'str'
        comment:'str'
        enabled:'bool'
        update_initramfs:'bool'
        ...
class TunableUpdateReturns(typing.TypedDict):
        type:'str'
        var:'str'
        value:'str'
        comment:'str'
        enabled:'bool'
        update_initramfs:'bool'
        id:'int'
        ...