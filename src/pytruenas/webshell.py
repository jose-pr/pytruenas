"""Command execution over the TrueNAS web-shell endpoint.

Reached at ``/websocket/shell`` (nginx), which proxies to ``/_shell`` on the
middleware's own port -- see :data:`WEBSHELL_PATH` for why that distinction
costs an afternoon if you get it wrong.

This is the executor for a host reachable on the API port but **not** on 22 --
NAT without a forwarded SSH port, a firewall allowing only 443, an appliance
behind a reverse proxy. Such a host otherwise has no ``run()`` at all: the
JSON-RPC API exposes no remote command execution (of 781 methods on
26.0.0-BETA.1 only ``core.resize_shell`` and ``user.shell_choices`` are
shell-adjacent, and the former only resizes an already-open session).

``middlewared`` serves ``/_shell`` as a *separate* websocket app beside the RPC
socket -- a sibling of ``/_upload`` and ``/_download``, which pytruenas already
uses. It is what the web UI's Shell page drives, so a command channel
demonstrably exists wherever the API does.

Protocol (verified against 26.0.0-BETA.1):

1. Open a websocket to ``/websocket/shell``.
2. Receive ``{"msg": "connected", "id": "<uuid>"}``.
3. Send **one JSON frame** ``{"token": ..., "options": {}}``. The token comes
   from ``auth.generate_token``; the server validates it via
   ``auth.get_token_for_shell_application``, which requires a token with no
   attributes and a user holding the ``web_shell`` privilege.
4. Every frame after that is raw PTY bytes, both directions.

Server-side it is ``os.forkpty()`` + ``os.execve("/usr/bin/login", ...)``: a
real interactive login shell (zsh for root on TrueNAS), not a request/response
API. **Input must be sent as BINARY frames** -- a text frame reaches
``os.write(master_fd, ...)`` as ``str``, the writer thread dies, and the
connection resets with no error message.

A command runs through that terminal with
:class:`hostctl.console.PosixConsoleProfile`: the command and any ``input=``
are typed base64-encoded inside fixed shell syntax, output is framed by markers
the shell prints (never by the echo), stdin is a temporary file or
``/dev/null``, and stderr and the exit status come back in their own frames.
:class:`WebShellExecutor` is hostctl's :class:`hostctl.console.ConsoleExecutor`
over that websocket, which gives it hostctl's ``subprocess``-shaped call
surface with stdout delivered as it arrives.

A command that exits the shell (``exit 3``) ends the session; the next call
reconnects. This provider ranks after SSH, whose separate channels need none of
the above.
"""

from __future__ import annotations

import json as _json
import re as _re
import threading as _threading
import typing as _ty

from hostctl.console import (
    ConsoleExecutor as _ConsoleExecutor,
    PosixConsoleProfile as _PosixConsoleProfile,
)
from hostctl.exceptions import OperationNotStartedError as _OperationNotStartedError
from hostctl.executor import ExecutorRequest as _ExecutorRequest
from hostctl.provider import (
    ExecutorProvider as _ExecutorProvider,
    ProviderProbe as _ProviderProbe,
    ProviderSelector as _ProviderSelector,
)

from .host import TrueNASClient

#: Terminal escape sequences a PTY emits around real output.
_ANSI = _re.compile(
    rb"\x1b\[[0-9;?]*[a-zA-Z]"
    rb"|\x1b\](?:[^\x1b\x07]|\x1b(?!\\))*(?:\x07|\x1b\\)"
    rb"|\x1b[=>]"
)

#: The interactive prompt a login shell prints (``root@HOST[~]#``).
_PROMPT = _re.compile(rb"[^\s@]+@[^\s\[]*\[[^\]]*\][#$] ?")

#: How long to wait for the login banner to settle after authenticating. Only
#: to catch a token rejection before the first command: output is framed.
_SETTLE = 1.0

#: Opening the websocket and authenticating must not hang forever.
CONNECT_TIMEOUT = 30.0

#: Longest one write may block. The socket has one timeout for both
#: directions, and a read just before may have left it at a millisecond, which
#: fails a send that waits for the server to drain typed input.
_WRITE_TIMEOUT = 30.0

#: The **externally reachable** web-shell path. ``middlewared`` registers the
#: handler at ``/_shell`` on its internal port; nginx exposes it as
#: ``/websocket/shell``. Connecting to ``/_shell`` on 443 does not fail cleanly
#: -- nginx serves the web UI there with a 200, ``websocket-client`` follows the
#: redirect, and rejects the ``https://`` target with ``ValueError: scheme https
#: is invalid``.
WEBSHELL_PATH = "/websocket/shell"

#: The framed protocol. zsh, TrueNAS root's login shell, reads it as sh does.
#: No acknowledged batches: the middleware keeps reading the terminal, and a
#: websocket send blocks rather than overflowing the terminal's input queue.
_PROFILE = _PosixConsoleProfile(batch=None)


def clean_output(data: bytes) -> str:
    """Render raw PTY bytes as text: escape sequences, prompts and CRs removed.

    A display helper for bytes read OUTSIDE a command's frame (a banner, an
    interactive session). Command output is never passed through it: what
    :class:`WebShellExecutor` returns is the program's own bytes.
    """
    data = _PROMPT.sub(b"", _ANSI.sub(b"", data)).replace(b"\r", b"")
    return data.decode("utf-8", "replace")


class _WebSocketStream:
    """The web shell's websocket as a :class:`hostctl.console.ConsoleStream`."""

    def __init__(self, ws: _ty.Any) -> None:
        self._ws = ws
        #: Bytes received but not yet read: a frame may exceed `size`.
        self._pending = bytearray()

    def read(self, size: int = -1, *, timeout: "_ty.Optional[float]" = None) -> bytes:
        if not self._pending:
            # websocket-client reads 0 as non-blocking, which raises rather
            # than returning empty; a millisecond keeps "only what is there".
            self._ws.settimeout(None if timeout is None else max(timeout, 0.001))
            try:
                data = self._ws.recv()
            except Exception as exc:
                if type(exc).__name__ == "WebSocketTimeoutException":
                    return b""
                raise ConnectionError(
                    f"web shell connection lost: {type(exc).__name__}"
                ) from exc
            if isinstance(data, str):
                data = data.encode("utf-8", "surrogateescape")
            if not data and not getattr(self._ws, "connected", True):
                raise ConnectionError("web shell connection closed")
            self._pending += data
        count = len(self._pending) if size is None or size < 0 else size
        chunk = bytes(self._pending[:count])
        del self._pending[:count]
        return chunk

    def write(self, data: bytes) -> None:
        # Binary frames only: see the module docstring.
        self._ws.settimeout(_WRITE_TIMEOUT)
        try:
            self._ws.send_binary(bytes(data))
        except OSError:
            raise
        except Exception as exc:
            raise ConnectionError(
                f"web shell connection lost: {type(exc).__name__}"
            ) from exc


class WebShellSession:
    """One authenticated ``/_shell`` websocket running a login shell."""

    def __init__(
        self, client: "TrueNASClient", *, options: "_ty.Optional[dict]" = None
    ):
        self.client = client
        self.options = options or {}
        self._ws = None
        self._stream: "_ty.Optional[_WebSocketStream]" = None
        #: Guards opening and closing; never held while a command runs, so a
        #: timed-out command's session can be closed from another thread.
        self._lock = _threading.RLock()
        self.shell_id: "_ty.Optional[str]" = None

    # -- connection --------------------------------------------------------

    def _uri(self) -> str:
        target = self.client._http_target(WEBSHELL_PATH)
        scheme = "wss" if target.scheme == "https" else "ws"
        return target._replace(scheme=scheme).uri

    def connect(self):
        """Open and authenticate the session; idempotent."""
        with self._lock:
            if self._ws is not None:
                return self._ws
            try:
                import websocket as _websocket
            except ImportError as exc:  # pragma: no cover - dependency present
                raise ImportError("the web shell requires websocket-client") from exc

            from . import _tls

            # The same trust as the API websocket -- see pytruenas._tls.
            ws = _websocket.WebSocket(sslopt=_tls.sslopt(self.client.config.verify))
            ws.connect(self._uri(), timeout=CONNECT_TIMEOUT)
            try:
                self._authenticate(ws)
            except BaseException:
                # A failed token, or a refusal of any shape, left the
                # websocket open.
                ws.close()
                raise
            self._ws = ws
            self._stream = _WebSocketStream(ws)
            return ws

    def _authenticate(self, ws: _ty.Any) -> None:
        # match_origin=True, single_use=True: the middleware's own default
        # for the first is True. This token is handed straight to a
        # websocket opened here, from this machine, exactly once.
        token = self.client.api.auth.generate_token(60, {}, True, True)
        ws.send(_json.dumps({"token": token, "options": self.options}))

        # Catch a rejected token before the first command; the banner that
        # follows a good one is simply outside every command's frame.
        ws.settimeout(_SETTLE)
        while True:
            try:
                frame = ws.recv()
            except Exception:
                break
            if not isinstance(frame, str):
                continue
            try:
                message = _json.loads(frame)
            except ValueError:
                continue
            if not isinstance(message, dict):
                continue
            if message.get("msg") == "connected":
                self.shell_id = message.get("id")
            elif message.get("msg") == "failed":
                error = message.get("error")
                reason = error.get("reason") if isinstance(error, dict) else error
                raise _OperationNotStartedError(
                    f"web shell rejected the token: {reason or 'unknown'}"
                )
        if self.shell_id is None:
            raise _OperationNotStartedError(
                "web shell sent no 'connected' message: the endpoint closed or "
                "stayed silent after the token"
            )

    @property
    def stream(self) -> _WebSocketStream:
        """The session's terminal as a console stream; connects first."""
        with self._lock:
            self.connect()
            return _ty.cast(_WebSocketStream, self._stream)

    def close(self) -> None:
        with self._lock:
            ws, self._ws = self._ws, None
            self._stream = None
            self.shell_id = None
            if ws is not None:
                try:
                    ws.close()
                except Exception:
                    pass

    def _drop(self, stream: "_ty.Optional[_WebSocketStream]") -> None:
        """Close the session if ``stream`` is still its terminal.

        A newer session that replaced it stays open.
        """
        with self._lock:
            if stream is not None and self._stream is stream:
                self.close()


class WebShellExecutor(_ConsoleExecutor):
    """``run()`` over the web shell: :class:`hostctl.console.ConsoleExecutor`.

    Each command takes the provider's session, connecting it first; a
    connection that fails is a decline, so the host tries its next provider.
    No ``args``, ``cwd`` or ``env``: the terminal takes one line of shell
    text, which hostctl renders. A timeout or a failure closes the session,
    whose hang-up ends the command (``TimeoutExpired.orphaned`` is False);
    the next command reconnects.
    """

    def __init__(self, provider: "WebShellExecutorProvider") -> None:
        self._provider = provider
        super().__init__(self._open, profile=_PROFILE)

    def _open(self) -> _WebSocketStream:
        self._provider.connect()
        return self._provider.session.stream

    def _abandon(self, request: _ExecutorRequest, *, stream: object = None) -> bool:
        # The base types ^C best effort; closing the session is what ends the
        # command either way.
        super()._abandon(request, stream=stream)
        session = self._provider._session
        if session is not None:
            session._drop(stream)
        return False


class WebShellExecutorProvider(_ExecutorProvider):
    """Executor for hosts reachable on the API port but not over SSH."""

    def __init__(self, client: "TrueNASClient"):
        self.client = client
        self._session: "_ty.Optional[WebShellSession]" = None
        # No `args`: the terminal takes one line of shell text, so hostctl
        # renders the whole invocation to a single string rather than an argv.
        super().__init__("webshell", WebShellExecutor(self), capabilities=())

    # -- lifecycle ---------------------------------------------------------

    @property
    def session(self) -> WebShellSession:
        if self._session is None:
            self._session = WebShellSession(self.client)
        return self._session

    def probe(self) -> _ProviderProbe:
        """Report availability without dispatching a command.

        A local target has the unix socket and does not need this.
        """
        config = getattr(self.client, "config", None)
        if config is not None and getattr(config, "is_local", False):
            return _ProviderProbe(
                "unavailable", reason="local target uses the middleware socket"
            )
        return _ProviderProbe("available", capabilities=self.capabilities)

    def connect(self) -> None:
        """Open the session; a failure is a decline naming its cause."""
        try:
            self.session.connect()
        except _OperationNotStartedError:
            raise
        except Exception as exc:
            raise _OperationNotStartedError(
                f"web shell unavailable: {type(exc).__name__}: "
                f"{_ProviderSelector.redact(exc)}",
                cause=exc,
            ) from exc

    def close(self) -> None:
        if self._session is not None:
            self._session.close()
            self._session = None


__all__ = [
    "WebShellExecutor",
    "WebShellExecutorProvider",
    "WebShellSession",
    "clean_output",
]
