
from pytruenas import Namespace, TrueNASClient
import typing
class PoolScrub(Namespace):
    _namespace:typing.Literal['pool.scrub']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        pool_scrub_entry:'PoolScrubEntry'={},
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
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'QueryOptionsGetInstance'={},
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
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[PoolScrubEntry_]|PoolScrubEntry_|int|PoolScrubEntry_': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[PoolScrubEntry_]:
            
        PoolScrubEntry_:
            
        int:
            
        PoolScrubEntry_:
            
        """
        ...
    @typing.overload
    def run(self, 
        name:'str',
        threshold:'int'=35,
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
        action:'str'="START",
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
        pool_scrub_update:'PoolScrubUpdate'={},
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

class PoolScrubEntry(typing.TypedDict):
        pool:'int'
        threshold:'int'
        description:'str'
        schedule:'Schedule'
        enabled:'bool'
        ...
class Schedule(typing.TypedDict):
        minute:'str'
        hour:'str'
        dom:'str'
        month:'str'
        dow:'str'
        ...
class PoolScrubCreateReturns(typing.TypedDict):
        pool:'int'
        threshold:'int'
        description:'str'
        schedule:'Schedule'
        enabled:'bool'
        id:'int'
        pool_name:'str'
        ...
class QueryOptionsGetInstance(typing.TypedDict):
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
class PoolScrubEntry_(typing.TypedDict):
        pool:'int'
        threshold:'int'
        description:'str'
        schedule:'Schedule'
        enabled:'bool'
        id:'int'
        pool_name:'str'
        ...
class PoolScrubUpdate(typing.TypedDict):
        pool:'int'
        threshold:'int'
        description:'str'
        schedule:'Schedule'
        enabled:'bool'
        pool_name:'str'
        ...
class PoolScrubUpdateReturns(typing.TypedDict):
        pool:'int'
        threshold:'int'
        description:'str'
        schedule:'Schedule'
        enabled:'bool'
        id:'int'
        pool_name:'str'
        ...
