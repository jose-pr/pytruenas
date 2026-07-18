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

    if backend == "local" or (backend == "auto" and client._api.is_local):
        return LocalPath(*segments) if segments else LocalPath("/")

    ws_backend = TnasWsBackend(client)
    if backend in ("ws", "api"):
        return TnasWsPath(_ws_uri(client, posix), backend=ws_backend)
    return TruenasPath(_truenas_uri(client, posix), backend=ws_backend)


def _host(client: "TrueNASClient") -> str:
    return getattr(client._api, "host", None) or "localhost"


def _ws_uri(client: "TrueNASClient", posix: str) -> str:
    return f"truenas+ws://{_host(client)}{_abspath(posix)}"


def _truenas_uri(client: "TrueNASClient", posix: str) -> str:
    return f"truenas://{_host(client)}{_abspath(posix)}"


def _abspath(posix: str) -> str:
    return posix if posix.startswith("/") else "/" + posix
