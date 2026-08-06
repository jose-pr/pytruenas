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
demonstrably exists wherever the API does. nginx proxies it on 443 with a 7-day
timeout, so it reaches exactly the hosts SSH cannot.

Protocol (verified against 26.0.0-BETA.1, 18/18 live):

1. Open a websocket to ``/websocket/shell``.
2. Receive ``{"msg": "connected", "id": "<uuid>"}``.
3. Send **one JSON frame** ``{"token": ..., "options": {}}``. The token comes
   from ``auth.generate_token``; the server validates it via
   ``auth.get_token_for_shell_application``, which requires a token with no
   attributes and a user holding the ``web_shell`` privilege.
4. Every frame after that is raw PTY bytes, both directions.

Server-side it is ``os.forkpty()`` + ``os.execve("/usr/bin/login", ...)``, so
this is a real login shell -- not a request/response API.

**Input must be sent as BINARY frames.** The handler queues ``msg.data``
verbatim and the writer thread calls ``os.write(master_fd, ...)``, which
requires bytes. A *text* frame delivers a ``str``, ``os.write`` raises, the
worker thread dies without closing the pty, and the connection resets with no
error message. This is the single least obvious thing about the endpoint.

Known limits, all deliberate and declared rather than papered over:

* **stdout and stderr are one stream** -- a PTY has no separate error channel,
  so ``capture_output="stderr"`` cannot be honoured and ``CompletedProcess.
  stderr`` is always ``None``. The merged output is reported as stdout. A
  caller passing ``stderr=`` is not rejected, but nothing is written to it:
  duplicating the merged stream into both sinks would double every line.
  Splitting the two would mean rewriting the caller's command (redirecting
  ``2>`` to a marked file and reading it back), which changes what runs and
  breaks on shells without process substitution -- so it is deliberately not
  done here.

Output that is **not** captured is written through to ``stdout`` (defaulting to
``sys.stdout.buffer``) incrementally, as frames arrive, rather than buffered
until the command finishes. Those writes carry the **raw** PTY bytes, so colour
and other escape sequences survive; the captured ``CompletedProcess.stdout``
value stays cleaned, since a caller parsing it wants the text rather than the
terminal's rendering of it. ``capture_output``/``stdout`` resolution goes
through ``hostctl.executor.capture_streams``, the same helper the SSH executor
uses, so the option surface matches whichever provider a host selects.
* **No exit-status channel** -- the return code is recovered by appending a
  sentinel (``printf "__END__%s\\n" "$?"``) and reading until it appears.
* **No raw multi-line input** -- an embedded newline submits a partial line to
  the PTY and desynchronises every later read. Pipes and here-strings work
  because they are ordinary single-line shell syntax.
* A command that exits the shell (``exit 3``) ends the session; the next call
  reconnects.

Because of those, this provider is ordered **after** SSH. It is a real
executor for ordinary commands, not a degraded fallback -- but SSH's clean
separate channels are better when available.
"""

from __future__ import annotations

import json as _json
import re as _re
import subprocess as _subprocess
import sys as _sys
import threading as _threading
import time as _time
import typing as _ty
import uuid as _uuid

# `capture_streams` is part of `hostctl.executor`'s own __all__. `write_output`
# is NOT re-exported, so it comes from the private module -- deliberately, and
# narrowly: reimplementing it here would mean re-deriving its bytes<->str
# fallback and its fd-dup handling, and then drifting from the semantics every
# other executor gets. Tracked as a request to export it; if it moves, this
# import is the single site to fix.
from hostctl.executor import capture_streams as _capture_streams
from hostctl.executor._common import write_output as _write_output
from hostctl.provider import (
    ExecutorProvider as _ExecutorProvider,
    OperationNotStarted as _OperationNotStarted,
    ProviderProbe as _ProviderProbe,
)

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from . import TrueNASClient

#: Terminal escape sequences a PTY emits around real output. Stripped before a
#: caller sees stdout -- they are display instructions, not data.
_ANSI = _re.compile(
    rb"\x1b\[[0-9;?]*[a-zA-Z]"
    rb"|\x1b\][^\x07]*\x07"
    rb"|\x1b[=>]"
    rb"|\x1b\[\?[0-9]+[hl]"
    rb"|\x1b\[K"
)

#: The interactive prompt the login shell prints. It is echoed into the stream
#: alongside command output and has to come back out.
#:
#: Two shapes are matched: the full ``user@host[cwd]#`` prompt, and the bare
#: ``#``/``$`` that zsh emits (padded with spaces to the terminal width) while
#: redrawing its line. The second is easy to miss -- it looks like blank output
#: rather than a prompt, and leaves a stray ``#`` on the end of every result.
_PROMPT = _re.compile(
    r"^[^\s@]+@[^\s\[]*\[[^\]]*\][#$]\s*"  # root@HOST[~]#
    r"|^[#$]\s{2,}$"  # a bare, space-padded redraw
    r"|^\s*$",  # and the blank line it leaves behind
    _re.MULTILINE,
)

#: How long to wait for the login banner to settle before the first command.
_SETTLE = 2.0

DEFAULT_TIMEOUT = 120.0

#: Bytes to accumulate before writing to a streaming sink. A PTY delivers many
#: very small frames, so writing each one straight through costs a syscall per
#: keystroke echo for no benefit -- nothing reads a terminal that fast.
_BATCH = 4096

#: Longest a partial batch may wait before being flushed anyway. Without it a
#: command that prints one slow line at a time (a progress log, a compile)
#: would show nothing until it happened to cross _BATCH, which is exactly the
#: "silent until done" behaviour streaming is meant to remove.
_FLUSH_INTERVAL = 0.1

#: The **externally reachable** web-shell path. ``middlewared`` registers the
#: handler at ``/_shell`` (``main.py``'s ``add_route('*', '/_shell{...}')``),
#: but that is the *internal* path on port 6000: nginx exposes it as
#: ``/websocket/shell`` and proxies to ``/_shell`` behind the scenes.
#:
#: Connecting to ``/_shell`` on 443 does not fail cleanly -- nginx serves the
#: web UI there, so ``GET`` returns **200** instead of the 400 a websocket
#: endpoint gives, ``websocket-client`` follows the resulting redirect, and the
#: redirect target is an ``https://`` URL its own ``parse_url`` then rejects
#: with the baffling ``ValueError: scheme https is invalid``.
WEBSHELL_PATH = "/websocket/shell"


def clean_output(data: bytes) -> str:
    """Strip escape sequences, prompts, and CRs from raw PTY bytes.

    What comes off a PTY is a *terminal rendering*, not a clean stream: cursor
    moves, line redraws, and the shell's own prompt are interleaved with the
    command's output. This removes the rendering so a caller sees what the
    command actually printed.
    """
    text = _ANSI.sub(b"", data).replace(b"\r", b"").decode("utf-8", "replace")
    text = _PROMPT.sub("", text)
    # Collapse the blank runs the prompt removal leaves behind.
    return _re.sub(r"\n{2,}", "\n", text)


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

            sslopt = {} if self.client.sslverify else {"cert_reqs": ssl.CERT_NONE}
            ws = _websocket.WebSocket(sslopt=sslopt)
            ws.connect(self._uri())

            token = self.client.api.auth.generate_token(60, {}, False)
            ws.send(_json.dumps({"token": token, "options": self.options}))

            # Drain the connect frame and the login banner. A short read
            # timeout is the only way to know the prompt has settled -- the
            # server sends no "ready" marker.
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

    def run_script(
        self,
        script: str,
        *,
        timeout: "float | None" = None,
        sink: "_ty.Callable[[bytes], None] | None" = None,
    ) -> "tuple[str, bytes, int]":
        """Run one shell script; return cleaned output, raw bytes, and status.

        ``script`` must be a single line -- an embedded newline submits a
        partial line to the PTY and desynchronises every later read.

        ``sink``, when given, receives the raw PTY bytes AS THEY ARRIVE rather
        than only at completion, so a long-running command reports progress
        instead of going silent until its sentinel appears. Raw is deliberate:
        the sink is what a caller sees on their terminal, and stripping the
        escape sequences there would discard exactly the colour they are
        watching for. The cleaned text is still what the return value carries.

        Streaming has to hold back a suffix. The completion sentinel arrives
        split across frames like any other output, so the last ``len(end)``
        bytes are never emitted until more arrive behind them -- otherwise half
        a sentinel reaches the terminal and the caller sees the marker this
        module exists to hide. The withheld tail is flushed on completion,
        minus the sentinel line itself.
        """
        if "\n" in script or "\r" in script:
            raise ValueError(
                "the web shell takes single-line commands; encode a multi-line "
                "payload as a here-string or a pipe"
            )
        timeout = DEFAULT_TIMEOUT if timeout is None else timeout
        marker = _uuid.uuid4().hex[:12]
        end = f"__EN{marker}__"
        pattern = _re.compile(_re.escape(end) + r"(\d+)")

        with self._lock:
            ws = self.connect()
            # BINARY: the server writes msg.data straight to the pty fd, which
            # rejects str and kills its writer thread. See the module docstring.
            ws.send_binary(f'{script}; printf "{end}%s\\n" "$?"\n'.encode())

            ws.settimeout(timeout)
            deadline = _time.monotonic() + timeout
            buffer = b""
            # How much of `buffer` the sink has already seen. Bytes are emitted
            # once and never re-sent, so this only ever moves forward.
            emitted = 0
            # Never emit a tail that could still be a partial sentinel. The
            # sentinel is ASCII, so its byte length bounds how much to withhold.
            hold = len(end.encode()) + 12  # + room for the status digits
            flush_at = _time.monotonic() + _FLUSH_INTERVAL
            while _time.monotonic() < deadline:
                try:
                    frame = ws.recv()
                except Exception as exc:
                    self.close()
                    raise _subprocess.SubprocessError(
                        f"web shell connection lost: {type(exc).__name__}"
                    ) from exc
                buffer += frame if isinstance(frame, bytes) else frame.encode()
                text = clean_output(buffer)
                found = pattern.search(text)
                if sink is not None and not found:
                    safe = len(buffer) - hold
                    # Batch: a PTY delivers many tiny frames (often a frame per
                    # keystroke echo), and one write+flush each turns a noisy
                    # command into thousands of syscalls. Accumulate to
                    # _BATCH before emitting; the deadline below bounds how
                    # long a quiet partial batch can sit unflushed, so this
                    # trades syscalls for latency without ever withholding
                    # output indefinitely.
                    if safe - emitted >= _BATCH or (
                        safe > emitted and _time.monotonic() >= flush_at
                    ):
                        sink(buffer[emitted:safe])
                        emitted = safe
                        flush_at = _time.monotonic() + _FLUSH_INTERVAL
                if found:
                    if sink is not None:
                        sink(self._tail(buffer[emitted:], end))
                    return (
                        self._strip(text, script, end),
                        buffer,
                        int(found.group(1)),
                    )

        self.close()
        raise _subprocess.TimeoutExpired(script, timeout)

    @staticmethod
    def _tail(remainder: bytes, end: str) -> bytes:
        """The last withheld bytes, minus the sentinel line.

        The sentinel is the module's own bookkeeping and must not reach a
        caller's terminal. Everything the command itself printed before it
        still has to be flushed, hence trimming rather than dropping.
        """
        cut = remainder.find(end.encode())
        return remainder if cut < 0 else remainder[:cut]

    @staticmethod
    def _strip(text: str, script: str, end: str) -> str:
        """Drop the echoed command line and the sentinel from the output."""
        lines = []
        for line in text.splitlines():
            if end in line:
                continue
            # The pty echoes the submitted line back before running it.
            if not lines and script[:40] in line:
                continue
            lines.append(line)
        return "\n".join(lines).strip("\n")


class WebShellExecutorProvider(_ExecutorProvider):
    """Executor for hosts reachable on the API port but not over SSH."""

    def __init__(self, client: "TrueNASClient"):
        self.client = client
        self._session: "WebShellSession | None" = None
        # No `args`: a PTY takes one line of shell text, so hostctl should
        # render the whole invocation to a single string rather than an argv.
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

        A local target has the unix socket and does not need this. A user
        without the ``web_shell`` privilege would be rejected at the handshake,
        so decline up front rather than fail mid-command.
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
        if options.get("stdin") is not None:
            raise NotImplementedError(
                "the web shell cannot redirect stdin: the PTY has no input "
                "channel a caller can attach to"
            )
        if options.get("input") is not None:
            raise NotImplementedError(
                "the web shell cannot pipe input; encode it as a here-string "
                "or a pipe inside the command"
            )

        script = str(command)
        encoding = _ty.cast("str | None", options.get("encoding"))
        errors = _ty.cast("str | None", options.get("errors"))
        text_mode = bool(encoding or errors or options.get("text"))

        # hostctl's own convention, applied by the same helper every other
        # executor uses: `capture_output` resolves into concrete stdout/stderr
        # targets, so a caller writes one invocation that behaves identically
        # whichever provider a SystemHost happens to select.
        stdout_target, stderr_target = _capture_streams(
            _ty.cast(_ty.Any, options.get("capture_output", True)),
            _ty.cast(_ty.Any, options.get("stdout")),
            _ty.cast(_ty.Any, options.get("stderr")),
        )

        # Anything not being captured is streamed as it arrives. Only a
        # non-PIPE stdout gets a live sink: a PIPE is collected and returned,
        # and DEVNULL is discarded by write_output anyway -- but routing it
        # through the sink would still pay for the batching work, so skip it.
        sink = None
        if stdout_target != _subprocess.PIPE:
            sink = self._sink(stdout_target, encoding, errors)

        text, raw, returncode = self.session.run_script(
            script,
            timeout=_ty.cast("float | None", options.get("timeout")),
            sink=sink,
        )

        # The captured value is the CLEANED text: a caller parsing stdout wants
        # what the command printed, not the terminal's rendering of it. The
        # live sink above is the opposite case and deliberately gets `raw`.
        value: "str | bytes" = text if text_mode else text.encode(encoding or "utf-8")

        # Already written by the sink; `dispatch_output` would write it twice.
        stdout = value if stdout_target == _subprocess.PIPE else None
        # stdout and stderr are the same stream on a PTY. There is nothing to
        # put in stderr, so it stays None whatever the caller asked for --
        # writing the merged output to BOTH sinks would duplicate every line.
        stderr = None
        result = _subprocess.CompletedProcess(script, returncode, stdout, stderr)
        if options.get("check") and returncode:
            raise _subprocess.CalledProcessError(returncode, script, stdout, stderr)
        return result

    @staticmethod
    def _sink(
        target: object, encoding: "str | None", errors: "str | None"
    ) -> "_ty.Callable[[bytes], None]":
        """A callable writing raw PTY bytes to one resolved stdout target.

        ``None`` means "the process's own stdout", matching
        :func:`hostctl.executor._common.dispatch_output`. ``sys.stdout.buffer``
        is preferred over ``sys.stdout`` so the bytes reach the terminal
        UNDECODED -- a batch boundary can fall inside a multi-byte character,
        and decoding each batch independently would corrupt it. ``write_output``
        handles every other target shape (an int fd, a text stream, DEVNULL),
        including the bytes->str fallback when a stream refuses bytes.
        """

        def _write(chunk: bytes) -> None:
            stream = target
            if stream is None:
                stream = getattr(_sys.stdout, "buffer", _sys.stdout)
            _write_output(
                _ty.cast(_ty.Any, stream), chunk, encoding=encoding, errors=errors
            )

        return _write


__all__ = ["WebShellExecutorProvider", "WebShellSession", "clean_output"]
