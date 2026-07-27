"""``hostctl`` providers for a TrueNAS middleware target.

Only **one** adapter is TrueNAS-specific: :class:`TnasWsPathProvider`, paths
served by the middleware ``filesystem.*`` API. It is deliberately thin -- it
owns *connection* behaviour only, and leaves operating-system semantics to
:class:`hostctl.host.PosixHost`.

Local execution needs no adapter at all: :func:`local_providers` returns
hostctl's stock pair. A target reached over the middleware unix socket *is*
this machine, so a command there is a plain ``subprocess`` call and a path is a
plain local path -- there is nothing about TrueNAS to add.

**On ordering** (see ``TrueNASHost._build_providers``):

``local`` -> ``ssh`` -> ``webshell``, and ``local`` -> ``sftp`` -> ``tnasws``.

Local comes first because reaching this machine through SSH, a PTY, or the
filesystem API would be slower and strictly less capable; it is only built when
the target is local, and everything after it is a way of reaching a machine
somewhere else. Among the remote options SSH wins on capability, which also
reproduces :class:`~pytruenas.fs.truenas.TruenasPath`'s hand-rolled "try SFTP,
fall back to the websocket" behaviour -- now through hostctl's selector, which
additionally records a redacted trace of what was tried and why
(``host.last_selection``).

**On honesty.** ``probe()`` reports what a transport can *actually* do rather
than what would be convenient. The JSON-RPC endpoint is not a general command
channel: it exposes ``filesystem.*`` and friends, not arbitrary exec (verified
on 26.0.0-BETA.1 -- of 781 methods only ``core.resize_shell`` and
``user.shell_choices`` are shell-adjacent, and the former merely resizes an
already-open session). That limitation belongs to the JSON-RPC endpoint, not to
``middlewared`` as a whole: it also serves the PTY behind
``/websocket/shell``, which :mod:`pytruenas.webshell` drives to give a
remote host without SSH a real command channel.
"""

from __future__ import annotations

import typing as _ty

from hostctl.provider import (
    ExecutorProvider as _ExecutorProvider,
    PathProvider as _PathProvider,
    ProviderProbe as _ProviderProbe,
)

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from pathlib_next import Path

    from . import TrueNASClient


#: Path operations the middleware ``filesystem.*`` API can actually serve.
#: Deliberately narrower than ``PathProvider.DEFAULT_CAPABILITIES``: the
#: websocket API has no symlink creation, no rename, and no realpath, which is
#: precisely why ``TruenasPath`` prefers SFTP for those. Declaring them here
#: would make the selector choose this provider for operations it cannot do.
WS_PATH_CAPABILITIES = frozenset(
    (
        "stat",
        "scandir",
        "open",
        "open_read",
        "open_write",
        "read",
        "write",
        "exists",
        "is_file",
        "is_dir",
        "mkdir",
        "chmod",
        "unlink",
        "rmdir",
    )
)


class TnasWsPathProvider(_PathProvider):
    """Paths served by the middleware ``filesystem.*`` websocket API.

    Always available for a connected client -- the middleware socket *is* the
    client's own connection, so there is no separate transport to fail. It is
    ordered after SFTP because its operation surface is narrower, not because it
    is less reliable.
    """

    def __init__(self, client: "TrueNASClient") -> None:
        self.client = client
        super().__init__(
            "tnasws",
            self._make_path,
            capabilities=WS_PATH_CAPABILITIES,
        )

    @property
    def _client(self):
        """The client whose websocket serves these paths.

        A ``TrueNASHost`` passes *itself* here (the two are built together, and
        the client is created lazily from the host's config), so unwrap it:
        ``pytruenas.fs.path`` needs the client, not the host.
        """
        client = self.client
        host_client = getattr(client, "client", None)
        return host_client if host_client is not None else client

    def _make_path(self, *segments: object) -> "Path":
        from .fs import path as _make

        # Always the websocket backend. A *local* target is served by hostctl's
        # own local path provider, which the host orders ahead of this one --
        # so there is no local case left to special-case here.
        return _make(self._client, *segments, backend="ws")

    def probe(self) -> _ProviderProbe:
        return _ProviderProbe("available", capabilities=self.capabilities)


def local_providers():
    """hostctl's stock local executor and path providers.

    A target reached over the middleware unix socket *is* this machine, so a
    command there is a plain ``subprocess`` call and a path is a plain local
    path. hostctl already provides both, and this is the same one-liner its own
    ``system.py:_local_provider`` uses -- there is nothing TrueNAS-specific to
    add, so pytruenas does not define a provider class for it.

    (There was one. It wrapped ``LocalExecutor`` behind an ``is_local`` guard
    and called itself ``MiddlewareExecutorProvider``, which was doubly
    misleading: nothing about the dispatch involved ``middlewared``, and the
    guard only duplicated the decision the caller had already made by choosing
    to build it.)
    """
    from hostctl.executor import LocalExecutor
    from pathlib_next import Path as _LocalPath

    return (
        _ExecutorProvider("local", LocalExecutor()),
        _PathProvider("local", lambda *parts: _LocalPath(*parts)),
    )


__all__ = [
    "TnasWsPathProvider",
    "WS_PATH_CAPABILITIES",
    "local_providers",
]
