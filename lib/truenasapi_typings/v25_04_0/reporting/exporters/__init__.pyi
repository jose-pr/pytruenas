from pytruenas import Namespace as _NS 
class ReportingExporters(_NS):
    
    def create(
        reporting_exporter_create,
    ) -> ReportingExportersCreate:
        """Create a specific reporting exporter configuration containing required details for exporting reporting metrics."""
        ...
    def delete(
        id,
    ) -> ReportingExportersDelete:
        """Delete Reporting Exporter of `id`."""
        ...
    def exporter_schemas(
    ) -> ReportingExportersExporter_schemas:
        """Get the schemas for all the reporting export types we support with their respective attributes required for successfully exporting reporting metrics to them."""
        ...
    def get_instance(
        id,
        options,
    ) -> ReportingExportersGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(
        filters,
        options,
    ) -> ReportingExportersQuery:
        """"""
        ...
    def update(
        id,
        reporting_exporter_update,
    ) -> ReportingExportersUpdate:
        """Update Reporting Exporter of `id`."""
        ...
class ReportingExportersCreate:
    ...
class ReportingExportersDelete:
    ...
class ReportingExportersExporter_schemas:
    ...
class ReportingExportersGet_instance:
    ...
class ReportingExportersQuery:
    ...
class ReportingExportersUpdate:
    ... 