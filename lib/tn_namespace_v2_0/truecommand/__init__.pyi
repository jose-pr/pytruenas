
from pytruenas import TrueNASClient
from pytruenas.base import Namespace

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
    @typing.overload
    def update(self, 
        truecommand_update:'TruecommandUpdate'={},
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

