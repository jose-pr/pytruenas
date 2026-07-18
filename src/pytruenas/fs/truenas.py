"""``TruenasPath`` -- a remote TrueNAS path that prefers SFTP, falls back to the
middleware ``filesystem.*`` websocket API.

A remote TrueNAS host can be reached two ways: over SSH/SFTP (rich POSIX
semantics -- symlinks, rename, recursive remove) when a shell is configured, or
over the middleware websocket (:class:`~pytruenas.fs.tnasws.TnasWsPath`), which is
always available but exposes a narrower ``filesystem.*`` surface. ``TruenasPath``
composes the two: each operation is tried on the SFTP leg first and falls back to
the websocket leg when SFTP is unavailable or does not implement it.

The SFTP leg is pluggable. When ``pathlib_next``'s ``SftpPath`` is importable
(the ``sftp``/``sftp-async`` extra -- see pathlib_next 0.8.2 which made this work
asyncssh-only), it is used; otherwise this falls back to the websocket leg alone.
Construct via :meth:`~pytruenas.TrueNASClient.path`.
"""

from __future__ import annotations

import typing as _ty

from .tnasws import TnasWsBackend as _TnasWsBackend
from .tnasws import TnasWsPath as _TnasWsPath

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient

_FTYPE = _ty.Literal["file", "link", "directory"]

#: Operations delegated to the SFTP leg first (falling back to the websocket leg).
#: Everything else runs on the websocket leg directly (stat/open/read/write/mkdir/
#: chown are all first-class there). These are the ops SFTP does better or that the
#: ``filesystem.*`` API does not offer (delete, symlink, rename, resolve).
_SFTP_FIRST = frozenset(
    {"unlink", "rmdir", "rename", "symlink_to", "readlink", "resolve", "rm"}
)


def _sftp_path_cls():
    """Return pathlib_next's ``SftpPath`` if importable, else ``None``.

    Kept lazy so importing this module never requires the SFTP extra; the caller
    treats ``None`` as "no SFTP leg -- websocket only".
    """
    try:
        from pathlib_next.uri.schemes.sftp import SftpPath
    except ImportError:
        return None
    return SftpPath


class TruenasPath(_TnasWsPath):
    """Remote TrueNAS path: SFTP-preferred, websocket-``filesystem.*`` fallback.

    Subclasses :class:`~pytruenas.fs.tnasws.TnasWsPath` so the always-available
    websocket backend is the base behaviour; the SFTP-preferred operations
    (:data:`_SFTP_FIRST`) are overridden to try SFTP first. Carries the same
    ``TnasWsBackend`` (holding the client); the SFTP leg is built lazily from the
    client's shell/ssh configuration.
    """

    __SCHEMES = ("truenas",)
    __slots__ = ()

    # -- SFTP leg ----------------------------------------------------------

    def _sftp(self):
        """Build an ``SftpPath`` for this path from the client's ssh config, or None.

        Returns ``None`` when pathlib_next's SFTP is unavailable or the client has
        no usable shell target -- callers then use the websocket leg.
        """
        sftp_cls = _sftp_path_cls()
        if sftp_cls is None:
            return None
        client = self.backend.client
        shell = getattr(client, "shell", None)
        host = getattr(shell, "host", None)
        if not host:
            return None
        port = getattr(shell, "port", 0) or 22
        # Reuse the client's asyncssh connect options (key/password) so the SFTP
        # leg authenticates the same way the client's own ssh channel does.
        connect_opts = _connect_opts_from_shell(shell)
        from pathlib_next.uri.schemes.sftp import AsyncsshSftpBackend

        backend = AsyncsshSftpBackend(connect_opts=connect_opts)
        return sftp_cls(f"sftp://{host}:{port}{self.path}", backend=backend)

    def _try_sftp(self, op: str, *args, **kwargs):
        """Run ``op`` on the SFTP leg; raise ``_NoSftp`` if there is no SFTP leg."""
        sftp = self._sftp()
        if sftp is None:
            raise _NoSftp()
        return getattr(sftp, op)(*args, **kwargs)

    # -- delegated operations ---------------------------------------------

    def unlink(self, missing_ok=False):
        try:
            return self._try_sftp("unlink", missing_ok=missing_ok)
        except (_NoSftp, NotImplementedError):
            return super().unlink(missing_ok=missing_ok)

    def rmdir(self):
        try:
            return self._try_sftp("rmdir")
        except (_NoSftp, NotImplementedError):
            return super().rmdir()

    def rename(self, target):
        try:
            return self._try_sftp("rename", _as_posix(target))
        except (_NoSftp, NotImplementedError):
            raise NotImplementedError("rename requires the SFTP backend")

    def readlink(self):
        try:
            link = self._try_sftp("readlink")
        except (_NoSftp, NotImplementedError):
            raise NotImplementedError("readlink requires the SFTP backend")
        return self.with_segments(_as_posix(link))

    def symlink_to(
        self,
        target,
        target_is_directory=False,
        *,
        force: "bool | _FTYPE | _ty.Sequence[_FTYPE]" = False,
        onremove: "_ty.Callable[[_ty.Any, str], bool] | None" = None,
    ):
        """Create a symlink, with pytruenas's ``force=`` convenience.

        ``force`` removes a conflicting existing target first (a bool, a single
        file-type, or a set of file-types that may be replaced); ``onremove`` is a
        callback consulted before each removal. Not part of pathlib_next -- kept
        from the original pytruenas API. The link itself is created via the SFTP
        leg (``filesystem.*`` has no symlink op).
        """
        if force and (self.exists() or self.is_symlink()):
            onremove = onremove or (lambda _p, _t: True)
            if force is True:
                allowed = set(_ty.get_args(_FTYPE))
            elif isinstance(force, str):
                allowed = {force}
            else:
                allowed = set(force)
            if self.is_symlink():
                if "link" not in allowed:
                    raise FileExistsError(self)
                if onremove(self, "link"):
                    self.unlink()
            else:
                kind = "directory" if self.is_dir() else "file" if self.is_file() else "unknown"
                if kind not in allowed:
                    raise FileExistsError(self)
                if onremove(self, kind):
                    self.rm(recursive=True, missing_ok=True)
        try:
            return self._try_sftp("symlink_to", _as_posix(target), target_is_directory)
        except (_NoSftp, NotImplementedError):
            raise NotImplementedError("symlink_to requires the SFTP backend")

    def resolve(self, strict=False):
        try:
            resolved = self._try_sftp("resolve", strict=strict)
        except (_NoSftp, NotImplementedError):
            # No SFTP: the middleware has no realpath; return self unchanged
            # (best effort, matching a filesystem with no symlink resolution).
            return self
        return self.with_segments(_as_posix(resolved))


class _NoSftp(Exception):
    """Internal: signals that no SFTP leg is available for a fallback op."""


def _as_posix(value: object) -> str:
    """Best-effort POSIX path string for a Uri/Path/str target."""
    for attr in ("path", "as_posix"):
        candidate = getattr(value, attr, None)
        if callable(candidate):
            return candidate()
        if isinstance(candidate, str):
            return candidate
    return str(value)


def _connect_opts_from_shell(shell) -> "dict":
    """Map the client's shell target to asyncssh connect options."""
    opts: "dict[str, object]" = {}
    username = getattr(shell, "username", "") or ""
    password = getattr(shell, "password", None)
    if "|" in username:
        logintype, user = username.split("|", maxsplit=1)
    else:
        logintype, user = "password", username or "root"
    opts["username"] = user or "root"
    if password:
        if logintype == "client_keys":
            opts["client_keys"] = [password.encode() if isinstance(password, str) else password]
        else:
            opts["password"] = password
    return opts
