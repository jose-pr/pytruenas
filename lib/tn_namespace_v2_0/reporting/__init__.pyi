
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Reporting(Namespace):
    _namespace:_ty.Literal['reporting']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
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
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            reporting_entry
        """
        ...
    @_ty.overload
    def get_data(self, 
        graphs:'list'=[],
        reporting_query:'dict[str]'={},
    /) -> 'list': 
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
        list:
            reporting_data
        """
        ...
    @_ty.overload
    def graphs(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
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
            
        dict[str]:
            
        list:
            
        """
        ...
    @_ty.overload
    def netdata_get_data(self, 
        graphs:'list'=[],
        reporting_query_netdata:'dict[str]'={},
    /) -> 'list': 
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
        list:
            reporting_data
        """
        ...
    @_ty.overload
    def netdata_graph(self, 
        name:'str',
        reporting_query_netdata:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            netdata_graph_reporting_data
        """
        ...
    @_ty.overload
    def netdata_graphs(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
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
            
        dict[str]:
            
        list:
            
        """
        ...
    @_ty.overload
    def update(self, 
        reporting_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            reporting_update_returns
        """
        ...
