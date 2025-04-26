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
    sftpfailure_follow_symlinks=True,
    sftpfailure_path_pos=0,
    **kwargs: _C.kwargs,
) -> _T:
    path: Path = args[sftpfailure_path_pos]

    args = [_os.fspath(arg) if hasattr(arg, "__fspath__") else arg for arg in args]

    try:
        return _utils.async_to_sync(commamd(*args, **kwargs))
    except _ssh.SFTPFileAlreadyExists:
        raise FileExistsError(path)
    except (_ssh.SFTPNoSuchPath, _ssh.SFTPNoSuchFile):
        raise FileNotFoundError(path)
    except _ssh.SFTPFailure as failure:
        try:
            if sftpfailure_follow_symlinks:
                stat = _utils.async_to_sync(path._client.sftp.stat(path._path))
            else:
                stat = _utils.async_to_sync(path._client.sftp.lstat(path._path))
            filetype = stat.type
        except (_ssh.SFTPNoSuchPath, _ssh.SFTPNoSuchFile):
            filetype = _ssh.FILEXFER_TYPE_UNKNOWN
        sftpfailure = sftpfailure or _sftpfailure
        error = sftpfailure(path, failure, filetype)
        if not error:
            error = Exception(path, failure, filetype)
        raise error


def chmod(path: "Path", mode: int, *, follow_symlinks=True):
    if follow_symlinks:
        return _syncsftp(path._client.sftp.chmod, path, mode)
    else:
        raise NotImplementedError("lchmod")


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


def exists(path: "Path"):
    return _syncsftp(path._client.sftp.exists, path)


def is_block_device(path: "Path"):
    type = _syncsftp(path._client.sftp._type, path)
    return type == _ssh.FILEXFER_TYPE_BLOCK_DEVICE


def is_char_device(path: "Path"):
    type = _syncsftp(path._client.sftp._type, path)
    return type == _ssh.FILEXFER_TYPE_CHAR_DEVICE


def is_dir(path: "Path"):
    type = _syncsftp(path._client.sftp._type, path)
    return type == _ssh.FILEXFER_TYPE_DIRECTORY


def is_fifo(path: "Path"):
    type = _syncsftp(path._client.sftp._type, path)
    return type == _ssh.FILEXFER_TYPE_FIFO


def is_file(path: "Path"):
    type = _syncsftp(path._client.sftp._type, path)
    return type == _ssh.FILEXFER_TYPE_REGULAR


def is_socket(path: "Path"):
    type = _syncsftp(path._client.sftp._type, path)
    return type == _ssh.FILEXFER_TYPE_SOCKET


def is_symlink(path: "Path"):
    try:
        return (
            _syncsftp(path._client.sftp.lstat, path).type == _ssh.FILEXFER_TYPE_SYMLINK
        )
    except FileNotFoundError as _e:
        return False


def iterdir(path: "Path"):
    for file in _syncsftp(path._client.sftp.listdir, path):
        yield path / file


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


def readlink(path: "Path"):
    return path._with_path(_syncsftp(path._client.sftp.readlink, path))


def rename(path: "Path", target):
    return _syncsftp(path._client.sftp.rename, path, target)


def rmdir(path: "Path"):
    return _syncsftp(path._client.sftp.rmdir, path)


def resolve(path: "Path", strict=False):
    sftpfile = _syncsftp(
        path._client.sftp.realpath, path, check=_ssh.FXRP_STAT_IF_EXISTS
    )
    if strict and sftpfile.attrs.type == _ssh.FILEXFER_TYPE_UNKNOWN:
        raise FileNotFoundError(path)
    return path._with_path(sftpfile.filename)


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


def stat(path: "Path", *, follow_symlinks=True):
    if follow_symlinks:
        stat = _syncsftp(path._client.sftp.stat, path)
    else:
        stat = _syncsftp(path._client.sftp.lstat, path)
    return _stat(
        [
            getattr(stat, _STATMAP.get(field, field.removeprefix("st_")), None)
            for field in _utils.STAT_FIELDS
        ]
    )


def symlink_to(path: "Path", target: "Path", target_is_directory=False):
    return _syncsftp(
        path._client.sftp.symlink, path._with_path(target), path, sftpfailure_path_pos=1
    )


def unlink(path: "Path", missing_ok=False):
    try:
        return _syncsftp(path._client.sftp.unlink, path)
    except FileNotFoundError as e:
        if not missing_ok:
            raise e


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
