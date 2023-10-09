
from pytruenas.base import Namespace

import typing
class Config(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'config')

    Options = typing.TypedDict('Options', {
            'reboot':'bool',
    })
    Configsave = typing.TypedDict('Configsave', {
            'secretseed':'bool',
            'pool_keys':'bool',
            'root_authorized_keys':'bool',
            'gluster_config':'bool',
    })
