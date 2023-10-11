
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Truecommand(
    Namespace
    ):
    _namespace:typing.Literal['truecommand']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'TruecommandEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        TruecommandEntry:
            truecommand_entry
        """
        ...
    @typing.overload
    def connected(self, 
    /) -> 'TruecommandConnected': 
        """
        Returns information which shows if system has an authenticated api key
        and has initiated a VPN connection with TrueCommand.

        Parameters
        ----------
        Returns
        -------
        TruecommandConnected:
            truecommand_connected
        """
        ...
    @typing.overload
    def update(self, 
        truecommand_update:'TruecommandUpdate',
    /) -> 'TruecommandUpdateReturns': 
        """
        Update Truecommand service settings.
        
        `api_key` is a valid API key generated by iX Portal.

        Parameters
        ----------
        truecommand_update:
            truecommand_update
        Returns
        -------
        TruecommandUpdateReturns:
            truecommand_update_returns
        """
        ...
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
    TruecommandEntry = typing.TypedDict('TruecommandEntry', {
            'id':'int',
            'api_key':'typing.Optional[str]',
            'status':'Status',
            'status_reason':'StatusReason',
            'remote_url':'typing.Optional[str]',
            'remote_ip_address':'typing.Optional[str]',
            'enabled':'bool',
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
