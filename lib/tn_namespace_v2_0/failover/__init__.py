
from pytruenas.base import Namespace

import typing
from enum import Enum

class Failover(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'failover')

    Options = typing.TypedDict('Options', {
            'timeout':'int',
            'job':'bool',
            'job_return':'typing.Optional[bool]',
            'callback':'typing.Union[str, int, bool, dict[str], list]',
            'connect_timeout':'float',
            'raise_connect_error':'bool',
    })
    FailoverEntry = typing.TypedDict('FailoverEntry', {
            'id':'int',
            'disabled':'bool',
            'timeout':'int',
            'master':'bool',
    })
    class Action(str,Enum):
        ENABLE = 'ENABLE'
        DISABLE = 'DISABLE'
        ...
    Options_ = typing.TypedDict('Options_', {
            'active':'bool',
    })
    Options__ = typing.TypedDict('Options__', {
            'reboot':'bool',
    })
    PoolKeys = typing.TypedDict('PoolKeys', {
            'name':'str',
            'passphrase':'str',
    })
    DatasetKeys = typing.TypedDict('DatasetKeys', {
            'name':'str',
            'passphrase':'str',
    })
    Options___ = typing.TypedDict('Options___', {
            'pools':'list[PoolKeys]',
            'datasets':'list[DatasetKeys]',
    })
    FailoverUpdate = typing.TypedDict('FailoverUpdate', {
            'disabled':'bool',
            'timeout':'int',
            'master':'typing.Optional[bool]',
    })
    FailoverUpdateReturns = typing.TypedDict('FailoverUpdateReturns', {
            'id':'int',
            'disabled':'bool',
            'timeout':'int',
            'master':'bool',
    })
    FailoverUpgrade = typing.TypedDict('FailoverUpgrade', {
            'train':'str',
            'resume':'bool',
            'resume_manual':'bool',
    })
