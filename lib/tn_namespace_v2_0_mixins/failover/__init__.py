
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class Failover(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'failover')

    class Action(str,Enum):
        ENABLE = 'ENABLE'
        DISABLE = 'DISABLE'
        ...
    DatasetKeys = typing.TypedDict('DatasetKeys', {
            'name':'str',
            'passphrase':'str',
    })
    FailoverEntry = typing.TypedDict('FailoverEntry', {
            'id':'int',
            'disabled':'bool',
            'timeout':'int',
            'master':'bool',
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
    Options = typing.TypedDict('Options', {
            'timeout':'int',
            'job':'bool',
            'job_return':'typing.Optional[bool]',
            'callback':'typing.Union[str, int, bool, dict[str], list]',
            'connect_timeout':'float',
            'raise_connect_error':'bool',
    })
    Options_ = typing.TypedDict('Options_', {
            'active':'bool',
    })
    Options__ = typing.TypedDict('Options__', {
            'reboot':'bool',
    })
    Options___ = typing.TypedDict('Options___', {
            'pools':'list[PoolKeys]',
            'datasets':'list[DatasetKeys]',
    })
    PoolKeys = typing.TypedDict('PoolKeys', {
            'name':'str',
            'passphrase':'str',
    })
