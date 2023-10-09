
from pytruenas import Namespace
import typing
class GlusterEventsd(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'gluster.eventsd')

    WebhookCreate = typing.TypedDict('WebhookCreate', {
            'url':'str',
            'bearer_token':'str',
            'secret':'str',
    })
    WebhookDelete = typing.TypedDict('WebhookDelete', {
            'url':'str',
    })
