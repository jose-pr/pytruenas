"""Filesystem paths for a :class:`~pytruenas.TrueNASClient`.

``client.path(...)`` is hostctl's composite path: it routes each operation to
this host's path providers in order and falls through to the next when one
cannot serve the call. For a remote host that is ``sftp`` (over the host's own
SSH connection) then ``tnasws``; for the local socket it is a plain local path.

The path types behind it, for a caller building one directly or reading the
provider table:

* **local** client (running on the NAS) -> :class:`pathapi.LocalPath`;
* the middleware ``filesystem.*`` API -> :class:`~pytruenas.fs.tnasws.TnasWsPath`,
  the ``tnasws`` provider's path type.
* ``pytruenas.fs.path(client, *segments, backend=...)`` builds one of these;
  its ``backend=`` vocabulary (``"local"``/``"ws"``/``"api"``/``"truenas"``/
  ``"auto"``) is NOT the provider-name vocabulary ``client.path(backend=...)``
  takes.

These are real ``pathapi`` path types, so every generic operation
(``read_bytes``/``walk``/``glob``/``copy``/...) comes from ``pathapi``.
"""

from __future__ import annotations

import posixpath as _posixpath
import typing as _ty

from hostctl import uri_host as _uri_host
from pathapi import LocalPath as LocalPath

from .tnasws import _SCHEME
from .tnasws import TnasWsBackend as TnasWsBackend
from .tnasws import TnasWsPath as TnasWsPath

if _ty.TYPE_CHECKING:
    from pathapi import Path

    from .. import TrueNASClient

__all__ = ["LocalPath", "TnasWsPath", "TnasWsBackend", "path", "symlink_to"]

_FTYPE = _ty.Literal["file", "link", "directory"]


def path(client: "TrueNASClient", *segments, backend: "str | None" = None):
    """Build the path type for ``client`` and ``segments``.

    ``backend`` chooses it: ``"local"`` -> :class:`LocalPath`, ``"ws"``/
    ``"api"`` -> :class:`TnasWsPath`, ``"truenas"`` -> ``client.path(...)``
    (the composite path over the host's providers, rooted at ``/``). Default
    (``None``/``"auto"``): ``LocalPath`` for a local client, otherwise
    ``client.path(...)``. Another value raises ``ValueError``.
    """
    backend = backend or "auto"
    # Joined as the composite path joins: an absolute segment restarts the
    # path, so every leg names the same file.
    posix = _posixpath.join(*(str(s) for s in segments)) if segments else "/"

    if backend == "local" or (backend == "auto" and _settings(client).is_local):
        return LocalPath(*segments) if segments else LocalPath("/")
    if backend in ("ws", "api"):
        # `with_path` percent-encodes the name into the URI and `.path` decodes
        # it back, so a `?`, `#` or `%` in a filename stays part of the name.
        root = TnasWsPath(
            f"{_SCHEME}://{_uri_host(_host(client))}/", backend=TnasWsBackend(client)
        )
        return root.with_path(_abspath(posix))
    if backend in ("truenas", "auto"):
        # The host's own path rather than `CompositePosixPath.over(...)`: a
        # selector built per call forgets the host's declines, so a refused
        # SSH port would be dialled again for every path.
        return client.path(_abspath(posix))
    raise ValueError(
        f"unknown path backend: {backend!r} (local, ws, api, truenas, auto)"
    )


def symlink_to(
    path: "Path",
    target: object,
    target_is_directory: bool = False,
    *,
    force: "bool | _FTYPE | _ty.Sequence[_FTYPE]" = False,
    onremove: "_ty.Callable[[_ty.Any, str], bool] | None" = None,
):
    """Make ``path`` a symlink to ``target``, replacing a conflicting entry.

    Works on any ``pathapi`` path: ``client.path(...)``, a ``LocalPath``.
    ``force`` removes an existing entry first: ``True`` any kind, or the kinds
    named (``"file"``, ``"link"``, ``"directory"``; a directory is removed
    recursively); another kind raises ``FileExistsError``. ``onremove(path,
    kind)`` is asked before each removal, and a false answer keeps the entry.

    Raises ``NotImplementedError`` -- before removing anything -- when no leg of
    ``path`` can create a symlink: the middleware ``filesystem.*`` API has
    none, so a host without SFTP cannot.
    """
    from pathapi.protocols import Symlink, supports

    if not supports(path, Symlink):
        raise NotImplementedError(f"{path}: no leg of this path can create a symlink")
    if force and (path.exists() or path.is_symlink()):
        onremove = onremove or (lambda _p, _t: True)
        if force is True:
            allowed = set(_ty.get_args(_FTYPE))
        elif isinstance(force, str):
            allowed = {force}
        else:
            allowed = set(force)
        if path.is_symlink():
            kind = "link"
        elif path.is_dir():
            kind = "directory"
        else:
            kind = "file" if path.is_file() else "unknown"
        if kind not in allowed:
            raise FileExistsError(path)
        if onremove(path, kind):
            if kind == "directory":
                path.rm(recursive=True, missing_ok=True)
            else:
                path.unlink()
    return path.symlink_to(_as_posix(target), target_is_directory)


def _as_posix(value: object) -> str:
    """The POSIX path string of a ``str``, a URI path or any path object."""
    if isinstance(value, str):
        return value
    uri_path = getattr(value, "path", None)
    if isinstance(uri_path, str):
        return uri_path
    as_posix = getattr(value, "as_posix", None)
    return as_posix() if callable(as_posix) else str(value)


def _settings(client: "TrueNASClient"):
    """The object carrying ``host``/``is_local`` for ``client``.

    A ``TrueNASHost`` keeps them on ``_config``; the pre-hostctl client kept
    them on ``_api``. Both spellings are accepted because this module is
    reached from both directions -- the path providers pass a host, while
    ``client.path()`` callers may hold either.
    """
    for name in ("_config", "_api"):
        settings = getattr(client, name, None)
        if settings is not None:
            return settings
    return client


def _host(client: "TrueNASClient") -> str:
    return getattr(_settings(client), "host", None) or "localhost"


def _abspath(posix: str) -> str:
    return posix if posix.startswith("/") else "/" + posix
