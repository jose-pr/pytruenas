from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class ReportingExporters(_NS):
    
    def create(self,
        reporting_exporter_create:reporting_exporter_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingExportersCreate:
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
    ) -> list[ReportingExporterSchema]:
        """Get the schemas for all the reporting export types we support with their respective attributes required for successfully exporting reporting metrics to them."""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingExportersGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ReportingExporterQueryResultItem]|ReportingExporterQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        reporting_exporter_update:reporting_exporter_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingExportersUpdate:
        """Update Reporting Exporter of `id`."""
        ...
reporting_exporter_create = _ty.TypedDict('reporting_exporter_create', {
    'enabled': bool,
    'attributes': _jsonschema.JsonValue,
    'name': str, 
})
ReportingExportersCreate = _ty.TypedDict('ReportingExportersCreate', {
    'id': int,
    'enabled': bool,
    'attributes': _jsonschema.JsonValue,
    'name': str, 
})
ReportingExporterSchema = _ty.TypedDict('ReportingExporterSchema', {
    'key': str,
    'schema': _jsonschema.JsonArray, 
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
ReportingExportersGet_instance = _ty.TypedDict('ReportingExportersGet_instance', {
    'id': int,
    'enabled': bool,
    'attributes': _jsonschema.JsonValue,
    'name': str, 
})
ReportingExporterQueryResultItem = _ty.TypedDict('ReportingExporterQueryResultItem', {
    'id': _ty.NotRequired[int],
    'enabled': _ty.NotRequired[bool],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue],
    'name': _ty.NotRequired[str], 
})
reporting_exporter_update = _ty.TypedDict('reporting_exporter_update', {
    'enabled': _ty.NotRequired[bool],
    'attributes': _ty.NotRequired[_jsonschema.JsonValue],
    'name': _ty.NotRequired[str], 
})
ReportingExportersUpdate = _ty.TypedDict('ReportingExportersUpdate', {
    'id': int,
    'enabled': bool,
    'attributes': _jsonschema.JsonValue,
    'name': str, 
})