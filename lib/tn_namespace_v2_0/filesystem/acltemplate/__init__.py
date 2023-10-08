
from pytruenas import Namespace
class FilesystemAcltemplate(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'filesystem.acltemplate')

