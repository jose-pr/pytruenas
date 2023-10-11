
from pytruenas.base import Namespace

import typing
from enum import Enum

class Config(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'config')

    Configsave = typing.TypedDict('Configsave', {
            'secretseed':'bool',
            'pool_keys':'bool',
            'root_authorized_keys':'bool',
            'gluster_config':'bool',
    })
    Options = typing.TypedDict('Options', {
            'reboot':'bool',
    })
