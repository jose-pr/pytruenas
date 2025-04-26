from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .exporters import Exporters 
class Reporting(_NS):
    
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ConfigReturn:
        """"""
        ...
    def get_data(self,
        graphs:list[GetDataGraphIdentifier],
        query:GetDataQuery,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[GetDataReportingGetDataResponse]:
        """Get reporting data for given graphs.

List of possible graphs can be retrieved using `reporting.graphs` call.

For the time period of the graph either `unit` and `page` OR `start` and `end` should be used, not both.

`aggregate` will return aggregate available data for each graph (e.g. min, max, mean)."""
        ...
    def graph(self,
        str:str,
        query:GraphQuery,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[GraphReportingGetDataResponse]:
        """Get reporting data for `name` graph."""
        ...
    def graphs(self,
        filters:_jsonschema.JsonArray=[],
        options:GraphsOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[GraphsReportingGraphQueryResultItem]|GraphsReportingGraphQueryResultItem|int:
        """"""
        ...
    def netdata_get_data(self,
        graphs:list[NetdataGetDataGraphIdentifier],
        query:NetdataGetDataQuery,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[NetdataGetDataReportingGetDataResponse]:
        """Get reporting data for given graphs.

List of possible graphs can be retrieved using `reporting.netdata_graphs` call.

For the time period of the graph either `unit` and `page` OR `start` and `end` should be used, not both.

`aggregate` will return aggregate available data for each graph (e.g. min, max, mean)."""
        ...
    def netdata_graph(self,
        str:str,
        query:NetdataGraphQuery,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[NetdataGraphReportingGetDataResponse]:
        """Get reporting data for `name` graph."""
        ...
    def netdata_graphs(self,
        filters:_jsonschema.JsonArray=[],
        options:NetdataGraphsOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[NetdataGraphsReportingGraphQueryResultItem]|NetdataGraphsReportingGraphQueryResultItem|int:
        """Get reporting netdata graphs."""
        ...
    def update(self,
        reporting_update:UpdateReportingUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """`tier1_days` can be set to specify for how many days we want to store reporting history which in netdata terms specifies the number of days netdata should be storing data in tier1 storage."""
        ...
    exporters: Exporters
ConfigReturn = _ty.TypedDict('ConfigReturn', {
    'id': int,
    'tier0_days': int,
    'tier1_days': int,
    'tier1_update_interval': int, 
})
GetDataGraphIdentifier = _ty.TypedDict('GetDataGraphIdentifier', {
    'name': str,
    'identifier': _ty.NotRequired[str|None], 
})
GetDataQuery = _ty.TypedDict('GetDataQuery', {
    'unit': _ty.NotRequired[str|None],
    'page': _ty.NotRequired[int],
    'aggregate': _ty.NotRequired[bool],
    'start': _ty.NotRequired[int|None],
    'end': _ty.NotRequired[int|None], 
})
GetDataReportingGetDataResponse = _ty.TypedDict('GetDataReportingGetDataResponse', {
    'name': str,
    'identifier': str|None,
    'data': _jsonschema.JsonArray,
    'aggregations': _jsonschema.JsonValue,
    'start': int,
    'end': int,
    'legend': list[str], 
})
GraphQuery = _ty.TypedDict('GraphQuery', {
    'unit': _ty.NotRequired[str|None],
    'page': _ty.NotRequired[int],
    'aggregate': _ty.NotRequired[bool],
    'start': _ty.NotRequired[int|None],
    'end': _ty.NotRequired[int|None], 
})
GraphReportingGetDataResponse = _ty.TypedDict('GraphReportingGetDataResponse', {
    'name': str,
    'identifier': str|None,
    'data': _jsonschema.JsonArray,
    'aggregations': _jsonschema.JsonValue,
    'start': int,
    'end': int,
    'legend': list[str], 
})
GraphsOptions = _ty.TypedDict('GraphsOptions', {
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
GraphsReportingGraphQueryResultItem = _ty.TypedDict('GraphsReportingGraphQueryResultItem', {
    'name': _ty.NotRequired[str],
    'title': _ty.NotRequired[str],
    'vertical_label': _ty.NotRequired[str],
    'identifiers': _ty.NotRequired[list[str]|None], 
})
NetdataGetDataGraphIdentifier = _ty.TypedDict('NetdataGetDataGraphIdentifier', {
    'name': str,
    'identifier': _ty.NotRequired[str|None], 
})
NetdataGetDataQuery = _ty.TypedDict('NetdataGetDataQuery', {
    'unit': _ty.NotRequired[str|None],
    'page': _ty.NotRequired[int],
    'aggregate': _ty.NotRequired[bool],
    'start': _ty.NotRequired[int|None],
    'end': _ty.NotRequired[int|None], 
})
NetdataGetDataReportingGetDataResponse = _ty.TypedDict('NetdataGetDataReportingGetDataResponse', {
    'name': str,
    'identifier': str|None,
    'data': _jsonschema.JsonArray,
    'aggregations': _jsonschema.JsonValue,
    'start': int,
    'end': int,
    'legend': list[str], 
})
NetdataGraphQuery = _ty.TypedDict('NetdataGraphQuery', {
    'unit': _ty.NotRequired[str|None],
    'page': _ty.NotRequired[int],
    'aggregate': _ty.NotRequired[bool],
    'start': _ty.NotRequired[int|None],
    'end': _ty.NotRequired[int|None], 
})
NetdataGraphReportingGetDataResponse = _ty.TypedDict('NetdataGraphReportingGetDataResponse', {
    'name': str,
    'identifier': str|None,
    'data': _jsonschema.JsonArray,
    'aggregations': _jsonschema.JsonValue,
    'start': int,
    'end': int,
    'legend': list[str], 
})
NetdataGraphsOptions = _ty.TypedDict('NetdataGraphsOptions', {
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
NetdataGraphsReportingGraphQueryResultItem = _ty.TypedDict('NetdataGraphsReportingGraphQueryResultItem', {
    'name': _ty.NotRequired[str],
    'title': _ty.NotRequired[str],
    'vertical_label': _ty.NotRequired[str],
    'identifiers': _ty.NotRequired[list[str]|None], 
})
UpdateReportingUpdate = _ty.TypedDict('UpdateReportingUpdate', {
    'tier0_days': _ty.NotRequired[int],
    'tier1_days': _ty.NotRequired[int],
    'tier1_update_interval': _ty.NotRequired[int], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'tier0_days': int,
    'tier1_days': int,
    'tier1_update_interval': int, 
})