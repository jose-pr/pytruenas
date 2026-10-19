"""``hostctl`` providers for a TrueNAS middleware target.

Only **one** adapter is TrueNAS-specific: :class:`TnasWsPathProvider`, paths
served by the middleware ``filesystem.*`` API. It is deliberately thin -- it
owns *connection* behaviour only, and leaves operating-system semantics to
:class:`hostctl.host.PosixHost`.

Local execution needs no adapter at all: :func:`local_providers` returns
hostctl's stock pair (:func:`hostctl.local_providers`). A target reached over the middleware unix socket *is*
this machine, so a command there is a plain ``subprocess`` call and a path is a
plain local path -- there is nothing about TrueNAS to add.

**On ordering** (see ``TrueNASClient.default_providers``):

``local`` -> ``ssh`` -> ``webshell``, and ``local`` -> ``sftp`` -> ``tnasws``.

Local comes first because reaching this machine through SSH, a PTY, or the
filesystem API would be slower and strictly less capable; it is only built when
the target is local, and everything after it is a way of reaching a machine
somewhere else. Among the remote options SSH wins on capability; hostctl's
selector falls back to the websocket when SFTP cannot serve, and records a
redacted trace of what was tried and why (``host.last_selection``).

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

from hostctl.provider import (
    PathProvider as _PathProvider,
    ProviderProbe as _ProviderProbe,
)

from pathapi import Path

from .host import TrueNASClient

#: Path operations the middleware ``filesystem.*`` API can actually serve.
#: Deliberately narrower than ``PathProvider.DEFAULT_CAPABILITIES``: the
#: websocket API has no symlink creation, no rename, and no realpath, which is
#: why the host's composite path routes those to SFTP. Declaring them here
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

    def _make_path(self, *segments: object) -> "Path":
        from .fs.tnasws import _for_host

        # The plain websocket path: the host's composite path routes what this
        # provider cannot do (rename, symlinks, resolve) to `sftp` itself.
        return _for_host(self.client, *segments)

    def probe(self) -> _ProviderProbe:
        return _ProviderProbe("available", capabilities=self.capabilities)


def local_providers():
    """hostctl's stock local executor and path providers.

    A target reached over the middleware unix socket *is* this machine, so a
    command there is a plain ``subprocess`` call and a path is a plain local
    path. This is :func:`hostctl.local_providers` unchanged: there is nothing
    TrueNAS-specific to add, so pytruenas defines no provider class for it.
    Returns a fresh ``(executor_provider, path_provider)`` pair, both named
    ``"local"``.
    """
    from hostctl import local_providers as _local_providers

    return _local_providers()


__all__ = [
    "TnasWsPathProvider",
    "WS_PATH_CAPABILITIES",
    "local_providers",
]
