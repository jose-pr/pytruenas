
from pytruenas import Namespace
class SystemSecurity(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'system.security')

