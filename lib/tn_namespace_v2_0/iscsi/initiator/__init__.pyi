
from pytruenas import Namespace, TrueNASClient
import typing
class IscsiInitiator(Namespace):
    _namespace:typing.Literal['iscsi.initiator']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        iscsi_initiator_create:'IscsiInitiatorCreate'={},
    /) -> 'dict[str]': 
        """
        Create an iSCSI Initiator.
        
        `initiators` is a list of initiator hostnames which are authorized to access an iSCSI Target. To allow all
        possible initiators, `initiators` can be left empty.

        Parameters
        ----------
        iscsi_initiator_create:
            iscsi_initiator_create
        Returns
        -------
        dict[str]:
            iscsi_initiator_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete iSCSI initiator of `id`.

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
    def update(self, 
        id:'int',
        iscsi_initiator_update:'IscsiInitiatorUpdate'={},
    /) -> 'dict[str]': 
        """
        Update iSCSI initiator of `id`.

        Parameters
        ----------
        id:
            Update iSCSI initiator of `id`.
            Create an iSCSI Initiator.
        iscsi_initiator_update:
            iscsi_initiator_update
        Returns
        -------
        dict[str]:
            iscsi_initiator_update_returns
        """
        ...

class IscsiInitiatorCreate(typing.TypedDict):
        initiators:'list'
        comment:'str'
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
class IscsiInitiatorUpdate(typing.TypedDict):
        initiators:'list'
        comment:'str'
        ...
