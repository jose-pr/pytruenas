
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Stats(Namespace):
    _namespace:_ty.Literal['stats']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def get_data(self, 
        stats_list:'list'=[],
        stats_filter:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            stats_data
        """
        ...
    @_ty.overload
    def get_dataset_info(self, 
        source:'str',
        type:'str',
    /) -> 'dict[str]': 
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
        dict[str]:
            dataset_info
        """
        ...
    @_ty.overload
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
