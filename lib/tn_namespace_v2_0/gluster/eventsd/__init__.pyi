
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class GlusterEventsd(
    Namespace
    ):
    _namespace:typing.Literal['gluster.eventsd']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        webhook_create:'WebhookCreate'={},
    /) -> None: 
        """
        Add `url` webhook that will be called
        with a JSON formatted POST request that
        will include the event that was triggered
        along with the relevant data.
        
        `url` is a http address (i.e. http://192.168.1.50/endpoint)
        `bearer_token` is a bearer token
        `secret` secret to encode the JWT message
        
        NOTE: This webhook will be synchronized to all
        peers in the trusted storage pool.

        Parameters
        ----------
        webhook_create:
            webhook_create
        Returns
        -------
        """
        ...
    @typing.overload
    def delete(self, 
        webhook_delete:'WebhookDelete'={},
    /) -> None: 
        """
        Delete `url` webhook
        
        `url` is a http address (i.e. http://192.168.1.50/endpoint)

        Parameters
        ----------
        webhook_delete:
            webhook_delete
        Returns
        -------
        """
        ...
    @typing.overload
    def sync(self, 
    /) -> None: 
        """
        Sync the webhooks config file to all peers in the
        trusted storage pool

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def webhooks(self, 
    /) -> None: 
        """
        List the current webhooks (if any)

        Parameters
        ----------
        Returns
        -------
        """
        ...
    WebhookCreate = typing.TypedDict('WebhookCreate', {
            'url':'str',
            'bearer_token':'str',
            'secret':'str',
    })
    WebhookDelete = typing.TypedDict('WebhookDelete', {
            'url':'str',
    })
