
from pytruenas import Namespace, TrueNASClient
import typing
class Truecommand(Namespace):
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

class TruecommandEntry(typing.TypedDict):
        id:'int'
        api_key:'typing.Optional[str]'
        status:'str'
        status_reason:'str'
        remote_url:'typing.Optional[str]'
        remote_ip_address:'typing.Optional[str]'
        enabled:'bool'
        ...
class TruecommandConnected(typing.TypedDict):
        connected:'bool'
        truecommand_ip:'typing.Optional[str]'
        truecommand_url:'typing.Optional[str]'
        status:'str'
        status_reason:'str'
        ...
class TruecommandUpdate(typing.TypedDict):
        enabled:'bool'
        api_key:'typing.Optional[str]'
        ...
class TruecommandUpdateReturns(typing.TypedDict):
        id:'int'
        api_key:'typing.Optional[str]'
        status:'str'
        status_reason:'str'
        remote_url:'typing.Optional[str]'
        remote_ip_address:'typing.Optional[str]'
        enabled:'bool'
        ...