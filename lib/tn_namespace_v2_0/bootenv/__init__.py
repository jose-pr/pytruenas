
from pytruenas import Namespace
import typing
class Bootenv(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'bootenv')

    BootenvCreate = typing.TypedDict('BootenvCreate', {
            'name':'str',
            'source':'str',
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
    BootenvEntry = typing.TypedDict('BootenvEntry', {
            'id':'str',
            'realname':'str',
            'name':'str',
            'active':'str',
            'activated':'bool',
            'can_activate':'bool',
            'mountpoint':'str',
            'space':'str',
            'created':'str',
            'keep':'bool',
            'rawspace':'int',
    })
    Attributes = typing.TypedDict('Attributes', {
            'keep':'bool',
    })
    BootenvUpdate = typing.TypedDict('BootenvUpdate', {
            'name':'str',
    })
