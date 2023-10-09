
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
class IscsiGlobal_(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'iscsi.global')

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
