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

How a command is run through a terminal without the terminal getting in the way
(:meth:`WebShellSession.execute`):

* **Nothing typed is interpreted by the line editor.** The command -- and any
  ``input=`` -- travels base64-encoded; what is typed is only ``[A-Za-z0-9+/=]``
  inside fixed shell syntax. A ``^C``, a TAB (completion), a ``!`` (history
  expansion) or a stray newline in the payload cannot escape into the shell.
* **Output is framed by markers the command prints, never by the echo.** The
  typed line spells each marker in two quoted halves (``printf %s%s "__ST"
  "<id>__"``), so only the printed output ever contains it contiguously. The
  echo of the command line, zsh's line redraws, the login banner and the prompt
  all fall outside the frame and are ignored. ``stty -opost`` turns the
  terminal's output processing off, so the bytes between the markers are
  exactly what the program wrote.
* **stdin is a file, never the terminal.** ``input=`` (and a ``stdin=`` object,
  read to EOF first) is decoded into a temporary file and redirected in; with
  no input, stdin is ``/dev/null``. Bytes typed into a terminal that the program
  does not consume are read by the SHELL as its next command line -- as root --
  so there is no way to stream stdin through it safely.
* **stderr goes to a temporary file** and is emitted after the command, in its
  own frame. It works in any POSIX login shell (no process substitution), at the
  cost that a live stderr sink receives the bytes when the command finishes.
  ``stderr=STDOUT`` merges with ``2>&1`` instead, preserving interleaving.
* **The exit status** is printed in the closing marker.

A command that exits the shell (``exit 3``) ends the session; the next call
reconnects. This provider ranks after SSH, whose separate channels need none of
the above.
"""

from __future__ import annotations

import base64 as _base64
import json as _json
import re as _re
import subprocess as _subprocess
import sys as _sys
import threading as _threading
import time as _time
import typing as _ty
import uuid as _uuid

# Both public as of hostctl 0.2.5. Sharing them is a correctness requirement,
# not a convenience: a host can dispatch the same call through different
# providers on different attempts, so an executor that handled output
# differently would return results that varied by which transport won.
from hostctl.executor import (
    capture_streams as _capture_streams,
    expired as _expired,
    write_output as _write_output,
)
from hostctl.provider import (
    ExecutorProvider as _ExecutorProvider,
    OperationNotStarted as _OperationNotStarted,
    ProviderProbe as _ProviderProbe,
)

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from . import TrueNASClient

#: Terminal escape sequences a PTY emits around real output.
_ANSI = _re.compile(
    rb"\x1b\[[0-9;?]*[a-zA-Z]"
    rb"|\x1b\](?:[^\x1b\x07]|\x1b(?!\\))*(?:\x07|\x1b\\)"
    rb"|\x1b[=>]"
)

#: The interactive prompt a login shell prints (``root@HOST[~]#``).
_PROMPT = _re.compile(rb"[^\s@]+@[^\s\[]*\[[^\]]*\][#$] ?")

#: How long to wait for the login banner to settle after authenticating. Not
#: needed for correctness any more (output is framed by markers), only to catch
#: a token rejection before the first command.
_SETTLE = 1.0

#: Opening the websocket and authenticating must not hang forever.
CONNECT_TIMEOUT = 30.0

#: Longest a single ``recv()`` blocks, so a deadline is checked even while the
#: command is silent.
_POLL = 1.0

#: Bytes to accumulate before writing to a streaming sink.
_BATCH = 4096

#: Longest a partial batch may wait before being flushed anyway.
_FLUSH_INTERVAL = 0.1

#: Longest typed line carrying base64 input. The terminal takes it one line at
#: a time; a bounded line keeps each redraw cheap.
_CHUNK = 3072

#: The **externally reachable** web-shell path. ``middlewared`` registers the
#: handler at ``/_shell`` on its internal port; nginx exposes it as
#: ``/websocket/shell``. Connecting to ``/_shell`` on 443 does not fail cleanly
#: -- nginx serves the web UI there with a 200, ``websocket-client`` follows the
#: redirect, and rejects the ``https://`` target with ``ValueError: scheme https
#: is invalid``.
WEBSHELL_PATH = "/websocket/shell"


def _send(sink: "_ty.Callable[[bytes], None] | None", data: bytes) -> None:
    if sink is not None and data:
        sink(data)


def clean_output(data: bytes) -> str:
    """Render raw PTY bytes as text: escape sequences, prompts and CRs removed.

    A display helper for bytes read OUTSIDE a command's frame (a banner, an
    interactive session). Command output is never passed through it: what
    :meth:`WebShellSession.execute` returns is the program's own bytes.
    """
    data = _PROMPT.sub(b"", _ANSI.sub(b"", data)).replace(b"\r", b"")
    return data.decode("utf-8", "replace")


def _b64(data: bytes) -> str:
    return _base64.b64encode(data).decode("ascii")


def _input_bytes(value: object, encoding: "str | None") -> bytes:
    """``input=`` as bytes: bytes-like as-is, text encoded, nothing else."""
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value)
    if isinstance(value, str):
        return value.encode(encoding or "utf-8")
    raise TypeError(
        f"input must be bytes or str, not {type(value).__name__}"
    )  # a repr of an arbitrary object is not data


def _partial(data: bytearray, marker: bytes, start: int) -> int:
    """Length of the longest suffix of ``data[start:]`` that begins ``marker``.

    Only that much has to be held back while waiting for the rest of a marker:
    holding back a whole marker's length instead delayed every short line of
    streamed output until enough later output pushed it out.
    """
    for size in range(min(len(marker) - 1, len(data) - start), 0, -1):
        if data.endswith(marker[:size]):
            return size
    return 0


class _Frame:
    """Incremental parser for one command's output on the shared PTY stream.

    ``__ST<id>__`` opens stdout, ``__OUT<id>__`` closes it (and opens stderr),
    ``__EN<id>_<rc>_EN__`` ends the command. Each marker is searched for only in
    bytes not yet scanned (plus a marker's length of overlap), so the cost is
    linear in the output rather than re-scanning the whole buffer per frame.
    """

    def __init__(self, token: str):
        self.start = f"__ST{token}__".encode()
        self.mid = f"__OUT{token}__".encode()
        self.end = _re.compile(rb"__EN" + token.encode() + rb"_(\d+)_EN__")
        self._end_prefix = b"__EN" + token.encode() + b"_"
        self.buffer = bytearray()
        self.state = "wait"  # wait -> out -> err -> done
        self.pos = 0  # where the current region starts in `buffer`
        self.scan = 0  # everything before this has been searched
        self.out = bytearray()
        self.err = bytearray()
        self.returncode: "int | None" = None

    @property
    def started(self) -> bool:
        return self.state != "wait"

    def feed(self, data: bytes) -> "tuple[bytes, bytes]":
        """Add ``data``; return the ``(stdout, stderr)`` bytes now safe to emit."""
        self.buffer += data
        out_emit = bytearray()
        err_emit = bytearray()
        while True:
            if self.state == "wait":
                hit = self.buffer.find(self.start, self.scan)
                if hit < 0:
                    self.scan = max(0, len(self.buffer) - len(self.start))
                    break
                self.state, self.pos = "out", hit + len(self.start)
                self.scan = self.pos
            elif self.state == "out":
                hit = self.buffer.find(self.mid, self.scan)
                if hit < 0:
                    safe = len(self.buffer) - _partial(self.buffer, self.mid, self.pos)
                    out_emit += self.buffer[self.pos : safe]
                    self.out += self.buffer[self.pos : safe]
                    self.pos = self.scan = safe
                    break
                out_emit += self.buffer[self.pos : hit]
                self.out += self.buffer[self.pos : hit]
                self.state, self.pos = "err", hit + len(self.mid)
                self.scan = self.pos
            elif self.state == "err":
                match = self.end.search(self.buffer, self.scan)
                if match is None:
                    # Hold back anything that could be the start of the end
                    # marker (its prefix plus the status digits).
                    tail = self.buffer.rfind(self._end_prefix, self.pos)
                    safe = (
                        tail
                        if tail >= 0
                        else len(self.buffer)
                        - _partial(self.buffer, self._end_prefix, self.pos)
                    )
                    err_emit += self.buffer[self.pos : safe]
                    self.err += self.buffer[self.pos : safe]
                    # Only the held-back tail can still hold the marker.
                    self.pos = self.scan = safe
                    break
                err_emit += self.buffer[self.pos : match.start()]
                self.err += self.buffer[self.pos : match.start()]
                self.returncode = int(match.group(1))
                self.state = "done"
                break
            else:
                break
        # Nothing before the frame is ever needed again: drop it, so the buffer
        # holds at most one marker's worth of unscanned bytes.
        if self.pos > 65536:
            del self.buffer[: self.pos]
            self.scan -= self.pos
            self.pos = 0
        return bytes(out_emit), bytes(err_emit)


class WebShellSession:
    """One authenticated ``/_shell`` websocket running a login shell."""

    def __init__(self, client: "TrueNASClient", *, options: "dict | None" = None):
        self.client = client
        self.options = options or {}
        self._ws = None
        self._lock = _threading.RLock()
        self.shell_id: "str | None" = None

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

            import ssl

            from .utils import tls

            # The same trust as the API websocket -- see pytruenas.utils.tls.
            context = tls.context(self.client.sslverify)
            sslopt = (
                {"cert_reqs": ssl.CERT_NONE}
                if context is None
                else {"context": context}
            )
            ws = _websocket.WebSocket(sslopt=sslopt)
            ws.connect(self._uri(), timeout=CONNECT_TIMEOUT)

            # match_origin=True, single_use=True: the middleware's own default
            # for the first is True and pytruenas was passing False, which
            # made a leaked token usable from anywhere. This one is handed
            # straight to a websocket WE open, from this machine, exactly once.
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
                if isinstance(frame, str):
                    try:
                        message = _json.loads(frame)
                    except ValueError:
                        continue
                    if message.get("msg") == "connected":
                        self.shell_id = message.get("id")
                    elif message.get("msg") == "failed":
                        ws.close()
                        raise _OperationNotStarted(
                            "web shell rejected the token: "
                            f"{message.get('error', {}).get('reason', 'unknown')}"
                        )
            self._ws = ws
            return ws

    def close(self) -> None:
        with self._lock:
            ws, self._ws = self._ws, None
            self.shell_id = None
            if ws is not None:
                try:
                    ws.close()
                except Exception:
                    pass

    # -- execution ---------------------------------------------------------

    @staticmethod
    def command_lines(
        command: str,
        token: str,
        *,
        input: "bytes | None" = None,
        merge_stderr: bool = False,
    ) -> "list[str]":
        """The lines typed into the terminal to run ``command``.

        Every byte of ``command`` and ``input`` is base64-encoded; the lines
        themselves are plain ASCII with no control characters, TABs, ``!`` or
        newlines except the one ending each line. Markers are spelled in two
        quoted halves so the terminal's echo of these lines never contains a
        marker contiguously -- only the output of ``printf`` does.
        """
        v = f"__pytn{token}"
        lines = [f"{v}e=$(mktemp) {v}i=$(mktemp) {v}f=$(mktemp)"]
        if input:
            encoded = _b64(input)
            for offset in range(0, len(encoded), _CHUNK):
                chunk = encoded[offset : offset + _CHUNK]
                lines.append(f"printf %s '{chunk}' >> \"${v}i\"")
            # `< file`, not `base64 -d file`: BSD base64 (macOS) takes no
            # positional file argument and reads stdin instead, so the decoded
            # input came out empty and the command ran with no input at all.
            lines.append(f'base64 -d < "${v}i" > "${v}f"')
            stdin = f'"${v}f"'
        else:
            stdin = "/dev/null"
        stderr = "2>&1" if merge_stderr else f'2>"${v}e"'
        lines.append(
            "stty -opost 2>/dev/null; "
            f'printf %s%s "__ST" "{token}__"; '
            f"eval \"$(printf %s '{_b64(command.encode())}' | base64 -d)\" "
            f"< {stdin} {stderr}; "
            f"{v}r=$?; "
            f'printf %s%s "__OUT" "{token}__"; '
            f'cat "${v}e"; '
            f'rm -f "${v}e" "${v}i" "${v}f"; '
            f'printf %s%s%s%s "__EN" "{token}_" "${v}r" "_EN__"'
        )
        return lines

    def execute(
        self,
        command: str,
        *,
        input: "bytes | None" = None,
        merge_stderr: bool = False,
        timeout: "float | None" = None,
        sink: "_ty.Callable[[bytes], None] | None" = None,
        errsink: "_ty.Callable[[bytes], None] | None" = None,
    ) -> "tuple[bytes, bytes, int]":
        """Run ``command``; return ``(stdout, stderr, returncode)`` as bytes.

        ``sink`` receives stdout AS IT ARRIVES (for output the caller did not
        capture), ``errsink`` receives stderr when the command finishes.
        ``timeout=None`` waits indefinitely. On timeout the command is
        interrupted and the session closed (its hang-up ends the shell's jobs),
        and a ``TimeoutExpired`` carrying the partial output is raised.

        A connection lost before the command's opening marker arrived raises
        ``OperationNotStarted``: nothing ran, so another provider may retry.
        """
        token = _uuid.uuid4().hex[:16]
        frame = _Frame(token)
        deadline = None if timeout is None else _time.monotonic() + timeout
        with self._lock:
            ws = self.connect()
            try:
                for line in self.command_lines(
                    command, token, input=input, merge_stderr=merge_stderr
                ):
                    ws.send_binary((line + "\n").encode("ascii"))
            except Exception as exc:
                self.close()
                raise _OperationNotStarted(
                    f"web shell send failed: {type(exc).__name__}", cause=exc
                ) from exc

            pending = bytearray()
            flush_at = _time.monotonic() + _FLUSH_INTERVAL
            while frame.state != "done":
                remaining = None if deadline is None else deadline - _time.monotonic()
                if remaining is not None and remaining <= 0:
                    if sink is not None and pending:
                        sink(bytes(pending))
                    self._abandon(ws)
                    raise _expired(
                        command,
                        timeout,
                        output=bytes(frame.out),
                        stderr=bytes(frame.err),
                        orphaned=False,
                    )
                ws.settimeout(_POLL if remaining is None else min(_POLL, remaining))
                try:
                    data = ws.recv()
                except Exception as exc:
                    if type(exc).__name__ == "WebSocketTimeoutException":
                        if sink is not None and pending:
                            sink(bytes(pending))
                            pending.clear()
                        continue
                    self.close()
                    if not frame.started:
                        raise _OperationNotStarted(
                            f"web shell connection lost: {type(exc).__name__}",
                            cause=exc,
                        ) from exc
                    raise _subprocess.SubprocessError(
                        f"web shell connection lost: {type(exc).__name__}"
                    ) from exc
                if isinstance(data, str):
                    data = data.encode("utf-8", "surrogateescape")
                out, err = frame.feed(data)
                if sink is not None and out:
                    pending += out
                    if len(pending) >= _BATCH or _time.monotonic() >= flush_at:
                        sink(bytes(pending))
                        pending.clear()
                        flush_at = _time.monotonic() + _FLUSH_INTERVAL
                _send(errsink, err)
            if sink is not None and pending:
                sink(bytes(pending))
        return bytes(frame.out), bytes(frame.err), _ty.cast(int, frame.returncode)

    def _abandon(self, ws) -> None:
        """Interrupt the running command and drop the session."""
        try:
            ws.send_binary(b"\x03")
        except Exception:
            pass
        self.close()


class WebShellExecutorProvider(_ExecutorProvider):
    """Executor for hosts reachable on the API port but not over SSH."""

    def __init__(self, client: "TrueNASClient"):
        self.client = client
        self._session: "WebShellSession | None" = None
        # No `args`: the terminal takes one line of shell text, so hostctl
        # renders the whole invocation to a single string rather than an argv.
        super().__init__("webshell", self._execute, capabilities=())

    # -- lifecycle ---------------------------------------------------------

    @property
    def session(self) -> WebShellSession:
        if self._session is None:
            self._session = WebShellSession(self._client)
        return self._session

    @property
    def _client(self):
        client = getattr(self.client, "client", None)
        return client if client is not None else self.client

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
        try:
            self.session.connect()
        except _OperationNotStarted:
            raise
        except Exception as exc:
            raise _OperationNotStarted(
                f"web shell unavailable: {type(exc).__name__}", cause=exc
            ) from exc

    def close(self) -> None:
        if self._session is not None:
            self._session.close()
            self._session = None

    # -- dispatch ----------------------------------------------------------

    def _execute(self, command: object, *args: object, **options: object):
        if args:
            raise NotImplementedError(
                "the web shell takes one rendered command, not argv arguments"
            )
        script = str(command)
        encoding = _ty.cast("str | None", options.get("encoding"))
        errors = _ty.cast("str | None", options.get("errors"))
        text_mode = bool(encoding or errors or options.get("text"))

        payload = options.get("input")
        stdin = options.get("stdin")
        if payload is not None and stdin is not None:
            raise ValueError("stdin and input arguments may not both be used")
        if isinstance(stdin, int) and stdin != _subprocess.DEVNULL:
            raise NotImplementedError(
                "the web shell needs a readable stdin object, not a file "
                "descriptor: the terminal has no fd a caller's pipe can be "
                "attached to"
            )
        if stdin is not None and not isinstance(stdin, int):
            read = getattr(stdin, "read", None)
            if read is None:
                raise NotImplementedError(
                    "stdin must be a readable object with a .read() method"
                )
            # Read to EOF and deliver as input: see the module docstring for
            # why stdin cannot be streamed through a terminal.
            payload = read()
        data = None if payload is None else _input_bytes(payload, encoding)

        # hostctl's own convention, applied by the same helper every other
        # executor uses, so one invocation behaves the same on every provider.
        stdout_target, stderr_target = _capture_streams(
            _ty.cast(_ty.Any, options.get("capture_output", True)),
            _ty.cast(_ty.Any, options.get("stdout")),
            _ty.cast(_ty.Any, options.get("stderr")),
        )
        merge = stderr_target == _subprocess.STDOUT
        sink = (
            None
            if stdout_target == _subprocess.PIPE
            else self._sink(stdout_target, encoding, errors, err=False)
        )
        errsink = (
            None
            if merge or stderr_target == _subprocess.PIPE
            else self._sink(stderr_target, encoding, errors, err=True)
        )
        timeout = _ty.cast("float | None", options.get("timeout"))
        try:
            out, err, returncode = self.session.execute(
                script,
                input=data,
                merge_stderr=merge,
                timeout=timeout,
                sink=sink,
                errsink=errsink,
            )
        except _subprocess.TimeoutExpired as exc:
            if text_mode:
                exc.output = self._decode(exc.output, encoding, errors)
                exc.stderr = self._decode(exc.stderr, encoding, errors)
            raise

        def _value(raw: bytes) -> "str | bytes":
            return self._decode(raw, encoding, errors) if text_mode else raw

        stdout = _value(out) if stdout_target == _subprocess.PIPE else None
        stderr = (
            _value(err) if not merge and stderr_target == _subprocess.PIPE else None
        )
        result = _subprocess.CompletedProcess(script, returncode, stdout, stderr)
        if options.get("check") and returncode:
            raise _subprocess.CalledProcessError(returncode, script, stdout, stderr)
        return result

    @staticmethod
    def _decode(raw: "bytes | None", encoding: "str | None", errors: "str | None"):
        if raw is None or isinstance(raw, str):
            return raw
        return raw.decode(encoding or "utf-8", errors or "strict")

    @staticmethod
    def _sink(
        target: object, encoding: "str | None", errors: "str | None", *, err: bool
    ) -> "_ty.Callable[[bytes], None]":
        """A callable writing raw bytes to one resolved output target.

        ``None`` means "the process's own stdout/stderr", matching
        :func:`hostctl.executor.dispatch_output`; the binary buffer is preferred
        so bytes reach the terminal undecoded. ``write_output`` handles every
        other target shape (an int fd, a text stream, DEVNULL).
        """
        default = _sys.stderr if err else _sys.stdout

        def _write(chunk: bytes) -> None:
            stream = target
            if stream is None:
                stream = getattr(default, "buffer", default)
            _write_output(
                _ty.cast(_ty.Any, stream), chunk, encoding=encoding, errors=errors
            )

        return _write


__all__ = ["WebShellExecutorProvider", "WebShellSession", "clean_output"]
