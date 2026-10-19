"""Filesystem paths for a :class:`~pytruenas.TrueNASClient`.

``client.path(...)`` is the one constructor: hostctl's composite path, which
routes each operation to this host's path providers in order and falls through
to the next when one cannot serve the call. For a remote host that is ``sftp``
(over the host's own SSH connection) then ``tnasws``; for the local socket it is
a plain local path. ``client.path(..., backend="tnasws")`` pins the websocket
leg.

This package holds the ``tnasws`` provider's path type,
:class:`~pytruenas.fs.tnasws.TnasWsPath`, a real ``pathapi`` path, so every
generic operation (``read_bytes``/``walk``/``glob``/``copy``/...) comes from
``pathapi``.
"""

from __future__ import annotations

from .tnasws import TnasWsBackend as TnasWsBackend
from .tnasws import TnasWsPath as TnasWsPath

__all__ = ["TnasWsPath", "TnasWsBackend"]
