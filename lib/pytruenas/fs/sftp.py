import typing as _ty
from os import stat_result as _stat
import io as _io
import asyncssh as _ssh


if _ty.TYPE_CHECKING:
    from . import Path


from .. import _utils

_STATMAP = {"st_mode": "permissions"}


def exists(path: "Path"):
    return _utils.async_to_sync(path._client.sftp.exists(path.as_posix()))


def stat(path: "Path"):
    stat = _utils.async_to_sync(path._client.sftp.stat(path.as_posix()))
    return _stat(
        [
            getattr(stat, _STATMAP.get(field, field.removeprefix("st_")), None)
            for field in _utils.STAT_FIELDS
        ]
    )


def chown(
    path: "Path",
    uid: int,
    gid: int,
    *,
    follow_symlinks: bool = True,
):

    if not follow_symlinks:
        raise NotImplementedError("not follow_symlinks")
    _utils.async_to_sync(path._client.sftp.chown(path.as_posix(), uid, gid))


def mkdir(path: "Path", mode: int = 511, parents=False, exist_ok=False):
    try:
        _utils.async_to_sync(path._client.sftp.mkdir(path.as_posix()))
    except FileExistsError as e:
        if not exist_ok:
            raise e
    except FileNotFoundError as e:
        if not parents:
            raise e
        mkdir(path.parent, mode, parents)


def unlink(path: "Path", missing_ok=False):
    try:
        _utils.async_to_sync(path._client.sftp.unlink(path.as_posix()))
    except FileNotFoundError as e:
        if not missing_ok:
            raise e


def rmdir(path: "Path"):
    _utils.async_to_sync(path._client.sftp.rmdir(path.as_posix()))


def rename(path: "Path", target):
    _utils.async_to_sync(path._client.sftp.rename(path.as_posix(), target))


def readlink(path: "Path"):
    return _utils.async_to_sync(path._client.sftp.readlink(path.as_posix()))


def open(
    path: "Path",
    mode: str,
    buffering=-1,
):
    if "b" not in mode:
        raise NotImplementedError(mode)
    if buffering != -1:
        pass

    file = _utils.async_to_sync(path._client.sftp.open(path.as_posix(), mode))
    return _AsynToSyncFileHandle(file)


class _AsynToSyncFileHandle(_io.IOBase):
    def __init__(self, fh: _ssh.SFTPClientFile):
        super().__init__()
        self.fh = fh

    def readable(self):
        return True

    def writable(self):
        return True

    def seekable(self):
        return True

    def write(self, data):
        return _utils.async_to_sync(self.fh.write(data))

    def flush(self):
        pass

    def close(self):
        return _utils.async_to_sync(self.fh.close())

    def seek(self, offset, whence=0):
        return _utils.async_to_sync(self.fh.seek(offset, whence))

    def tell(self):
        return _utils.async_to_sync(self.fh.tell())

    def read(self, size: int = -1):
        return _utils.async_to_sync(self.fh.read(size))

    def truncate(self, size=None):
        return _utils.async_to_sync(self.fh.truncate(size))
