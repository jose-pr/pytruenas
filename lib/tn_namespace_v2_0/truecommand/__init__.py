
from pytruenas.base import Namespace

import typing
class Truecommand(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'truecommand')

    TruecommandEntry = typing.TypedDict('TruecommandEntry', {
            'id':'int',
            'api_key':'typing.Optional[str]',
            'status':'str',
            'status_reason':'str',
            'remote_url':'typing.Optional[str]',
            'remote_ip_address':'typing.Optional[str]',
            'enabled':'bool',
    })
    TruecommandConnected = typing.TypedDict('TruecommandConnected', {
            'connected':'bool',
            'truecommand_ip':'typing.Optional[str]',
            'truecommand_url':'typing.Optional[str]',
            'status':'str',
            'status_reason':'str',
    })
    TruecommandUpdate = typing.TypedDict('TruecommandUpdate', {
            'enabled':'bool',
            'api_key':'typing.Optional[str]',
    })
    TruecommandUpdateReturns = typing.TypedDict('TruecommandUpdateReturns', {
            'id':'int',
            'api_key':'typing.Optional[str]',
            'status':'str',
            'status_reason':'str',
            'remote_url':'typing.Optional[str]',
            'remote_ip_address':'typing.Optional[str]',
            'enabled':'bool',
    })
