"""``TruenasPath`` -- a remote TrueNAS path that prefers SFTP, falls back to the
middleware ``filesystem.*`` websocket API.

A remote TrueNAS host can be reached two ways: over SSH/SFTP (rich POSIX
semantics -- symlinks, rename, recursive remove) when a shell is configured, or
over the middleware websocket (:class:`~pytruenas.fs.tnasws.TnasWsPath`), which is
always available but exposes a narrower ``filesystem.*`` surface. ``TruenasPath``
composes the two: five operations -- ``unlink``, ``rmdir``, ``rename``,
``symlink_to`` and ``readlink`` -- are tried on the SFTP leg first and fall back
to the websocket leg when SFTP is unavailable or does not implement it.
``resolve`` goes to the SFTP leg too, and returns ``self`` unchanged when there
is none: the middleware has no ``realpath``.

The SFTP leg is an :class:`sftppath.SFTPPath` over ``asyncssh`` (the ``ssh``
extra); without the extra this is the websocket leg alone.
Construct via :meth:`~pytruenas.TrueNASClient.path`.
"""

from __future__ import annotations

import typing as _ty

from .tnasws import TnasWsPath as _TnasWsPath

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient

_FTYPE = _ty.Literal["file", "link", "directory"]


def _sftp_path_cls():
    """Return ``sftppath.SFTPPath`` if importable, else ``None``.

    Kept lazy so importing this module never requires the SFTP extra; the caller
    treats ``None`` as "no SFTP leg -- websocket only".
    """
    try:
        from sftppath import SFTPPath
    except ImportError:
        return None
    return SFTPPath


class TruenasPath(_TnasWsPath):
    """Remote TrueNAS path: SFTP-preferred, websocket-``filesystem.*`` fallback.

    Subclasses :class:`~pytruenas.fs.tnasws.TnasWsPath` so the always-available
    websocket backend is the base behaviour; the SFTP-preferred operations
    (unlink/rmdir/rename/symlink_to/readlink/resolve) are overridden to try
    SFTP first. Carries the same
    ``TnasWsBackend`` (holding the client); the SFTP leg is built lazily from
    the host's SSH configuration (``client.config.ssh``, an
    :class:`hostctl.SSHConfig`).
    """

    __SCHEMES = ("truenas",)
    __slots__ = ()

    # -- SFTP leg ----------------------------------------------------------

    def _ssh_config(self):
        """The client's :class:`hostctl.SSHConfig`, or ``None``.

        The SSH leg lives on the host's config (``client.config.ssh``) since
        ``TrueNASClient`` was merged into ``TrueNASHost``. This used to read
        ``client.ssh_config`` and then ``client.shell``; neither carries the
        SSH target on a real host anymore -- ``ssh_config`` was removed with
        the merge and ``client.shell`` is hostctl's bound ``Shell``, which has
        no ``host`` -- so the whole SFTP leg was unreachable.
        """
        client = self.backend.client
        config = getattr(client, "config", None)
        if config is None:
            config = getattr(client, "_config", client)
        return getattr(config, "ssh", None)

    def _sftp(self):
        """Build an ``SFTPPath`` for this path from the client's ssh config, or None.

        Returns ``None`` when sftppath is unavailable or the client has no
        usable SSH target -- callers then use the websocket leg.
        """
        sftp_cls = _sftp_path_cls()
        if sftp_cls is None:
            return None
        ssh = self._ssh_config()
        host = getattr(ssh, "host", None)
        if not host:
            return None
        # Reuse the client's asyncssh connect options (key/password/known_hosts)
        # so the SFTP leg authenticates -- and checks the host key -- the same
        # way the client's own ssh channel does. Without asyncssh (no `ssh`
        # extra) there is no backend, and callers use the websocket leg.
        backend = _sftp_backend(self.backend.client, ssh)
        if backend is None:
            return None
        # `self.path` is the decoded name and `SFTPPath` takes a plain path,
        # not a URI, so it is passed as it is: `?`, `#` and `%` are filename
        # characters on this leg.
        return sftp_cls(self.path, backend=backend)

    def _try_sftp(self, op: str, *args, **kwargs):
        """Run ``op`` on the SFTP leg.

        Raises ``_NoSftp`` if there is no SFTP leg, and ``NotImplementedError`` if
        the SFTP path type does not implement ``op`` -- callers treat both as
        "fall back to the websocket leg".
        """
        sftp = self._sftp()
        if sftp is None:
            raise _NoSftp()
        method = getattr(sftp, op, None)
        if method is None:
            raise NotImplementedError(f"SFTP backend has no {op!r}")
        return method(*args, **kwargs)

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

    def _on_this_host(self, target) -> bool:
        """Whether a rename destination is on this path's host.

        A ``str`` names a path on this host. A path object must be a
        ``TnasWsPath`` for the same host: renaming hands the SFTP leg only the
        destination's PATH, so any other target would be renamed on THIS host
        under that name -- the file leaves the source, never reaches the
        destination, and no error is raised.
        """
        if isinstance(target, str):
            return True
        return isinstance(target, _TnasWsPath) and self._same_filesystem(target)

    def _rename_compatible(self, target) -> bool:
        # `move()` asks this first and copies + deletes when it is False.
        return self._on_this_host(target)

    def rename(self, target):
        if not self._on_this_host(target):
            raise NotImplementedError(
                f"cannot rename across hosts ({self} -> {target}); use move()"
            )
        try:
            moved = self._try_sftp("rename", _as_posix(target))
        except (_NoSftp, NotImplementedError):
            raise NotImplementedError("rename requires the SFTP backend")
        # Return the new path on THIS host, as pathlib does -- not the SFTP
        # leg's own path object, which carries a private per-call backend.
        return self.with_segments(_as_posix(moved if moved is not None else target))

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
        callback consulted before each removal. Not part of ``pathapi`` -- kept
        from the original pytruenas API. The link itself is created via the SFTP
        leg (``filesystem.*`` has no symlink op), so a host with no SFTP leg
        raises ``NotImplementedError`` -- and raises it *before* ``force``
        removes anything, so a call that cannot succeed leaves the existing
        target alone rather than deleting it and then failing.
        """
        # Resolve the creating leg up front. Building it is local (no network),
        # and doing it here is what keeps the force-removal below from running
        # on a host that has no way to create the replacement link.
        sftp = self._sftp()
        create = getattr(sftp, "symlink_to", None) if sftp is not None else None
        if create is None:
            raise NotImplementedError("symlink_to requires the SFTP backend")

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
                kind = (
                    "directory"
                    if self.is_dir()
                    else "file" if self.is_file() else "unknown"
                )
                if kind not in allowed:
                    raise FileExistsError(self)
                if onremove(self, kind):
                    self.rm(recursive=True, missing_ok=True)
        return create(_as_posix(target), target_is_directory)

    def resolve(self, strict=False):
        """This path with every symlink replaced, over SFTP; else ``self``.

        The SFTP leg resolves the way ``pathapi`` does, by reading each link.
        Without one the path is returned unchanged: the middleware has no
        ``realpath``, so the websocket leg cannot see through a link.
        """
        try:
            resolved = self._try_sftp("resolve", strict=strict)
        except (_NoSftp, NotImplementedError):
            return self
        return self.with_segments(_as_posix(resolved))


class _NoSftp(Exception):
    """Internal: signals that no SFTP leg is available for a fallback op."""


def _as_posix(value: object) -> str:
    """Best-effort POSIX path string for a URI/path/str target."""
    for attr in ("path", "as_posix"):
        candidate = getattr(value, attr, None)
        if callable(candidate):
            return candidate()
        if isinstance(candidate, str):
            return candidate
    return str(value)


def _sftp_backend(client: object, ssh: object):
    """One SFTP backend per client, or ``None`` without the ``ssh`` extra.

    Cached on the client because a backend owns its connection: a fresh
    backend per call opens a new SSH session for every operation. hostctl
    caches one backend per transport for the same reason.

    The cache is invalidated when the SSH settings change, so
    ``install_sshcreds()`` (which rewrites them) cannot leave a backend
    authenticating with the previous credentials; the replaced backend is
    closed.
    """
    try:
        from sftppath import AsyncSSHBackend
    except ImportError:
        return None
    host = ssh.host
    port = getattr(ssh, "port", 0) or 22
    connect_opts = _connect_opts_from_ssh(ssh)
    # A dict is not hashable and asyncssh options are not comparable by
    # identity, so the key is the rendered settings.
    key = repr((host, port, sorted((str(k), repr(v)) for k, v in connect_opts.items())))
    cached = getattr(client, "_sftp_backend_cache", None)
    if cached is not None and cached[0] == key:
        return cached[1]
    backend = AsyncSSHBackend(
        host, port, user=connect_opts.get("username"), connect_opts=connect_opts
    )
    try:
        client._sftp_backend_cache = (key, backend)  # type: ignore[attr-defined]
    except Exception:
        # A client stand-in that refuses attributes (a Mock with spec, a
        # frozen object): work uncached rather than fail the operation.
        pass
    else:
        if cached is not None:
            _close_backend(cached[1])
    return backend


def _close_backend(backend: object) -> None:
    """Close a replaced SFTP backend's connections; never raises."""
    close = getattr(backend, "close", None)
    if callable(close):
        try:
            close()
        except Exception:  # pragma: no cover - teardown must not raise
            pass


def _connect_opts_from_ssh(ssh) -> "dict":
    """asyncssh connect options for an :class:`hostctl.SSHConfig`.

    Delegates to ``SSHConfig.connect_opts()`` -- the single source of truth the
    host's own SSH executor and SFTP path provider both use -- so this leg
    authenticates *and applies the host-key policy* exactly the way
    ``client.run()`` does. Do not hand-copy fields here: a copied list is how
    a ``known_hosts`` policy reaches one leg and not the other.

    ``connect_opts()`` always carries ``known_hosts`` (``()`` checks
    ``~/.ssh/known_hosts``, ``None`` opts out) and ``config`` (``None`` unless
    the ``SSHConfig`` names an ssh_config), and every key it emits is an
    ``asyncssh.connect()`` keyword, which ``AsyncSSHBackend`` forwards as given.

    The pre-hostctl ``"client_keys|root"`` username packing is unpacked once,
    in :func:`pytruenas.host._ssh_config_from`, on the way into the config --
    it never reaches here.
    """
    return dict(ssh.connect_opts())
