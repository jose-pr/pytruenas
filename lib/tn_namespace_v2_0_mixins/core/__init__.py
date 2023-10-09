
from pytruenas.base import Namespace

import typing
from enum import Enum

class Core(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'core')

    Options = typing.TypedDict('Options', {
            'bind_address':'str',
            'bind_port':'int',
            'threaded':'bool',
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
    Progress = typing.TypedDict('Progress', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo = typing.TypedDict('ExcInfo', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job = typing.TypedDict('Job', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    Progress_ = typing.TypedDict('Progress_', {
            'percent':'typing.Optional[int]',
            'description':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    ExcInfo_ = typing.TypedDict('ExcInfo_', {
            'repr':'typing.Optional[str]',
            'type':'typing.Optional[str]',
            'extra':'typing.Union[str, int, bool, dict[str], list]',
    })
    Job_ = typing.TypedDict('Job_', {
            'id':'int',
            'method':'str',
            'arguments':'list',
            'transient':'bool',
            'description':'typing.Optional[str]',
            'abortable':'bool',
            'logs_path':'typing.Optional[str]',
            'logs_excerpt':'typing.Optional[str]',
            'progress':'Progress_',
            'result':'typing.Union[str, int, bool, dict[str], list]',
            'error':'typing.Optional[str]',
            'exception':'typing.Optional[str]',
            'exc_info':'ExcInfo_',
            'state':'str',
            'time_started':'typing.Optional[str]',
            'time_finished':'typing.Optional[str]',
    })
    JobUpdate = typing.TypedDict('JobUpdate', {
            'progress':'dict[str]',
    })
    class Type(str,Enum):
        ICMP = 'ICMP'
        ICMPV4 = 'ICMPV4'
        ICMPV6 = 'ICMPV6'
        ...
    Options_ = typing.TypedDict('Options_', {
            'type':'Type',
            'hostname':'str',
            'timeout':'int',
    })
    QueryOptions_ = typing.TypedDict('QueryOptions_', {
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
            'id':'str',
            'socket_family':'str',
            'address':'str',
            'authenticated':'bool',
            'call_count':'int',
    })
