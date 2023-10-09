
from pytruenas.base import Namespace

import typing
class FailoverDisabled(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'failover.disabled')

