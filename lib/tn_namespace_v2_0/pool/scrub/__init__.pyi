
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class PoolScrub(
    Namespace
    ):
    _namespace:typing.Literal['pool.scrub']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        pool_scrub_entry:'PoolScrubEntry',
    /) -> 'PoolScrubCreateReturns': 
        """
        Create a scrub task for a pool.
        
        `threshold` refers to the minimum amount of time in days has to be passed before
        a scrub can run again.

        Parameters
        ----------
        pool_scrub_entry:
            pool_scrub_entry
        Returns
        -------
        PoolScrubCreateReturns:
            pool_scrub_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete scrub task of `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance',
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]',
        query_options:'QueryOptions',
    /) -> 'typing.Union[list[PoolScrubEntry_], PoolScrubEntry_, int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[PoolScrubEntry_], PoolScrubEntry_, int]:
            
        """
        ...
    @typing.overload
    def run(self, 
        name:'str',
        threshold:'int',
    /) -> None: 
        """
        Initiate a scrub of a pool `name` if last scrub was performed more than `threshold` days before.

        Parameters
        ----------
        name:
            name
        threshold:
            threshold
        Returns
        -------
        """
        ...
    @typing.overload
    def scrub(self, 
        name:'str',
        action:'Action',
    /) -> None: 
        """
        Start/Stop/Pause a scrub on pool `name`.

        Parameters
        ----------
        name:
            name
        action:
            action
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        pool_scrub_update:'PoolScrubUpdate',
    /) -> 'PoolScrubUpdateReturns': 
        """
        Update scrub task of `id`.

        Parameters
        ----------
        id:
            Update scrub task of `id`.
            Create a scrub task for a pool.
        pool_scrub_update:
            pool_scrub_update
        Returns
        -------
        PoolScrubUpdateReturns:
            pool_scrub_update_returns
        """
        ...
    class Action(str,Enum):
        START = 'START'
        STOP = 'STOP'
        PAUSE = 'PAUSE'
        ...
    PoolScrubCreateReturns = typing.TypedDict('PoolScrubCreateReturns', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule',
            'enabled':'bool',
            'id':'int',
            'pool_name':'str',
    })
    PoolScrubEntry = typing.TypedDict('PoolScrubEntry', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule',
            'enabled':'bool',
    })
    PoolScrubEntry_ = typing.TypedDict('PoolScrubEntry_', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule',
            'enabled':'bool',
            'id':'int',
            'pool_name':'str',
    })
    PoolScrubUpdate = typing.TypedDict('PoolScrubUpdate', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule',
            'enabled':'bool',
            'pool_name':'str',
    })
    PoolScrubUpdateReturns = typing.TypedDict('PoolScrubUpdateReturns', {
            'pool':'int',
            'threshold':'int',
            'description':'str',
            'schedule':'Schedule',
            'enabled':'bool',
            'id':'int',
            'pool_name':'str',
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
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
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
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
