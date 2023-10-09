
from pytruenas.base import Namespace

import typing
from enum import Enum

class ReplicationConfig(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'replication.config')

    ReplicationConfigUpdate = typing.TypedDict('ReplicationConfigUpdate', {
            'max_parallel_replication_tasks':'typing.Optional[int]',
    })
