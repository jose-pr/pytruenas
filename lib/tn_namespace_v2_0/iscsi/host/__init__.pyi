
from pytruenas import Namespace, TrueNASClient
import typing
class IscsiHost(Namespace):
    _namespace:typing.Literal['iscsi.host']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        iscsi_host_create:'IscsiHostCreate'={},
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
        id:'int',
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
        id:'int',
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
    def get_targets(self, 
        id:'int',
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
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[dict[str]]|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[dict[str]]:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @typing.overload
    def set_initiators(self, 
        id:'int',
        ids:'list[int]'=[],
        force:'bool'=False,
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
        id:'int',
        ids:'list[int]'=[],
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
        id:'int',
        iscsi_host_update:'IscsiHostUpdate'={},
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

class IscsiHostCreate(typing.TypedDict):
        ip:'str'
        description:'str'
        iqns:'list[str]'
        added_automatically:'bool'
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
class IscsiHostUpdate(typing.TypedDict):
        ip:'str'
        description:'str'
        iqns:'list[str]'
        added_automatically:'bool'
        ...
