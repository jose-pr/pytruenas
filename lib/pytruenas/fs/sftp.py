import typing as _ty
from os import stat_result as _stat
import io as _io
import asyncssh as _ssh
import os as _os

if _ty.TYPE_CHECKING:
    from . import Path


from .. import _utils

_STATMAP = {"st_mode": "permissions"}


def _sftpfailure(path: "Path", failure: "_ssh.SFTPFailure", filetype: int):
    if filetype == _ssh.FILEXFER_TYPE_UNKNOWN:
        return FileNotFoundError(path)


_C = _ty.ParamSpec("C")
_T = _ty.TypeVar("T")


def _syncsftp(
    commamd: _ty.Callable[_C, _ty.Awaitable[_T]],
    *args: _C.args,
    sftpfailure=None,
    **kwargs: _C.kwargs,
) -> _T:
    path: Path = args[0]
    try:
        return _utils.async_to_sync(commamd(path._path, *args[1:], **kwargs))
    except _ssh.SFTPFileAlreadyExists:
        raise FileExistsError(path)
    except _ssh.SFTPNoSuchPath:
        raise FileNotFoundError(path)
    except _ssh.SFTPFailure as failure:
        filetype = path._client.sftp._type(path._path)
        sftpfailure = sftpfailure or _sftpfailure
        error = sftpfailure(path, failure, filetype)
        if not error:
            error = Exception(path, failure, filetype)
        raise error


def exists(path: "Path"):
    return _syncsftp(path._client.sftp.exists, path)


def stat(path: "Path"):
    stat = _syncsftp(path._client.sftp.stat, path)
    return _stat(
        [
            getattr(stat, _STATMAP.get(field, field.removeprefix("st_")), None)
            for field in _utils.STAT_FIELDS
        ]
    )


def chmod(path: "Path", mode: int):
    return _syncsftp(path._client.sftp.chmod, path)


def chown(
    path: "Path",
    uid: int,
    gid: int,
    *,
    follow_symlinks: bool = True,
):
    if uid == -1:
        uid = None
    if gid == -1:
        gid = None
    if not follow_symlinks:
        raise NotImplementedError("not follow_symlinks")
    return _syncsftp(path._client.sftp.chown, path, uid, gid)


def _mkdir_sftpfailure(path: "Path", failure: "_ssh.SFTPFailure", filetype: int):
    error = _sftpfailure(path, failure, filetype)
    if error:
        return error
    match filetype:
        case _ssh.FILEXFER_TYPE_DIRECTORY:
            return FileExistsError(path)
        case _:
            return NotADirectoryError(path)


def mkdir(path: "Path", mode: int = 511, parents=False, exist_ok=False):
    try:
        return _syncsftp(path._client.sftp.mkdir, path, sftpfailure=_mkdir_sftpfailure)
    except FileExistsError as e:
        if not exist_ok:
            raise e
    except FileNotFoundError as e:
        if not parents:
            raise e
        mkdir(path.parent, mode, parents)


def unlink(path: "Path", missing_ok=False):
    try:
        return _syncsftp(path._client.sftp.unlink, path)
    except FileNotFoundError as e:
        if not missing_ok:
            raise e


def rmdir(path: "Path"):
    return _syncsftp(path._client.sftp.rmdir, path)


def rename(path: "Path", target):
    return _syncsftp(path._client.sftp.rename, path, _os.fspath(target))


def readlink(path: "Path"):
    return _syncsftp(path._client.sftp.readlink, path)


def open(
    path: "Path",
    mode: str,
    buffering=-1,
):
    if "b" not in mode:
        raise NotImplementedError(mode)
    if buffering != -1:
        pass

    file = _syncsftp(path._client.sftp.open, path, mode)
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
