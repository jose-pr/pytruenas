
from pytruenas import Namespace, TrueNASClient
import typing
class Stats(Namespace):
    _namespace:typing.Literal['stats']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def get_data(self, 
        stats_list:'list[StatsData]'=[],
        stats_filter:'StatsFilter'={},
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

class StatsData(typing.TypedDict):
        source:'str'
        type:'str'
        dataset:'str'
        cf:'str'
        ...
class StatsFilter(typing.TypedDict):
        step:'int'
        start:'str'
        end:'str'
        ...
class StatsData_(typing.TypedDict):
        about:'str'
        meta:'dict[str]'
        data:'list'
        ...
class DatasetInfo(typing.TypedDict):
        source:'str'
        type:'str'
        datasets:'dict[str]'
        step:'int'
        last_update:'int'
        ...
