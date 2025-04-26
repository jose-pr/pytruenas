from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Exporters(_NS):
    
    def create(self,
        reporting_exporter_create:CreateReportingExporterCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Create a specific reporting exporter configuration containing required details for exporting reporting metrics."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete Reporting Exporter of `id`."""
        ...
    def exporter_schemas(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ExporterSchemasReportingExporterSchema]:
        """Get the schemas for all the reporting export types we support with their respective attributes required for successfully exporting reporting metrics to them."""
        ...
    def get_instance(self,
        id:int,
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryReportingExporterQueryResultItem]|QueryReportingExporterQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        reporting_exporter_update:UpdateReportingExporterUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update Reporting Exporter of `id`."""
        ...
CreateReportingExporterCreate = _ty.TypedDict('CreateReportingExporterCreate', {
    'enabled': bool,
    'attributes': _jsonschema.JsonValue,
    'name': str, 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'enabled': bool,
    'attributes': _jsonschema.JsonValue,
    'name': str, 
})
ExporterSchemasReportingExporterSchema = _ty.TypedDict('ExporterSchemasReportingExporterSchema', {
    'key': str,
    'schema': _jsonschema.JsonArray, 
})
GetInstanceOptions = _ty.TypedDict('GetInstanceOptions', {
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
GetInstanceReturn = _ty.TypedDict('GetInstanceReturn', {
    'id': int,
    'enabled': bool,
    'attributes': _jsonschema.JsonValue,
    'name': str, 
})
QueryOptions = _ty.TypedDict('QueryOptions', {
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
QueryReportingExporterQueryResultItem = _ty.TypedDict('QueryReportingExporterQueryResultItem', {
    'id': _ty.NotRequired[int],
    'enabled': _ty.NotRequired[bool],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue],
    'name': _ty.NotRequired[str], 
})
UpdateReportingExporterUpdate = _ty.TypedDict('UpdateReportingExporterUpdate', {
    'enabled': _ty.NotRequired[bool],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue],
    'name': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'enabled': bool,
    'attributes': _jsonschema.JsonValue,
    'name': str, 
})