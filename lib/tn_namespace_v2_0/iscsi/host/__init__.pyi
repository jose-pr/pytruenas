
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class IscsiHost(
    Namespace
    ):
    _namespace:typing.Literal['iscsi.host']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        _iscsi_host_create:'IscsiHostCreate',
    /) -> 'dict[str]': 
        """
        Creates iSCSI host.
        
        `ip` indicates an IP address of the host.
        `description` is a human-readable name for the host.
        `iqns` is a list of initiator iSCSI Qualified Names.

        Parameters
        ----------
        iscsi_host_create:
            iscsi_host_create
        Returns
        -------
        dict[str]:
            iscsi_host_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        _id:'int',
    /) -> 'bool': 
        """
        Update iSCSI host `id`.

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
    def get_initiators(self, 
        _id:'int',
    /) -> None: 
        """
        Returns initiator groups associated with host `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @typing.overload
    def get_instance(self, 
        _id:'typing.Union[str, int, bool, dict[str], list]',
        _query_options_get_instance:'QueryOptionsGetInstance',
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
    def get_targets(self, 
        _id:'int',
    /) -> None: 
        """
        Returns targets associated with host `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @typing.overload
    def query(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list, dict[str], int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list, dict[str], int]:
            
        """
        ...
    @typing.overload
    def set_initiators(self, 
        _id:'int',
        _ids:'list[int]',
        _force:'bool',
    /) -> None: 
        """
        Associates initiator groups `ids` with host `id`.
        Use `force` if you want to allow adding first or removing last initiator from initiator groups.

        Parameters
        ----------
        id:
            Associates initiator groups `ids` with host `id`.
        ids:
            Associates initiator groups `ids` with host `id`.
        force:
            force
        Returns
        -------
        """
        ...
    @typing.overload
    def set_targets(self, 
        _id:'int',
        _ids:'list[int]',
    /) -> None: 
        """
        Associates targets `ids` with host `id`.

        Parameters
        ----------
        id:
            id
        ids:
            ids
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        _id:'int',
        _iscsi_host_update:'IscsiHostUpdate',
    /) -> 'dict[str]': 
        """
        Update iSCSI host `id`.

        Parameters
        ----------
        id:
            Update iSCSI host `id`.
            Creates iSCSI host.
        iscsi_host_update:
            iscsi_host_update
        Returns
        -------
        dict[str]:
            iscsi_host_update_returns
        """
        ...
    IscsiHostCreate = typing.TypedDict('IscsiHostCreate', {
            'ip':'str',
            'description':'str',
            'iqns':'list[str]',
            'added_automatically':'bool',
    })
    IscsiHostUpdate = typing.TypedDict('IscsiHostUpdate', {
            'ip':'str',
            'description':'str',
            'iqns':'list[str]',
            'added_automatically':'bool',
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
