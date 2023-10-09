
from pytruenas.base import Namespace

import typing
class ZfsSnapshot(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'zfs.snapshot')

    SnapshotClone = typing.TypedDict('SnapshotClone', {
            'snapshot':'str',
            'dataset_dst':'str',
            'dataset_properties':'dict[str]',
    })
    SnapshotCreate = typing.TypedDict('SnapshotCreate', {
            'dataset':'str',
            'name':'str',
            'naming_schema':'str',
            'recursive':'bool',
            'exclude':'list[str]',
            'suspend_vms':'bool',
            'vmware_sync':'bool',
            'properties':'dict[str]',
    })
    Options = typing.TypedDict('Options', {
            'defer':'bool',
            'recursive':'bool',
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
    Options_ = typing.TypedDict('Options_', {
            'recursive':'bool',
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
    SnapshotRemove = typing.TypedDict('SnapshotRemove', {
            'dataset':'str',
            'name':'str',
            'defer_delete':'bool',
    })
    Options__ = typing.TypedDict('Options__', {
            'recursive':'bool',
            'recursive_clones':'bool',
            'force':'bool',
            'recursive_rollback':'bool',
    })
    UserProperty = typing.TypedDict('UserProperty', {
            'key':'str',
            'value':'str',
            'remove':'bool',
    })
    SnapshotUpdate = typing.TypedDict('SnapshotUpdate', {
            'user_properties_update':'list[UserProperty]',
    })
