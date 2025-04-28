import typing as _ty
from os import stat_result as _stat
import io as _io

from .. import _utils

if _ty.TYPE_CHECKING:
    from . import Path
    import _typeshed


def stat(path: "Path"):
    stat = path._client.api.filesystem.stat(path.as_posix(), _ioerror=True)
    return _stat(
        [
            stat.get(field.removeprefix("st_"))
            for field in _utils.STAT_FIELDS  # type:ignore
        ]
    )


def chown(
    path: "Path",
    uid: int | None,
    gid: int | None,
    *,
    follow_symlinks: bool = True,
    recursive=False,
    traverse=True
):
    if uid == -1:
        uid = None
    if gid == -1:
        gid = None

    if not follow_symlinks:
        raise NotImplementedError("not follow_symlinks")
    path._client.api.filesystem.chown(
        {
            "options": {"recursive": recursive, "traverse": traverse},
            "uid": uid,
            "gid": gid,
            "path": path.as_posix(),
        },
        _ioerror=True,
    )


def mkdir(path: "Path", mode: int = 511, parents=False, exist_ok=False):
    try:
        path._client.api.filesystem.mkdir(
            {"path": path.as_posix(), "options": {"mode": oct(mode)}}, _ioerror=True
        )
    except FileExistsError as e:
        if not exist_ok:
            raise e
    except FileNotFoundError as e:
        if not parents:
            raise e
        mkdir(path.parent, mode, parents)


def open(
    path: "Path",
    mode: _ty.Literal["rb"] | _ty.Literal["wb"] | _ty.Literal["ab"],
    buffering=-1,
):
    if mode not in ["rb", "wb", "ab"]:
        raise NotImplementedError(mode)
    if buffering != -1:
        pass
    if mode == "rb":
        return _io.BytesIO(_read(path))
    else:
        return _ApiFileHandle(path, mode == "ab")


class _ApiFileHandle(_io.IOBase):
    def __init__(self, file: "Path", append: bool):
        super().__init__()
        self._buffer = bytearray()
        self.file = file
        self.append = append

    def readable(self):
        return False

    def seekable(self):
        return False

    def writable(self):
        return True

    def write(self, data):
        if not _utils.isbytelike(data):
            raise TypeError("argument must be a bytes-like object")
        self._buffer.extend(data)
        return len(data)

    def flush(self):
        pass

    def close(self):
        if self.closed:
            return
        _write(self.file, self._buffer, append=self.append)
        return super().close()


def _read(path: "Path"):
    data = path._client.api.filesystem.get(
        path.as_posix(), _filetransfer=True, _ioerror=True
    )
    return _ty.cast(bytes, data)


def _write(
    path: "Path",
    data: "_typeshed.ReadableBuffer|_ty.IO|bytes",
    append=False,
    mode: int | None = None,
):
    if hasattr(data, "read"):
        _data: bytes = _ty.cast(_ty.IO, data).read()
    elif not isinstance(data, bytes):
        _data = bytes(data)
    else:
        _data = data
    opts: dict = {"append": not not append}
    if mode is not None:
        opts["mode"] = mode
    result = path._client.api.filesystem.put(
        path.as_posix(),
        opts,  # type:ignore
        _filetransfer=_data,
        _ioerror=True,
    )
    if result:
        return len(_data)
