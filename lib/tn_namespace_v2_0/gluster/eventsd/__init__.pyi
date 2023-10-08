
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class GlusterEventsd(Namespace):
    _namespace:_ty.Literal['gluster.eventsd']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        webhook_create:'dict[str]'={},
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
    @_ty.overload
    def delete(self, 
        webhook_delete:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
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
