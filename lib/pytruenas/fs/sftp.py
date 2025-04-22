import typing as _ty

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient as _Client
    from pathlib import PosixPath as _Path

from .. import _utils


def exists(path: "_Path", *, client: "_Client"):
    return _utils.async_to_sync(client.sftp.exists(path.as_posix()))
