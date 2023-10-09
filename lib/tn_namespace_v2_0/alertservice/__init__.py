
from pytruenas import Namespace
import typing
class Alertservice(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'alertservice')

    AlertServiceCreate = typing.TypedDict('AlertServiceCreate', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'str',
            'enabled':'bool',
    })
    AlertserviceCreateReturns = typing.TypedDict('AlertserviceCreateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'str',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
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
    AlertServiceType = typing.TypedDict('AlertServiceType', {
            'name':'str',
            'title':'str',
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
    AlertserviceEntry = typing.TypedDict('AlertserviceEntry', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'str',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
    })
    AlertserviceEntry_ = typing.TypedDict('AlertserviceEntry_', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'str',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
    })
    AlertserviceEntry__ = typing.TypedDict('AlertserviceEntry__', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'str',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
    })
    AlertServiceCreate_ = typing.TypedDict('AlertServiceCreate_', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'str',
            'enabled':'bool',
    })
    AlertServiceUpdate = typing.TypedDict('AlertServiceUpdate', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'str',
            'enabled':'bool',
    })
    AlertserviceUpdateReturns = typing.TypedDict('AlertserviceUpdateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'level':'str',
            'enabled':'bool',
            'id':'int',
            'type__title':'str',
    })
