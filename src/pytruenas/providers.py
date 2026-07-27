"""``hostctl`` providers for a TrueNAS middleware target.

Two adapters, both deliberately thin -- they own *connection* behaviour only,
and leave operating-system semantics to :class:`hostctl.host.PosixHost`:

* :class:`TnasWsPathProvider` -- paths served by the middleware
  ``filesystem.*`` API, wrapping the existing
  :class:`~pytruenas.fs.tnasws.TnasWsBackend`.
* :class:`MiddlewareExecutorProvider` -- command execution over the local
  middleware unix socket.

**On ordering.** A host composes these *after* the SSH providers, so SSH keeps
the preference it has today. That reproduces
:class:`~pytruenas.fs.truenas.TruenasPath`'s hand-rolled "try SFTP, fall back to
the websocket" behaviour using hostctl's selector, which additionally records a
redacted trace of what was tried and why (``host.last_selection``).

**On honesty.** ``probe()`` here reports what the transport can *actually* do
rather than what would be convenient. The **JSON-RPC endpoint** is not a general
command channel: it exposes ``filesystem.*`` and friends, not arbitrary exec
(verified on 26.0.0-BETA.1 -- of 781 methods only ``core.resize_shell`` and
``user.shell_choices`` are shell-adjacent, and the former merely resizes an
already-open session). So :class:`MiddlewareExecutorProvider` declares itself
available only where it genuinely is -- on the NAS itself, via the unix socket
-- and declines everywhere else, letting the selector fall through to SSH.
Claiming otherwise would turn a clean "no executor available" into a confusing
runtime failure halfway through a command.

That limitation belongs to the *JSON-RPC endpoint*, not to ``middlewared`` as a
whole: it also serves ``/_shell``, a separate websocket app running a real PTY
login shell, which is how the web UI's Shell page executes commands. Closing the
remote-without-SSH gap (a host reachable on the API port but not on 22 -- NAT,
firewall, reverse proxy) means adding a provider for *that* endpoint; the
protocol is specified in ``.agents/plans/hostctl_host_migration.md`` step 10.
"""

from __future__ import annotations

import typing as _ty

from hostctl.provider import (
    ExecutorProvider as _ExecutorProvider,
    OperationNotStarted as _OperationNotStarted,
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

        # A local target is served straight off the filesystem: going through
        # the middleware for a path on the same machine adds a websocket
        # round-trip, and `filesystem.get` routes reads through the HTTP side
        # channel, which cannot reach a unix-socket client at all.
        backend = "local" if self._is_local else "ws"
        return _make(self._client, *segments, backend=backend)

    @property
    def _is_local(self) -> bool:
        config = getattr(self.client, "config", None)
        if config is not None and hasattr(config, "is_local"):
            return bool(config.is_local)
        api = getattr(self._client, "_api", None)
        return bool(getattr(api, "is_local", False))

    def probe(self) -> _ProviderProbe:
        return _ProviderProbe("available", capabilities=self.capabilities)


class MiddlewareExecutorProvider(_ExecutorProvider):
    """Command execution over the local middleware unix socket.

    Usable only when this process runs *on* the NAS. The middleware websocket
    exposes no arbitrary-exec method, so there is nothing to dispatch remotely;
    rather than pretend, :meth:`probe` reports ``unavailable`` off-box and
    :meth:`connect` raises :class:`~hostctl.provider.OperationNotStarted` so the
    selector cleanly falls through to the next executor (SSH).

    ``OperationNotStarted`` is the right signal specifically because nothing was
    dispatched: hostctl only retries the next provider when a provider proves it
    started no work, which is what makes the fallback safe to do automatically.
    """

    def __init__(self, client: "TrueNASClient") -> None:
        self.client = client
        self._executor = None
        # ``args`` matters: without it hostctl renders the whole invocation to
        # one string (``/bin/sh -c 'printf hi'``) and hands it over as a single
        # command, which ``subprocess`` then looks up as one literal filename
        # and fails with FileNotFoundError. Declaring ``args`` makes the shell
        # flavour split the invocation into a real argv instead.
        super().__init__(
            "middleware", self._execute, capabilities=("cwd", "env", "args")
        )

    @property
    def _is_local(self) -> bool:
        # A TrueNASHost carries `.config`; a bare client carries the parsed
        # target as `._api`. Accept either, since the host builds this provider
        # with itself before its client exists.
        config = getattr(self.client, "config", None)
        if config is not None and hasattr(config, "is_local"):
            return bool(config.is_local)
        api = getattr(self.client, "_api", None)
        return bool(getattr(api, "is_local", False))

    def probe(self) -> _ProviderProbe:
        if not self._is_local:
            return _ProviderProbe(
                "unavailable",
                reason=(
                    "the middleware API exposes no remote command execution; "
                    "use SSH for a remote host"
                ),
            )
        return _ProviderProbe("available", capabilities=self.capabilities)

    def connect(self) -> None:
        if not self._is_local:
            raise _OperationNotStarted(
                "middleware executor is local-only; no command was dispatched"
            )

    def _execute(self, command: object, *args: object, **options: object):
        if not self._is_local:
            # Belt and braces: the selector should never route here, but a
            # direct caller must not get a silently wrong result.
            raise _OperationNotStarted(
                "middleware executor is local-only; no command was dispatched"
            )
        # Delegate to hostctl's own local executor rather than calling
        # subprocess here. It already owns input normalization against the
        # stream mode, the extended capture_output convention, and the
        # stdin/input conflict check -- reimplementing those is exactly how the
        # bytes-input deadlock got reintroduced once already.
        from hostctl.executor import LocalExecutor

        if self._executor is None:
            self._executor = LocalExecutor()
        return self._executor(command, *args, **_ty.cast(_ty.Any, options))


__all__ = [
    "MiddlewareExecutorProvider",
    "TnasWsPathProvider",
    "WS_PATH_CAPABILITIES",
]
