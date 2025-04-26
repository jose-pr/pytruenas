from pytruenas import Namespace as _NS
import typing as _ty 
class ReportingExporters(_NS):
    
    def create(self,
        reporting_exporter_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingExportersCreate:
        """Create a specific reporting exporter configuration containing required details for exporting reporting metrics."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingExportersDelete:
        """Delete Reporting Exporter of `id`."""
        ...
    def exporter_schemas(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingExportersExporter_schemas:
        """Get the schemas for all the reporting export types we support with their respective attributes required for successfully exporting reporting metrics to them."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingExportersGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingExportersQuery:
        """"""
        ...
    def update(self,
        id,
        reporting_exporter_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingExportersUpdate:
        """Update Reporting Exporter of `id`."""
        ...
class ReportingExportersCreate(_ty.TypedDict):
    ...
class ReportingExportersDelete(_ty.TypedDict):
    ...
class ReportingExportersExporter_schemas(_ty.TypedDict):
    ...
class ReportingExportersGet_instance(_ty.TypedDict):
    ...
class ReportingExportersQuery(_ty.TypedDict):
    ...
class ReportingExportersUpdate(_ty.TypedDict):
    ... 