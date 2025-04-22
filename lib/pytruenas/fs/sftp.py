from pathlib import PurePosixPath as _Path

from .. import TrueNASClient as _Client
from .. import _utils

def exists(path:_Path, *,client:_Client):
    async def run():
        sftp = await client.ssh.start_sftp_client()
        return await sftp.exists(path.as_posix())

    return _utils.async_to_sync(run())

