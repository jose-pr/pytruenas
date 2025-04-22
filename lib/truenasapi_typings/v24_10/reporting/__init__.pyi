from pytruenas import Namespace as _NS
from .exporters import ReportingExporters 
class Reporting(_NS):
    
    def config(self,
    ) -> ReportingConfig:
        """"""
        ...
    def get_data(self,
        graphs,
        query,
    ) -> ReportingGet_data:
        """Get reporting data for given graphs.

List of possible graphs can be retrieved using `reporting.graphs` call.

For the time period of the graph either `unit` and `page` OR `start` and `end` should be used, not both.

`aggregate` will return aggregate available data for each graph (e.g. min, max, mean)."""
        ...
    def graph(self,
        str,
        query,
    ) -> ReportingGraph:
        """Get reporting data for `name` graph."""
        ...
    def graphs(self,
        filters,
        options,
    ) -> ReportingGraphs:
        """"""
        ...
    def netdata_get_data(self,
        graphs,
        query,
    ) -> ReportingNetdata_get_data:
        """Get reporting data for given graphs.

List of possible graphs can be retrieved using `reporting.netdata_graphs` call.

For the time period of the graph either `unit` and `page` OR `start` and `end` should be used, not both.

`aggregate` will return aggregate available data for each graph (e.g. min, max, mean)."""
        ...
    def netdata_graph(self,
        str,
        query,
    ) -> ReportingNetdata_graph:
        """Get reporting data for `name` graph."""
        ...
    def netdata_graphs(self,
        filters,
        options,
    ) -> ReportingNetdata_graphs:
        """Get reporting netdata graphs."""
        ...
    def update(self,
        reporting_update,
    ) -> ReportingUpdate:
        """`tier1_days` can be set to specify for how many days we want to store reporting history which in netdata terms specifies the number of days netdata should be storing data in tier1 storage."""
        ...
    exporters: ReportingExporters
class ReportingConfig:
    ...
class ReportingGet_data:
    ...
class ReportingGraph:
    ...
class ReportingGraphs:
    ...
class ReportingNetdata_get_data:
    ...
class ReportingNetdata_graph:
    ...
class ReportingNetdata_graphs:
    ...
class ReportingUpdate:
    ... 