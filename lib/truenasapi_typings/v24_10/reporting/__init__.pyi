from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .exporters import ReportingExporters 
class Reporting(_NS):
    
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingConfig:
        """"""
        ...
    def get_data(self,
        graphs:list[GraphIdentifier],
        query:query,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ReportingGetDataResponse]:
        """Get reporting data for given graphs.

List of possible graphs can be retrieved using `reporting.graphs` call.

For the time period of the graph either `unit` and `page` OR `start` and `end` should be used, not both.

`aggregate` will return aggregate available data for each graph (e.g. min, max, mean)."""
        ...
    def graph(self,
        str:str,
        query:query,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ReportingGetDataResponse]:
        """Get reporting data for `name` graph."""
        ...
    def graphs(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ReportingGraphQueryResultItem]|ReportingGraphQueryResultItem|int:
        """"""
        ...
    def netdata_get_data(self,
        graphs:list[GraphIdentifier],
        query:query,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ReportingGetDataResponse]:
        """Get reporting data for given graphs.

List of possible graphs can be retrieved using `reporting.netdata_graphs` call.

For the time period of the graph either `unit` and `page` OR `start` and `end` should be used, not both.

`aggregate` will return aggregate available data for each graph (e.g. min, max, mean)."""
        ...
    def netdata_graph(self,
        str:str,
        query:query,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ReportingGetDataResponse]:
        """Get reporting data for `name` graph."""
        ...
    def netdata_graphs(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ReportingGraphQueryResultItem]|ReportingGraphQueryResultItem|int:
        """Get reporting netdata graphs."""
        ...
    def update(self,
        reporting_update:reporting_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingUpdate:
        """`tier1_days` can be set to specify for how many days we want to store reporting history which in netdata terms specifies the number of days netdata should be storing data in tier1 storage."""
        ...
    exporters: ReportingExporters
ReportingConfig = _ty.TypedDict('ReportingConfig', {
    'id': int,
    'tier0_days': int,
    'tier1_days': int,
    'tier1_update_interval': int, 
})
GraphIdentifier = _ty.TypedDict('GraphIdentifier', {
    'name': str,
    'identifier': _ty.NotRequired[str|None], 
})
query = _ty.TypedDict('query', {
    'unit': _ty.NotRequired[str|None],
    'page': _ty.NotRequired[int],
    'aggregate': _ty.NotRequired[bool],
    'start': _ty.NotRequired[int|None],
    'end': _ty.NotRequired[int|None], 
})
ReportingGetDataResponse = _ty.TypedDict('ReportingGetDataResponse', {
    'name': str,
    'identifier': str|None,
    'data': _jsonschema.JsonArray,
    'aggregations': _jsonschema.JsonValue,
    'start': int,
    'end': int,
    'legend': list[str], 
})
options = _ty.TypedDict('options', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
ReportingGraphQueryResultItem = _ty.TypedDict('ReportingGraphQueryResultItem', {
    'name': _ty.NotRequired[str],
    'title': _ty.NotRequired[str],
    'vertical_label': _ty.NotRequired[str],
    'identifiers': _ty.NotRequired[list[str]|None], 
})
reporting_update = _ty.TypedDict('reporting_update', {
    'tier0_days': _ty.NotRequired[int],
    'tier1_days': _ty.NotRequired[int],
    'tier1_update_interval': _ty.NotRequired[int], 
})
ReportingUpdate = _ty.TypedDict('ReportingUpdate', {
    'id': int,
    'tier0_days': int,
    'tier1_days': int,
    'tier1_update_interval': int, 
})