"""``TnasWsPath`` -- a pathlib_next URI path backed by the TrueNAS middleware.

The TrueNAS ``filesystem.*`` websocket API is a genuine filesystem accessible
only through the middleware connection, so -- exactly like ``SftpPath`` carries an
SFTP backend -- ``TnasWsPath`` is a :class:`~pathlib_next.uri.UriPath` whose
**backend** holds the :class:`~pytruenas.TrueNASClient`. Path I/O is implemented
by calling ``client.api.filesystem.<op>`` (``stat``/``mkdir``/``get``/``put``/
``chown``/...); there is no equivalent in pathlib_next, which is why this backend
stays custom while local/sftp delegate to pathlib_next's own path types.

Construct one through :meth:`~pytruenas.TrueNASClient.path` (which threads the
client in via the backend); a ``TnasWsPath`` built from a bare URI with no client
backend raises a clear error on the first I/O call.
"""

from __future__ import annotations

import io as _io
import stat as _stat
import typing as _ty

from pathlib_next.uri import UriPath as _UriPath
from pathlib_next.utils.stat import FileStat as _FileStat

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient

#: URI scheme(s) that resolve to :class:`TnasWsPath`. Not a real network scheme --
#: just a registration handle so the ``UriPath`` machinery + backend propagation
#: work; the connection lives on the backend, not in the URI.
_SCHEME = "truenas+ws"


class TnasWsBackend:
    """Backend state for :class:`TnasWsPath`: it just holds the client.

    Mirrors the role of ``SftpBackend``/``AsyncsshSftpBackend`` (which hold an
    SSH/SFTP connection); here the "connection" is the middleware
    :class:`~pytruenas.TrueNASClient`, whose ``api.filesystem`` namespace does the
    actual work.
    """

    __slots__ = ("client",)

    def __init__(self, client: "TrueNASClient") -> None:
        self.client = client


class TnasWsPath(_UriPath):
    """A path on a TrueNAS host, served by the middleware ``filesystem.*`` API."""

    __SCHEMES = (_SCHEME,)
    __slots__ = ()

    # -- backend / client access -------------------------------------------

    def _initbackend(self):
        # A TnasWsPath is only useful with a client-carrying backend; one built
        # from a bare URI has none, so fail clearly rather than at a random attr.
        raise RuntimeError(
            "TnasWsPath has no TrueNAS client backend; build it via "
            "client.path(...) rather than from a bare URI"
        )

    @property
    def _fs(self):
        """The middleware ``filesystem`` API namespace for this path's client."""
        return self.backend.client.api.filesystem

    # -- stat / listing ----------------------------------------------------

    def stat(self, *, follow_symlinks=True) -> "_FileStat":
        hint = self._pop_stat_hint()
        if hint is not None and not follow_symlinks:
            return hint
        info = self._fs.stat(self.path, _ioerror=True)
        return _stat_from_info(info)

    def _listdir(self):
        for entry in self._fs.listdir(self.path, _ioerror=True):
            yield entry["name"]

    def _scandir(self):
        # listdir returns metadata per entry in one round trip, so seed each
        # child's stat (lstat-like: symlinks unresolved) to avoid a stat() each.
        for entry in self._fs.listdir(self.path, _ioerror=True):
            yield entry["name"], _stat_from_info(entry)

    # -- open / read / write ----------------------------------------------

    def _open(self, mode="r", buffering=-1):
        # Per the BinaryOpen contract, ``open()`` strips the ``b`` before calling
        # ``_open`` and always expects a BINARY stream back (it wraps text
        # itself). So ``mode`` here is one of ``r``/``w``/``a`` (+ maybe ``+``).
        if "r" in mode and "+" not in mode:
            return _io.BytesIO(self._read_bytes())
        if "w" in mode or "a" in mode:
            return _TnasWsWriteHandle(self, append="a" in mode)
        raise NotImplementedError(mode)

    def _read_bytes(self) -> bytes:
        data = self._fs.get(self.path, _filetransfer=True, _ioerror=True)
        return _ty.cast(bytes, data)

    def _write_bytes(self, data: bytes, *, append: bool = False, mode: "int | None" = None):
        opts: dict = {"append": bool(append)}
        if mode is not None:
            opts["mode"] = mode
        self._fs.put(self.path, opts, _filetransfer=bytes(data), _ioerror=True)
        return len(data)

    # -- mutation ----------------------------------------------------------

    def _mkdir(self, mode):
        self._fs.mkdir({"path": self.path, "options": {"mode": oct(mode)}}, _ioerror=True)

    def chmod(self, mode, *, follow_symlinks=True):
        # filesystem.setperm takes an octal-ish mode string.
        self._fs.setperm(
            {"path": self.path, "mode": oct(mode)[2:], "options": {"recursive": False}},
            _ioerror=True,
        )

    def chown(self, uid=None, gid=None, *, follow_symlinks=True, recursive=False, traverse=True):
        if uid == -1:
            uid = None
        if gid == -1:
            gid = None
        if not follow_symlinks:
            raise NotImplementedError("chown(follow_symlinks=False)")
        self._fs.chown(
            {
                "path": self.path,
                "uid": uid,
                "gid": gid,
                "options": {"recursive": recursive, "traverse": traverse},
            },
            _ioerror=True,
        )

    def unlink(self, missing_ok=False):
        # The middleware has no filesystem.unlink; deletion is not part of the
        # filesystem.* API. Shell out on the host (the client runs commands
        # there). In a TruenasPath the SFTP leg handles this first when
        # available; this is the API-backend fallback.
        if missing_ok and not self.exists():
            return
        self.backend.client.run(("rm", "-f", self.path))

    def rmdir(self):
        self.backend.client.run(("rmdir", self.path))


def _stat_from_info(info: "dict") -> "_FileStat":
    """Map a middleware ``filesystem.stat``/``listdir`` entry to a ``FileStat``.

    The middleware reports ``mode`` (full ``st_mode`` incl. type bits), ``size``,
    and ``mtime``; missing pieces default sanely (a directory entry from
    ``listdir`` carries ``type`` when ``mode`` is absent).
    """
    mode = info.get("mode")
    if mode is None:
        # listdir entries may carry only a coarse type.
        entry_type = (info.get("type") or "").upper()
        mode = _stat.S_IFDIR if entry_type == "DIRECTORY" else _stat.S_IFREG
    size = info.get("size") or 0
    mtime = info.get("mtime") or 0
    return _FileStat(st_mode=int(mode), st_size=int(size), st_mtime=mtime)


class _TnasWsWriteHandle(_io.IOBase):
    """A write-only binary handle that buffers, then ``filesystem.put``s on close.

    The middleware upload is a single call, so writes accumulate and flush once
    at close (matching the old ``fs/api.py`` handle).
    """

    def __init__(self, path: "TnasWsPath", append: bool) -> None:
        super().__init__()
        self._path = path
        self._append = append
        self._buffer = bytearray()

    def writable(self):
        return True

    def readable(self):
        return False

    def seekable(self):
        return False

    def write(self, data):
        self._buffer.extend(data)
        return len(data)

    def close(self):
        if self.closed:
            return
        self._path._write_bytes(bytes(self._buffer), append=self._append)
        super().close()
