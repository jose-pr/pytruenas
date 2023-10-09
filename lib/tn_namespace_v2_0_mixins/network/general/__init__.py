
from pytruenas.base import Namespace

import typing
class NetworkGeneral(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'network.general')

    NetworkSummary = typing.TypedDict('NetworkSummary', {
            'ips':'dict[str]',
            'default_routes':'list[str]',
            'nameservers':'list[str]',
    })
