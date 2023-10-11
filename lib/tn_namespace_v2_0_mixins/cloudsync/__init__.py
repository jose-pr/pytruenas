
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Cloudsync(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'cloudsync')

    CloudSyncCreate = typing.TypedDict('CloudSyncCreate', {
            'description':'str',
            'path':'str',
            'credentials':'int',
            'attributes':'dict[str]',
            'schedule':'Schedule',
            'pre_script':'str',
            'post_script':'str',
            'snapshot':'bool',
            'bwlimit':'list[CloudSyncBwlimit]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'Direction',
            'transfer_mode':'TransferMode',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    CloudSyncBwlimit = typing.TypedDict('CloudSyncBwlimit', {
            'time':'str',
            'bandwidth':'typing.Optional[int]',
    })
    class Direction(str,Enum):
        PUSH = 'PUSH'
        PULL = 'PULL'
        ...
    class TransferMode(str,Enum):
        SYNC = 'SYNC'
        COPY = 'COPY'
        MOVE = 'MOVE'
        ...
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
    CloudSyncLs = typing.TypedDict('CloudSyncLs', {
            'credentials':'int',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'attributes':'dict[str]',
            'args':'str',
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
    CloudSyncRestore = typing.TypedDict('CloudSyncRestore', {
            'description':'str',
            'transfer_mode':'TransferMode_',
            'path':'str',
    })
    class TransferMode_(str,Enum):
        SYNC = 'SYNC'
        COPY = 'COPY'
        ...
    CloudSyncSyncOptions = typing.TypedDict('CloudSyncSyncOptions', {
            'dry_run':'bool',
    })
    CloudSyncSyncOnetime = typing.TypedDict('CloudSyncSyncOnetime', {
            'description':'str',
            'path':'str',
            'credentials':'int',
            'attributes':'dict[str]',
            'schedule':'Schedule',
            'pre_script':'str',
            'post_script':'str',
            'snapshot':'bool',
            'bwlimit':'list[CloudSyncBwlimit]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'Direction',
            'transfer_mode':'TransferMode',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
    CloudSyncSyncOnetimeOptions = typing.TypedDict('CloudSyncSyncOnetimeOptions', {
            'dry_run':'bool',
    })
    CloudSyncUpdate = typing.TypedDict('CloudSyncUpdate', {
            'description':'str',
            'path':'str',
            'credentials':'int',
            'attributes':'dict[str]',
            'schedule':'Schedule',
            'pre_script':'str',
            'post_script':'str',
            'snapshot':'bool',
            'bwlimit':'list[CloudSyncBwlimit]',
            'include':'list[str]',
            'exclude':'list[str]',
            'transfers':'typing.Optional[int]',
            'args':'str',
            'enabled':'bool',
            'direction':'Direction',
            'transfer_mode':'TransferMode',
            'encryption':'bool',
            'filename_encryption':'bool',
            'encryption_password':'str',
            'encryption_salt':'str',
            'create_empty_src_dirs':'bool',
            'follow_symlinks':'bool',
    })
