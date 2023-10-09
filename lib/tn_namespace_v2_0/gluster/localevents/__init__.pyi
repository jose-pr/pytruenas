
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class GlusterLocalevents(
    Namespace
    ):
    _namespace:typing.Literal['gluster.localevents']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def add_jwt_secret(self, 
        add_secret:'AddSecret'={},
    /) -> None: 
        """
        Add a `secret` key used to encode/decode
        JWT messages for sending/receiving gluster
        events.
        
        `secret` String representing the key to be used
                    to encode/decode JWT messages
        `force` Boolean if set to True, will forcefully
                    wipe any existing jwt key for this
                    peer. Note, if forcefully adding a
                    new key, the other peers in the TSP
                    will also need to be sent this key.
        
        Note: this secret is only used for messages
        that are destined for the api endpoint at
        http://*:6000/_clusterevents for each peer
        in the trusted storage pool.
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        add_secret:
            add_secret
        Returns
        -------
        """
        ...
    @typing.overload
    def get_set_jwt_secret(self, 
    /) -> 'str': 
        """
        Return the secret key used to encode/decode
        JWT messages for sending/receiving gluster
        events.
        
        Note: this secret is only used for messages
        that are destined for the api endpoint at
        http://*:6000/_clusterevents for each peer
        in the trusted storage pool.
        
        WARNING: clustering APIs are not intended for 3rd-party consumption and may result
        in a misconfigured SCALE cluster, production outage, or data loss.

        Parameters
        ----------
        Returns
        -------
        str:
            get_set_jwt_secret
        """
        ...
    AddSecret = typing.TypedDict('AddSecret', {
            'secret':'str',
            'force':'bool',
    })
