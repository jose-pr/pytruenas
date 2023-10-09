
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class Reporting(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'reporting')

    ReportingEntry = typing.TypedDict('ReportingEntry', {
            'graphite':'str',
            'graphite_separateinstances':'bool',
            'graph_age':'int',
            'graph_points':'int',
            'id':'int',
    })
    Graph = typing.TypedDict('Graph', {
            'name':'str',
            'identifier':'typing.Optional[str]',
    })
    class Unit(str,Enum):
        HOUR = 'HOUR'
        DAY = 'DAY'
        WEEK = 'WEEK'
        MONTH = 'MONTH'
        YEAR = 'YEAR'
        ...
    ReportingQuery = typing.TypedDict('ReportingQuery', {
            'unit':'Unit',
            'page':'int',
            'start':'str',
            'end':'str',
            'aggregate':'bool',
    })
    Aggregations = typing.TypedDict('Aggregations', {
            'min':'list',
            'max':'list',
            'mean':'list',
    })
    GraphReportingData = typing.TypedDict('GraphReportingData', {
            'name':'str',
            'identifier':'typing.Optional[str]',
            'data':'list',
            'aggregations':'Aggregations',
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
            'identifiers':'typing.Optional[list[str]]',
            'stacked':'bool',
            'stacked_show_total':'bool',
    })
    Graph__ = typing.TypedDict('Graph__', {
            'name':'str',
            'title':'str',
            'vertical_label':'str',
            'identifiers':'typing.Optional[list[str]]',
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
    Graph___ = typing.TypedDict('Graph___', {
            'name':'Name',
            'identifier':'typing.Optional[str]',
    })
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
    NetdataGraphReportingData_ = typing.TypedDict('NetdataGraphReportingData_', {
            'name':'str',
            'identifier':'typing.Optional[str]',
            'data':'list',
            'aggregations':'Aggregations',
    })
    QueryOptions_ = typing.TypedDict('QueryOptions_', {
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
    Graph____ = typing.TypedDict('Graph____', {
            'name':'str',
            'title':'str',
            'vertical_label':'str',
            'identifiers':'typing.Optional[list[str]]',
    })
    Graph_____ = typing.TypedDict('Graph_____', {
            'name':'str',
            'title':'str',
            'vertical_label':'str',
            'identifiers':'typing.Optional[list[str]]',
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
