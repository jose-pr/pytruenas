
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin
from enum import Enum
import typing
class IscsiGlobal_(
    ConfigMixin,
    Namespace
    ):
    _namespace:typing.Literal['iscsi.global']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def alua_enabled(self, 
    /) -> None: 
        """
        Returns whether iSCSI ALUA is enabled or not.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def client_count(self, 
    /) -> None: 
        """
        Return currently connected clients count.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            iscsi_global_entry
        """
        ...
    @typing.overload
    def sessions(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[int, Session, list[Session_]]': 
        """
        Get a list of currently running iSCSI sessions. This includes initiator and target names
        and the unique connection IDs.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[int, Session, list[Session_]]:
            
        """
        ...
    @typing.overload
    def update(self, 
        iscsiglobal_update:'IscsiglobalUpdate'={},
    /) -> 'dict[str]': 
        """
        `alua` is a no-op for FreeNAS.

        Parameters
        ----------
        iscsiglobal_update:
            iscsiglobal_update
        Returns
        -------
        dict[str]:
            iscsi_global_update_returns
        """
        ...
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
    Session = typing.TypedDict('Session', {
            'initiator':'str',
            'initiator_addr':'str',
            'initiator_alias':'typing.Optional[str]',
            'target':'str',
            'target_alias':'str',
            'header_digest':'typing.Optional[str]',
            'data_digest':'typing.Optional[str]',
            'max_data_segment_length':'typing.Optional[int]',
            'max_receive_data_segment_length':'typing.Optional[int]',
            'max_burst_length':'typing.Optional[int]',
            'first_burst_length':'typing.Optional[int]',
            'immediate_data':'bool',
            'iser':'bool',
            'offload':'bool',
    })
    Session_ = typing.TypedDict('Session_', {
            'initiator':'str',
            'initiator_addr':'str',
            'initiator_alias':'typing.Optional[str]',
            'target':'str',
            'target_alias':'str',
            'header_digest':'typing.Optional[str]',
            'data_digest':'typing.Optional[str]',
            'max_data_segment_length':'typing.Optional[int]',
            'max_receive_data_segment_length':'typing.Optional[int]',
            'max_burst_length':'typing.Optional[int]',
            'first_burst_length':'typing.Optional[int]',
            'immediate_data':'bool',
            'iser':'bool',
            'offload':'bool',
    })
    IscsiglobalUpdate = typing.TypedDict('IscsiglobalUpdate', {
            'basename':'str',
            'isns_servers':'list[str]',
            'listen_port':'int',
            'pool_avail_threshold':'typing.Optional[int]',
            'alua':'bool',
    })
