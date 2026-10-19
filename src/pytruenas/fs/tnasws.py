"""``TnasWsPath`` -- a URI path backed by the TrueNAS middleware.

The TrueNAS ``filesystem.*`` websocket API is a genuine filesystem accessible
only through the middleware connection, so ``TnasWsPath`` is a
:class:`uripath.URIPath` whose **backend** holds the
:class:`~pytruenas.TrueNASClient`. Path I/O is implemented by calling
``client.api.filesystem.<op>`` (``stat``/``mkdir``/``get``/``put``/
``chown``/...); no path library has an equivalent, which is why this backend
stays custom while local and SFTP paths are ``pathapi``'s and ``sftppath``'s.

Construct one through :meth:`~pytruenas.TrueNASClient.path` (which threads the
client in via the backend); a ``TnasWsPath`` built from a bare URI with no client
backend raises a clear error on the first I/O call.
"""

from __future__ import annotations

import errno as _errno
import io as _io
import os as _os
import stat as _stat
import typing as _ty

from pathapi import FileStat as _FileStat
from pathapi.providers import CommitOnClose as _CommitOnClose
from uripath import URIPath as _URIPath

from ..connection import ClientException as _ClientException
from ..namespace import ioerror as _ioerror

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient

#: URI scheme(s) that resolve to :class:`TnasWsPath`. Not a real network scheme --
#: just a registration handle so the ``URIPath`` machinery + backend propagation
#: work; the connection lives on the backend, not in the URI.
_SCHEME = "truenas+ws"

#: ``filesystem.listdir`` query options, one per caller.
#:
#: An unrestricted ``listdir`` computes every column of
#: ``FilesystemDirQueryResultItem``, and one of them -- ``zfs_attrs`` -- is
#: ZFS-only. On a non-ZFS filesystem the middleware does not return the ``null``
#: its own schema promises for that case; it fails the whole call with
#: ``EFAULT ... ZFS attributes are not supported.``. So every listing operation
#: (``iterdir``/``glob``/``walk``/``rglob``) raised on ``/tmp``, ``/var/tmp``,
#: ``/dev``, ``/proc``, ``/sys`` and any other non-pool mount, while ``stat`` and
#: ``read_bytes`` on the very same paths worked.
#:
#: Projecting with ``select`` fixes it at the source: an unrequested column is
#: never computed, so a single code path serves ZFS and non-ZFS alike -- no
#: error-string sniffing and no second round trip. Each caller asks for exactly
#: what it consumes, so neither pulls a column in on the other's behalf.
#:
#: Measured on 26.0.0-BETA.1: ``zfs_attrs`` is the *only* column that fails on a
#: non-ZFS path, and ``mtime`` is not a ``listdir`` column at all (it is absent
#: from the result schema and from every entry, on ZFS too) -- which is why the
#: stat projection does not ask for it and seeded stats carry ``st_mtime`` 0
#: here exactly as they always did. ``stat()`` uses ``filesystem.stat``, a
#: different call that does report ``mtime``, and is unaffected.
_LISTDIR_NAME_ONLY = {"select": ["name"]}

#: ``_scandir`` seeds each child's stat from the listing, so it needs everything
#: :func:`_stat_from_info` reads: ``mode`` (the full ``st_mode``), ``size``, and
#: ``type`` as the coarse fallback for an entry that reports no ``mode``.
_LISTDIR_STAT = {"select": ["name", "type", "size", "mode"]}


class TnasWsBackend:
    """Backend state for :class:`TnasWsPath`: it just holds the client.

    Mirrors the role of an SFTP backend (which holds an SSH connection); here
    the "connection" is the middleware
    :class:`~pytruenas.TrueNASClient`, whose ``api.filesystem`` namespace does the
    actual work.
    """

    __slots__ = ("client",)

    def __init__(self, client: "TrueNASClient") -> None:
        self.client = client


class TnasWsPath(_URIPath):
    """A path on a TrueNAS host, served by the middleware ``filesystem.*`` API."""

    __SCHEMES = (_SCHEME,)
    __slots__ = ()

    #: The path component names a real file *on the TrueNAS host*, so
    #: ``os.fspath()`` and ``host_fspath()`` may return it. Without this,
    #: fspath raises for this scheme and anything building a command line that
    #: names the file -- a `chmod`, a `systemctl` argument -- has to unwrap the
    #: URI by hand. It stays false for schemes whose path is not a filesystem
    #: path (`http`, `s3`), which is what the opt-in exists to distinguish.
    _host_filesystem_path = True

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

    def _host_client(self):
        """The client this path talks to, or ``None`` for a bare-URI path."""
        return getattr(getattr(self, "_backend", None), "client", None)

    def _same_filesystem(self, other) -> bool:
        """Whether ``other`` names files on the same TrueNAS host.

        uripath's default compares supplied backend objects, and
        ``fs.path()`` gives every path its own backend -- so two spellings of
        one file on one host read as two trees, and its same-file guard never
        fired: ``move(overwrite=True)`` onto a second ``fs.path()`` for the same
        file deleted it. The host is what the backend talks to: the same client,
        or clients for the same (credential-free) connection URI.
        """
        mine, theirs = self._host_client(), other._host_client()
        if mine is None or theirs is None:
            return super()._same_filesystem(other)
        if mine is theirs:
            return True
        uri = getattr(mine, "connection_uri", None)
        return isinstance(uri, str) and uri == getattr(theirs, "connection_uri", None)

    # -- stat / listing ----------------------------------------------------

    def stat(self, *, follow_symlinks=True) -> "_FileStat":
        hint = self._pop_stat_hint()
        if hint is not None and not follow_symlinks:
            return hint
        info = self._fs.stat(self.path, _ioerror=True)
        return _stat_from_info(info)

    def _listdir(self):
        for entry in self._fs.listdir(self.path, [], _LISTDIR_NAME_ONLY, _ioerror=True):
            yield entry["name"]

    def _scandir(self):
        # listdir returns metadata per entry in one round trip, so seed each
        # child's stat (lstat-like: symlinks unresolved) to avoid a stat() each.
        for entry in self._fs.listdir(self.path, [], _LISTDIR_STAT, _ioerror=True):
            yield entry["name"], _stat_from_info(entry)

    # -- open / read / write ----------------------------------------------

    def _open(self, mode="r", buffering=-1):
        # Per the BinaryOpen contract, ``open()`` strips the ``b`` before calling
        # ``_open`` and always expects a BINARY stream back (it wraps text
        # itself). So ``mode`` here is one of ``r``/``w``/``a`` (+ maybe ``+``).
        if "r" in mode and "+" not in mode:
            return _io.BytesIO(self._read_bytes())
        if mode.rstrip("+") in ("w", "a"):
            append = mode.startswith("a")
            # One `filesystem.put` when the stream closes; a `with` block that
            # raises discards the buffer, so a failed write uploads nothing.
            return _CommitOnClose(
                lambda buffer: self._write_bytes(buffer.getvalue(), append=append)
            )
        raise NotImplementedError(mode)

    def _read_bytes(self) -> bytes:
        try:
            data = self._fs.get(self.path, _filetransfer=True)
        except _ClientException as error:
            raise _oserror(_ioerror(error), self.path) from error
        return _ty.cast(bytes, data)

    def _write_bytes(
        self, data: bytes, *, append: bool = False, mode: "int | None" = None
    ):
        opts: dict = {"append": bool(append)}
        if mode is not None:
            opts["mode"] = mode
        self._fs.put(self.path, opts, _filetransfer=bytes(data), _ioerror=True)
        return len(data)

    # -- mutation ----------------------------------------------------------

    def mkdir(self, mode=None, parents=False, exist_ok=False):
        """Create this directory; ``mode`` defaults to ``0o755``.

        pathlib's ``0o777`` default is safe only because the kernel masks it
        with the process umask. The middleware applies the mode it is sent
        verbatim (measured live: a default ``mkdir()`` made a ``0o777``
        directory), so the conventional ``022`` umask is applied here. An
        explicit ``mode`` is sent as given.
        """
        mode = 0o777 & ~0o022 if mode is None else mode
        return super().mkdir(mode, parents=parents, exist_ok=exist_ok)

    def _mkdir(self, mode):
        self._fs.mkdir(
            {"path": self.path, "options": {"mode": oct(mode)}}, _ioerror=True
        )

    def chmod(self, mode, *, follow_symlinks=True):
        # filesystem.setperm takes an octal-ish mode string.
        self._job(
            self._fs.setperm,
            {"path": self.path, "mode": oct(mode)[2:], "options": {"recursive": False}},
        )

    def chown(
        self,
        uid=None,
        gid=None,
        *,
        follow_symlinks=True,
        recursive=False,
        traverse=True,
    ):
        if uid == -1:
            uid = None
        if gid == -1:
            gid = None
        if not follow_symlinks:
            raise NotImplementedError("chown(follow_symlinks=False)")
        self._job(
            self._fs.chown,
            {
                "path": self.path,
                "uid": uid,
                "gid": gid,
                "options": {"recursive": recursive, "traverse": traverse},
            },
        )

    def _job(self, method, *params):
        """Run a ``filesystem.*`` method that is a middleware job, to its end.

        Returns once the change is made; a failed job raises ``OSError`` (the
        matching subclass when the middleware names an errno).
        """
        try:
            return method(*params, job=True, _ioerror=True)
        except _ClientException as error:
            raise _oserror(error, self.path) from error

    def unlink(self, missing_ok=False):
        """Remove this file or link; a directory raises ``IsADirectoryError``.

        The ``filesystem.*`` API has no deletion, so this runs ``rm`` on the
        host. A failure is re-read with ``filesystem.stat`` to raise the
        ``OSError`` subclass pathlib would.
        """
        done = self.backend.client.run(("rm", "--", self.path), check=False)
        if done.returncode == 0:
            return
        try:
            info = self._fs.stat(self.path, _ioerror=True)
        except FileNotFoundError:
            if missing_ok:
                return
            raise
        if (info.get("type") or "").upper() == "DIRECTORY":
            raise _error(_errno.EISDIR, self.path)
        raise _command_error(done, self.path)

    def rmdir(self):
        """Remove this empty directory, as ``rmdir`` on the host does.

        Raises ``FileNotFoundError``, ``NotADirectoryError``, or ``OSError``
        with ``ENOTEMPTY`` when it has entries.
        """
        done = self.backend.client.run(("rmdir", "--", self.path), check=False)
        if done.returncode == 0:
            return
        info = self._fs.stat(self.path, _ioerror=True)
        if (info.get("type") or "").upper() != "DIRECTORY":
            raise _error(_errno.ENOTDIR, self.path)
        error = _command_error(done, self.path)
        if error.errno == _errno.EIO and any(self._listdir()):
            raise _error(_errno.ENOTEMPTY, self.path)
        raise error


#: What ``rm``/``rmdir`` print for the errors a caller branches on. Only a
#: fallback: a missing path or a wrong type is decided by ``filesystem.stat``.
_STDERR_ERRNO = {
    "Permission denied": _errno.EACCES,
    "Operation not permitted": _errno.EPERM,
    "Read-only file system": _errno.EROFS,
    "Directory not empty": _errno.ENOTEMPTY,
    "Device or resource busy": _errno.EBUSY,
}


def _error(code: int, path: str) -> OSError:
    """The ``OSError`` subclass for ``code``, as the OS would raise it."""
    return OSError(code, _os.strerror(code), path)


def _command_error(done, path: str) -> OSError:
    """An ``OSError`` for a failed ``rm``/``rmdir`` of ``path``."""
    stderr = done.stderr or b""
    if isinstance(stderr, bytes):
        stderr = stderr.decode(errors="replace")
    for text, code in _STDERR_ERRNO.items():
        if text in stderr:
            return _error(code, path)
    message = stderr.strip() or f"{done.args!r} exited {done.returncode}"
    return OSError(_errno.EIO, message, path)


def _oserror(error: Exception, path: str) -> OSError:
    """``error`` as an ``OSError`` about ``path``; one already is, unchanged."""
    if isinstance(error, OSError):
        return error
    return OSError(getattr(error, "errno", None) or _errno.EIO, str(error), path)


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
