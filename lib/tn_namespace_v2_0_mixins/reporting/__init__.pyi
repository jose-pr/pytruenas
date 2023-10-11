
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin
from enum import Enum
import typing
class Reporting(
    ConfigMixin,
    Namespace
    ):
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
        graphs:'list[Graph]',
        reporting_query:'ReportingQuery',
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
        query_filters:'list[list]',
        query_options:'QueryOptions',
    /) -> 'typing.Union[int, Graph_, list[Graph_]]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[int, Graph_, list[Graph_]]:
            
        """
        ...
    @typing.overload
    def netdata_get_data(self, 
        graphs:'list[Graph]',
        reporting_query_netdata:'ReportingQueryNetdata',
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
        reporting_query_netdata:'ReportingQueryNetdata',
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
        query_filters:'list[list]',
        query_options:'QueryOptions',
    /) -> 'typing.Union[int, Graph__, list[Graph__]]': 
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
        typing.Union[int, Graph__, list[Graph__]]:
            
        """
        ...
    @typing.overload
    def update(self, 
        reporting_update:'ReportingUpdate',
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
    ReportingEntry = typing.TypedDict('ReportingEntry', {
            'graphite':'str',
            'graphite_separateinstances':'bool',
            'graph_age':'int',
            'graph_points':'int',
            'id':'int',
    })
    Graph = typing.TypedDict('Graph', {
            'name':'Name',
            'identifier':'typing.Optional[str]',
    })
    ReportingQuery = typing.TypedDict('ReportingQuery', {
            'unit':'Unit',
            'page':'int',
            'start':'str',
            'end':'str',
            'aggregate':'bool',
    })
    class Unit(str,Enum):
        HOUR = 'HOUR'
        DAY = 'DAY'
        WEEK = 'WEEK'
        MONTH = 'MONTH'
        YEAR = 'YEAR'
        ...
    GraphReportingData = typing.TypedDict('GraphReportingData', {
            'name':'str',
            'identifier':'typing.Optional[str]',
            'data':'list',
            'aggregations':'Aggregations',
    })
    Aggregations = typing.TypedDict('Aggregations', {
            'min':'list',
            'max':'list',
            'mean':'list',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    Graph_ = typing.TypedDict('Graph_', {
            'name':'str',
            'title':'str',
            'vertical_label':'str',
            'identifiers':'typing.Optional[list]',
            'stacked':'bool',
            'stacked_show_total':'bool',
    })
    class Name(str,Enum):
        Cpu = 'cpu'
        Cputemp = 'cputemp'
        Disk = 'disk'
        Interface = 'interface'
        Load = 'load'
        Memory = 'memory'
        Swap = 'swap'
        Uptime = 'uptime'
        Arcactualrate = 'arcactualrate'
        Arcrate = 'arcrate'
        Arcsize = 'arcsize'
        Arcresult = 'arcresult'
        Disktemp = 'disktemp'
        ...
    ReportingQueryNetdata = typing.TypedDict('ReportingQueryNetdata', {
            'unit':'Unit',
            'page':'int',
            'aggregate':'bool',
            'start':'int',
            'end':'int',
    })
    NetdataGraphReportingData = typing.TypedDict('NetdataGraphReportingData', {
            'name':'str',
            'identifier':'typing.Optional[str]',
            'data':'list',
            'aggregations':'Aggregations',
    })
    Graph__ = typing.TypedDict('Graph__', {
            'name':'str',
            'title':'str',
            'vertical_label':'str',
            'identifiers':'typing.Optional[list]',
    })
    ReportingUpdate = typing.TypedDict('ReportingUpdate', {
            'graphite':'str',
            'graphite_separateinstances':'bool',
            'graph_age':'int',
            'graph_points':'int',
            'confirm_rrd_destroy':'bool',
    })
    ReportingUpdateReturns = typing.TypedDict('ReportingUpdateReturns', {
            'graphite':'str',
            'graphite_separateinstances':'bool',
            'graph_age':'int',
            'graph_points':'int',
            'id':'int',
    })
