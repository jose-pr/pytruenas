
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class Tunable(
    TableExtMixin,
    Namespace
    ):
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
        id:'typing.Union[str, int, bool, dict[str], list]',
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
    /) -> 'typing.Union[list[TunableEntry], TunableEntry, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[TunableEntry], TunableEntry, int]:
            
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
    class Type(str,Enum):
        SYSCTL = 'SYSCTL'
        UDEV = 'UDEV'
        ZFS = 'ZFS'
        ...
    TunableCreate = typing.TypedDict('TunableCreate', {
            'type':'Type',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
    })
    TunableCreateReturns = typing.TypedDict('TunableCreateReturns', {
            'type':'Type',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
            'id':'int',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    TunableEntry = typing.TypedDict('TunableEntry', {
            'type':'Type',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
            'id':'int',
    })
    class SYSCTL(str,Enum):
        SYSCTL = 'SYSCTL'
        ...
    class UDEV(str,Enum):
        UDEV = 'UDEV'
        ...
    class ZFS(str,Enum):
        ZFS = 'ZFS'
        ...
    TunableTypeChoices = typing.TypedDict('TunableTypeChoices', {
            'SYSCTL':'SYSCTL',
            'UDEV':'UDEV',
            'ZFS':'ZFS',
    })
    TunableUpdate = typing.TypedDict('TunableUpdate', {
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
    })
    TunableUpdateReturns = typing.TypedDict('TunableUpdateReturns', {
            'type':'Type',
            'var':'str',
            'value':'str',
            'comment':'str',
            'enabled':'bool',
            'update_initramfs':'bool',
            'id':'int',
    })
