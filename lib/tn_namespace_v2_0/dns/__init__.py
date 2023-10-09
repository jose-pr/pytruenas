
from pytruenas import Namespace
import typing
class Dns(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'dns')

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
    Nameserver = typing.TypedDict('Nameserver', {
            'nameserver':'str',
    })
    Nameserver_ = typing.TypedDict('Nameserver_', {
            'nameserver':'str',
    })
