import typing as _ty

if _ty.TYPE_CHECKING:
    from . import Path


from .. import _utils


def exists(path: "Path"):
    return _utils.async_to_sync(path._client.sftp.exists(path.as_posix()))
