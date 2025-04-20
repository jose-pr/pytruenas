from pytruenas import Namespace as _NS

from .exporters import ReportingExporters
 
class Reporting(_NS):
    
    def config(
        
    ) -> ReportingConfig:
        ...
    
    def get_data(
        
    ) -> ReportingGet_data:
        ...
    
    def graph(
        
    ) -> ReportingGraph:
        ...
    
    def graphs(
        
    ) -> ReportingGraphs:
        ...
    
    def netdata_get_data(
        
    ) -> ReportingNetdata_get_data:
        ...
    
    def netdata_graph(
        
    ) -> ReportingNetdata_graph:
        ...
    
    def netdata_graphs(
        
    ) -> ReportingNetdata_graphs:
        ...
    
    def update(
        
    ) -> ReportingUpdate:
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
 