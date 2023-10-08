
from pytruenas import Namespace, TrueNASClient
import typing
class PoolSnapshottask(Namespace):
    _namespace:typing.Literal['pool.snapshottask']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        periodic_snapshot_create:'PeriodicSnapshotCreate'={},
    /) -> 'dict[str]': 
        """
        Create a Periodic Snapshot Task
        
        Create a Periodic Snapshot Task that will take snapshots of specified `dataset` at specified `schedule`.
        Recursive snapshots can be created if `recursive` flag is enabled. You can `exclude` specific child datasets
        or zvols from the snapshot.
        Snapshots will be automatically destroyed after a certain amount of time, specified by
        `lifetime_value` and `lifetime_unit`.
        If multiple periodic tasks create snapshots at the same time (for example hourly and daily at 00:00) the snapshot
        will be kept until the last of these tasks reaches its expiry time.
        Snapshots will be named according to `naming_schema` which is a `strftime`-like template for snapshot name
        and must contain `%Y`, `%m`, `%d`, `%H` and `%M`.

        Parameters
        ----------
        periodic_snapshot_create:
            periodic_snapshot_create
        Returns
        -------
        dict[str]:
            pool_snapshottask_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
        options:'Options'={},
    /) -> 'bool': 
        """
        Delete a Periodic Snapshot Task with specific `id`

        Parameters
        ----------
        id:
            Delete a Periodic Snapshot Task with specific `id`
        options:
            options
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def delete_will_change_retention_for(self, 
        id:'int',
    /) -> 'dict[str]': 
        """
        Returns a list of snapshots which will change the retention if periodic snapshot task `id` is deleted.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        dict[str]:
            snapshots
        """
        ...
    @typing.overload
    def foreseen_count(self, 
        periodic_snapshot_foreseen_count:'PeriodicSnapshotForeseenCount'={},
    /) -> 'int': 
        """
        Returns a number of snapshots (per-dataset) being retained if a periodic snapshot task with specific parameters
        is created.

        Parameters
        ----------
        periodic_snapshot_foreseen_count:
            periodic_snapshot_foreseen_count
        Returns
        -------
        int:
            foreseen_count
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
    def max_count(self, 
    /) -> 'int': 
        """
        Returns a maximum amount of snapshots (per-dataset) the system can sustain.

        Parameters
        ----------
        Returns
        -------
        int:
            max_count
        """
        ...
    @typing.overload
    def max_total_count(self, 
    /) -> 'int': 
        """
        Returns a maximum amount of snapshots (total) the system can sustain.

        Parameters
        ----------
        Returns
        -------
        int:
            max_total_count
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[dict[str]]|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[dict[str]]:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @typing.overload
    def run(self, 
        id:'int',
    /) -> None: 
        """
        Execute a Periodic Snapshot Task of `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        periodic_snapshot_update:'PeriodicSnapshotUpdate'={},
    /) -> 'dict[str]': 
        """
        Update a Periodic Snapshot Task with specific `id`
        
        See the documentation for `create` method for information on payload contents

        Parameters
        ----------
        id:
            Update a Periodic Snapshot Task with specific `id`
        periodic_snapshot_update:
            periodic_snapshot_update
        Returns
        -------
        dict[str]:
            pool_snapshottask_update_returns
        """
        ...
    @typing.overload
    def update_will_change_retention_for(self, 
        id:'int',
        periodic_snapshot_update_will_change_retention:'PeriodicSnapshotUpdateWillChangeRetention'={},
    /) -> 'dict[str]': 
        """
        Returns a list of snapshots which will change the retention if periodic snapshot task `id` is updated
        with `data`.

        Parameters
        ----------
        id:
            id
        periodic_snapshot_update_will_change_retention:
            periodic_snapshot_update_will_change_retention
        Returns
        -------
        dict[str]:
            snapshots
        """
        ...

class PeriodicSnapshotCreate(typing.TypedDict):
        dataset:'str'
        recursive:'bool'
        exclude:'list[str]'
        lifetime_value:'int'
        lifetime_unit:'str'
        naming_schema:'str'
        schedule:'Schedule'
        allow_empty:'bool'
        enabled:'bool'
        ...
class Schedule(typing.TypedDict):
        minute:'str'
        hour:'str'
        dom:'str'
        month:'str'
        dow:'str'
        begin:'str'
        end:'str'
        ...
class Options(typing.TypedDict):
        fixate_removal_date:'bool'
        ...
class PeriodicSnapshotForeseenCount(typing.TypedDict):
        lifetime_value:'int'
        lifetime_unit:'str'
        schedule:'Schedule'
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
class PeriodicSnapshotUpdate(typing.TypedDict):
        dataset:'str'
        recursive:'bool'
        exclude:'list[str]'
        lifetime_value:'int'
        lifetime_unit:'str'
        naming_schema:'str'
        schedule:'Schedule'
        allow_empty:'bool'
        enabled:'bool'
        fixate_removal_date:'bool'
        ...
class PeriodicSnapshotUpdateWillChangeRetention(typing.TypedDict):
        dataset:'str'
        recursive:'bool'
        exclude:'list[str]'
        lifetime_value:'int'
        lifetime_unit:'str'
        naming_schema:'str'
        schedule:'Schedule'
        allow_empty:'bool'
        enabled:'bool'
        ...