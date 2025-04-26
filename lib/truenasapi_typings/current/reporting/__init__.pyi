from pytruenas import Namespace as _NS
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
        graphs,
        query,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingGet_data:
        """Get reporting data for given graphs.

List of possible graphs can be retrieved using `reporting.graphs` call.

For the time period of the graph either `unit` and `page` OR `start` and `end` should be used, not both.

`aggregate` will return aggregate available data for each graph (e.g. min, max, mean)."""
        ...
    def graph(self,
        str,
        query,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingGraph:
        """Get reporting data for `name` graph."""
        ...
    def graphs(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingGraphs:
        """"""
        ...
    def netdata_get_data(self,
        graphs,
        query,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingNetdata_get_data:
        """Get reporting data for given graphs.

List of possible graphs can be retrieved using `reporting.netdata_graphs` call.

For the time period of the graph either `unit` and `page` OR `start` and `end` should be used, not both.

`aggregate` will return aggregate available data for each graph (e.g. min, max, mean)."""
        ...
    def netdata_graph(self,
        str,
        query,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingNetdata_graph:
        """Get reporting data for `name` graph."""
        ...
    def netdata_graphs(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingNetdata_graphs:
        """Get reporting netdata graphs."""
        ...
    def update(self,
        reporting_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> ReportingUpdate:
        """`tier1_days` can be set to specify for how many days we want to store reporting history which in netdata terms specifies the number of days netdata should be storing data in tier1 storage."""
        ...
    exporters: ReportingExporters
class ReportingConfig(_ty.TypedDict):
    ...
class ReportingGet_data(_ty.TypedDict):
    ...
class ReportingGraph(_ty.TypedDict):
    ...
class ReportingGraphs(_ty.TypedDict):
    ...
class ReportingNetdata_get_data(_ty.TypedDict):
    ...
class ReportingNetdata_graph(_ty.TypedDict):
    ...
class ReportingNetdata_graphs(_ty.TypedDict):
    ...
class ReportingUpdate(_ty.TypedDict):
    ... 