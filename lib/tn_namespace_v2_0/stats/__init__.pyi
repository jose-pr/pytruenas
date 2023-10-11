
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Stats(
    Namespace
    ):
    _namespace:typing.Literal['stats']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def get_data(self, 
        stats_list:'list[StatsData]',
        stats_filter:'StatsFilter',
    /) -> 'StatsData_': 
        """
        Get data points from rrd files.

        Parameters
        ----------
        stats_list:
            stats_list
        stats_filter:
            stats-filter
        Returns
        -------
        StatsData_:
            stats_data
        """
        ...
    @typing.overload
    def get_dataset_info(self, 
        source:'str',
        type:'str',
    /) -> 'DatasetInfo': 
        """
        Returns info about a given dataset from some source.

        Parameters
        ----------
        source:
            source
        type:
            type
        Returns
        -------
        DatasetInfo:
            dataset_info
        """
        ...
    @typing.overload
    def get_sources(self, 
    /) -> 'dict[str]': 
        """
        Returns an object with all available sources tried with metric datasets.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            stats_sources
        """
        ...
    StatsData = typing.TypedDict('StatsData', {
            'source':'str',
            'type':'str',
            'dataset':'str',
            'cf':'str',
    })
    StatsFilter = typing.TypedDict('StatsFilter', {
            'step':'int',
            'start':'str',
            'end':'str',
    })
    StatsData_ = typing.TypedDict('StatsData_', {
            'about':'str',
            'meta':'dict[str]',
            'data':'list',
    })
    DatasetInfo = typing.TypedDict('DatasetInfo', {
            'source':'str',
            'type':'str',
            'datasets':'dict[str]',
            'step':'int',
            'last_update':'int',
    })
