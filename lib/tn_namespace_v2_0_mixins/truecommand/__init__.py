
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class Truecommand(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'truecommand')

    TruecommandEntry = typing.TypedDict('TruecommandEntry', {
            'id':'int',
            'api_key':'typing.Optional[str]',
            'status':'Status',
            'status_reason':'StatusReason',
            'remote_url':'typing.Optional[str]',
            'remote_ip_address':'typing.Optional[str]',
            'enabled':'bool',
    })
    class Status(str,Enum):
        CONNECTED = 'CONNECTED'
        CONNECTING = 'CONNECTING'
        DISABLED = 'DISABLED'
        FAILED = 'FAILED'
        ...
    class StatusReason(str,Enum):
        TruecommandServiceIsConnected = 'Truecommand service is connected.'
        PendingConfirmationFromIXPortalForTruecommandAPIKey = 'Pending Confirmation From iX Portal for Truecommand API Key.'
        TruecommandServiceIsDisabled = 'Truecommand service is disabled.'
        TruecommandAPIKeyDisabledByIXPortal = 'Truecommand API Key Disabled by iX Portal.'
        ...
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
            'status':'Status',
            'status_reason':'StatusReason',
            'remote_url':'typing.Optional[str]',
            'remote_ip_address':'typing.Optional[str]',
            'enabled':'bool',
    })
