"""Filesystem paths for a :class:`~pytruenas.TrueNASClient`.

``client.path(...)`` returns a `pathlib_next` path:

* **local** client (running on the NAS) -> a plain
  :class:`pathlib_next.LocalPath` (no extra dependencies);
* **remote** client -> a :class:`~pytruenas.fs.truenas.TruenasPath`, which
  prefers SFTP and falls back to the middleware ``filesystem.*`` websocket API
  (:class:`~pytruenas.fs.tnasws.TnasWsPath`).

The old bespoke multi-backend ``Path`` proxy is gone; these are real
`pathlib_next` path types, so every generic operation (``read_bytes``/``walk``/
``glob``/``copy``/...) comes from `pathlib_next` for free.
"""

from __future__ import annotations

import typing as _ty

from pathlib_next import LocalPath as LocalPath

from ._uri import quote_uri_path as _quote_uri_path
from .tnasws import TnasWsBackend as TnasWsBackend
from .tnasws import TnasWsPath as TnasWsPath
from .truenas import TruenasPath as TruenasPath

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient

__all__ = ["LocalPath", "TnasWsPath", "TnasWsBackend", "TruenasPath", "path"]


def path(client: "TrueNASClient", *segments, backend: "str | None" = None):
    """Build the appropriate path type for ``client`` and ``segments``.

    ``backend`` forces a specific type: ``"local"`` -> :class:`LocalPath`,
    ``"ws"``/``"api"`` -> :class:`TnasWsPath`, ``"truenas"``/``"auto"`` ->
    :class:`TruenasPath`. Default (``None``/``"auto"``): ``LocalPath`` for a local
    client, otherwise ``TruenasPath``.
    """
    backend = backend or "auto"
    posix = "/".join(str(s) for s in segments) if segments else "/"

    if backend == "local" or (backend == "auto" and _settings(client).is_local):
        return LocalPath(*segments) if segments else LocalPath("/")

    ws_backend = TnasWsBackend(client)
    if backend in ("ws", "api"):
        return TnasWsPath(_ws_uri(client, posix), backend=ws_backend)
    return TruenasPath(_truenas_uri(client, posix), backend=ws_backend)


def _settings(client: "TrueNASClient"):
    """The object carrying ``host``/``is_local`` for ``client``.

    A ``TrueNASHost`` keeps them on ``_config``; the pre-hostctl client kept
    them on ``_api``. Both spellings are accepted because this module is
    reached from both directions -- the path providers pass a host, while
    ``client.path()`` callers may hold either. Reading the wrong one raised
    ``AttributeError`` deep inside URI construction, which is a long way from
    the cause.
    """
    for name in ("_config", "_api"):
        settings = getattr(client, name, None)
        if settings is not None:
            return settings
    return client


def _host(client: "TrueNASClient") -> str:
    return getattr(_settings(client), "host", None) or "localhost"


def _ws_uri(client: "TrueNASClient", posix: str) -> str:
    return f"truenas+ws://{_host(client)}{_uri_path(posix)}"


def _truenas_uri(client: "TrueNASClient", posix: str) -> str:
    return f"truenas://{_host(client)}{_uri_path(posix)}"


def _uri_path(posix: str) -> str:
    """``posix`` as the absolute, percent-encoded path component of a URI.

    Both path types here are ``UriPath``s: they parse the string built above
    and uridecode it. Interpolated raw, a ``?`` or ``#`` in a filename began a
    query or fragment and truncated the path *at construction* --
    ``client.path("/mnt/tank/cache?v=2")`` yielded a path pointing at
    ``/mnt/tank/cache`` before any transport leg was chosen, so the websocket
    leg (``read_bytes``, ``stat``, every ``filesystem.*`` call) addressed the
    wrong file just as the SFTP one did, with no error either way.
    """
    return _quote_uri_path(_abspath(posix))


def _abspath(posix: str) -> str:
    return posix if posix.startswith("/") else "/" + posix
