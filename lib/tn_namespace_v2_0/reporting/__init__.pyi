
from pytruenas import Namespace, TrueNASClient
import typing
class Reporting(Namespace):
    _namespace:typing.Literal['reporting']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def clear(self, 
    /) -> None: 
        """
        Clear reporting database.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def config(self, 
    /) -> 'ReportingEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        ReportingEntry:
            reporting_entry
        """
        ...
    @typing.overload
    def get_data(self, 
        graphs:'list[Graph]'=[],
        reporting_query:'ReportingQuery'={},
    /) -> 'list[GraphReportingData]': 
        """
        Get reporting data for given graphs.
        
        List of possible graphs can be retrieved using `reporting.graphs` call.
        
        For the time period of the graph either `unit` and `page` OR `start` and `end` should be
        used, not both.
        
        `aggregate` will return aggregate available data for each graph (e.g. min, max, mean).

        Parameters
        ----------
        graphs:
            graphs
        reporting_query:
            reporting_query
        Returns
        -------
        list[GraphReportingData]:
            reporting_data
        """
        ...
    @typing.overload
    def graphs(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'int|Graph_|list[Graph_]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        int:
            
        Graph_:
            
        list[Graph_]:
            
        """
        ...
    @typing.overload
    def netdata_get_data(self, 
        graphs:'list[Graph__]'=[],
        reporting_query_netdata:'ReportingQueryNetdata'={},
    /) -> 'list[NetdataGraphReportingData]': 
        """
        Get reporting data for given graphs.
        
        List of possible graphs can be retrieved using `reporting.netdata_graphs` call.
        
        For the time period of the graph either `unit` and `page` OR `start` and `end` should be
        used, not both.
        
        `aggregate` will return aggregate available data for each graph (e.g. min, max, mean).

        Parameters
        ----------
        graphs:
            graphs
        reporting_query_netdata:
            reporting_query_netdata
        Returns
        -------
        list[NetdataGraphReportingData]:
            reporting_data
        """
        ...
    @typing.overload
    def netdata_graph(self, 
        name:'str',
        reporting_query_netdata:'ReportingQueryNetdata_'={},
    /) -> 'NetdataGraphReportingData': 
        """
        Get reporting data for `name` graph.

        Parameters
        ----------
        name:
            name
        reporting_query_netdata:
            reporting_query_netdata
        Returns
        -------
        NetdataGraphReportingData:
            netdata_graph_reporting_data
        """
        ...
    @typing.overload
    def netdata_graphs(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'int|Graph___|list[Graph___]': 
        """
        Get reporting netdata graphs.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        int:
            
        Graph___:
            
        list[Graph___]:
            
        """
        ...
    @typing.overload
    def update(self, 
        reporting_update:'ReportingUpdate'={},
    /) -> 'ReportingUpdateReturns': 
        """
        Configure Reporting Database settings.
        
        `graphite` specifies a destination hostname or IP for collectd data sent by the Graphite plugin..
        
        `graphite_separateinstances` corresponds to collectd SeparateInstances option.
        
        `graph_age` specifies the maximum age of stored graphs in months. `graph_points` is the number of points for
        each hourly, daily, weekly, etc. graph. Changing these requires destroying the current reporting database,
        so when these fields are changed, an additional `confirm_rrd_destroy: true` flag must be present.

        Parameters
        ----------
        reporting_update:
            reporting_update
        Returns
        -------
        ReportingUpdateReturns:
            reporting_update_returns
        """
        ...

class ReportingEntry(typing.TypedDict):
        graphite:'str'
        graphite_separateinstances:'bool'
        graph_age:'int'
        graph_points:'int'
        id:'int'
        ...
class Graph(typing.TypedDict):
        name:'str'
        identifier:'typing.Optional[str]'
        ...
class ReportingQuery(typing.TypedDict):
        unit:'str'
        page:'int'
        start:'str'
        end:'str'
        aggregate:'bool'
        ...
class GraphReportingData(typing.TypedDict):
        name:'str'
        identifier:'typing.Optional[str]'
        data:'list'
        aggregations:'Aggregations'
        ...
class Aggregations(typing.TypedDict):
        min:'list'
        max:'list'
        mean:'list'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class Graph_(typing.TypedDict):
        name:'str'
        title:'str'
        vertical_label:'str'
        identifiers:'typing.Optional[list[str]]'
        stacked:'bool'
        stacked_show_total:'bool'
        ...
class Graph__(typing.TypedDict):
        name:'str'
        identifier:'typing.Optional[str]'
        ...
class ReportingQueryNetdata(typing.TypedDict):
        unit:'str'
        page:'int'
        aggregate:'bool'
        start:'int'
        end:'int'
        ...
class NetdataGraphReportingData(typing.TypedDict):
        name:'str'
        identifier:'typing.Optional[str]'
        data:'list'
        aggregations:'Aggregations'
        ...
class ReportingQueryNetdata_(typing.TypedDict):
        unit:'str'
        page:'int'
        aggregate:'bool'
        start:'int'
        end:'int'
        ...
class Graph___(typing.TypedDict):
        name:'str'
        title:'str'
        vertical_label:'str'
        identifiers:'typing.Optional[list[str]]'
        ...
class ReportingUpdate(typing.TypedDict):
        graphite:'str'
        graphite_separateinstances:'bool'
        graph_age:'int'
        graph_points:'int'
        confirm_rrd_destroy:'bool'
        ...
class ReportingUpdateReturns(typing.TypedDict):
        graphite:'str'
        graphite_separateinstances:'bool'
        graph_age:'int'
        graph_points:'int'
        id:'int'
        ...
