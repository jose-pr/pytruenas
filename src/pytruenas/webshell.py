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

* **stdout and stderr share one fd**, because a PTY has no second channel.
  They are separated *in band* when the caller asks for it: the command is
  wrapped so its stderr passes through a process substitution that brackets it
  with OSC 1337 markers, and the reader routes the marked regions to stderr.
  Verified live on 26.0.0-BETA.1.

  This needs ``2> >(...)``, which only bash/zsh/ksh parse -- under ``sh`` it is
  a syntax error, the command never runs, and the call would TIME OUT rather
  than fail usefully. So it is gated on the login shell reported by
  ``auth.me()`` (see :meth:`WebShellSession.supports_stderr_split`) and simply
  stays merged when that is not positive. Merged output is always correct,
  just less informative.

  A caller who asks for no separation (no ``stderr=``, no
  ``capture_output="stderr"``) pays nothing: the wrapper is only applied when
  the difference is observable.

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
  because they are ordinary single-line shell syntax, and a here-DOCUMENT is
  the one legal multi-line form (its newlines are the document's own, and the
  shell reads to the delimiter). ``input=`` uses exactly that.
* **Input works, in two shapes.** ``input=`` is a value known in full up
  front and rides along as a here-document -- no timing, no second channel,
  and the preferred form. ``stdin=`` takes a readable object and PUMPS it on a
  background thread, for a stream the caller is still producing; it races the
  pty's echo of the command line and is mitigated, not cured, by a short delay
  (see :meth:`WebShellSession._pump_stdin`). A file DESCRIPTOR is rejected --
  there is no pty fd to attach one to.
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

# Both public as of hostctl 0.2.5 (`write_output` was private until then, and
# this module imported it from `_common`). Sharing them is a correctness
# requirement, not a convenience: a host can dispatch the same call through
# different providers on different attempts, so an executor that handled output
# differently would return results that varied by which transport won.
from hostctl.executor import (
    capture_streams as _capture_streams,
    write_output as _write_output,
)
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
    r"[^\s@]+@[^\s\[]*\[[^\]]*\][#$]\s*"  # root@HOST[~]#
    r"|^[#$]\s{2,}"  # a bare, space-padded redraw
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

#: OSC code for the stderr boundary markers. 1337 is iTerm2's vendor code,
#: already used for private terminal integrations, so a terminal that does not
#: know these specific payloads still parses the SEQUENCE correctly and prints
#: nothing -- which is exactly the fallback wanted. A bare private string would
#: risk being rendered as literal text somewhere.
_OSC = 1337

#: What the wrapper emits around bytes that came from the command's stderr.
#: Matched against the RAW stream (never the cleaned text -- `clean_output`
#: strips OSC sequences, which would delete the very markers being looked for).
_ERR_START = b"\x1b]1337;PytruenasStderr\x07"
_ERR_END = b"\x1b]1337;PytruenasStdout\x07"

#: Shells whose syntax supports the `2> >(...)` process substitution the stderr
#: split depends on. `sh`/`dash` parse it as a syntax error, and the failure is
#: not clean: the command never runs, so the completion sentinel never appears
#: and the call TIMES OUT rather than reporting the real problem. Hence a
#: positive probe rather than an attempt-and-see.
_PROCSUB_SHELLS = ("bash", "zsh", "ksh")

#: How long the stdin pump waits before its first write, so the pty has echoed
#: the command line and the program is actually reading. See
#: `WebShellSession._pump_stdin` -- this mitigates a race it cannot eliminate,
#: which is why `input=` (a here-document, delivered with the command itself)
#: is preferred whenever the data is known up front.
_PUMP_DELAY = 0.5

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


def _with_input(script: str, value: object, *, encoding: object = None) -> str:
    """Embed ``value`` as the command's stdin, via a here-document.

    The PTY has no separate input channel, but a value known in FULL up front
    needs none: a here-document is ordinary single-line shell syntax, and the
    shell feeds it to the command as stdin exactly as a pipe would.

    The delimiter is quoted (``<<'EOF'``) so the shell performs NO expansion on
    the payload -- an unquoted here-doc would substitute ``$HOME``, backticks,
    and ``\\`` escapes inside what is supposed to be opaque data.

    A payload containing the delimiter would end the document early, so the
    delimiter carries a random suffix; a value containing THAT is not worth
    defending against. Bytes are decoded because the whole command is one text
    line by the time it reaches the pty.
    """
    if isinstance(value, bytes):
        value = value.decode(
            _ty.cast(str, encoding) or "utf-8", "replace"
        )
    text = str(value)
    delimiter = "PYTNIN" + _uuid.uuid4().hex[:8]
    if delimiter in text:  # pragma: no cover - a random 8-hex collision
        raise ValueError("input collides with the generated here-doc delimiter")
    # A here-doc is the one place a newline is legal in an otherwise
    # single-line command: it is the document's own line separator, and the
    # shell keeps reading until the delimiter line. `run_script` still rejects
    # newlines in the COMMAND, so this is built as one string and sent whole.
    return f"{script} <<'{delimiter}'\n{text}\n{delimiter}"


def _send(sink: "_ty.Callable[[bytes], None] | None", data: bytes) -> None:
    """Hand non-empty ``data`` to ``sink``, if there is one."""
    if sink is not None and data:
        sink(data)


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
        #: Tri-state: None = not yet probed, then the cached answer. See
        #: `supports_stderr_split`.
        self._procsub: "bool | None" = None
        #: Guards websocket SENDS only. Deliberately not `_lock`: the stdin
        #: pump runs while `run_script` holds that one and blocks in recv, so
        #: sharing it would deadlock. See `_pump_stdin`.
        self._send_lock = _threading.Lock()

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

    # -- stderr splitting --------------------------------------------------

    def login_shell(self) -> "str | None":
        """The login shell of the account this session authenticates as.

        ``auth.me()`` reports the authenticated account's passwd entry, so
        ``pw_shell`` is the shell ``/usr/bin/login`` will exec -- exactly what
        the PTY ends up running. ``None`` when the API cannot answer.
        """
        try:
            return _ty.cast(
                "str | None", self.client.api.auth.me().get("pw_shell")
            )
        except Exception:
            return None

    def supports_stderr_split(self) -> bool:
        """Whether the login shell can split stderr; resolved once, then cached.

        The split wraps the command in ``2> >(...)`` process substitution,
        which only bash/zsh/ksh parse. Under ``sh``/``dash`` it is a syntax
        error and the command never runs -- so the completion sentinel never
        arrives and the call TIMES OUT instead of failing usefully. Hence a
        positive answer is required before wrapping anything.

        The answer comes from the **API** (``auth.me()``'s ``pw_shell``), not
        from running a command. Asking the shell to identify itself would mean
        driving the very PTY this is meant to make safe: if the terminal is
        wedged, so is the probe, and the timeout it exists to prevent happens
        during the check. The API path also costs no PTY round-trip at all.

        Falls back to ``False`` when the shell is unknown -- merged output is
        always correct, just less informative, so an unknown shell degrades
        rather than risking the syntax error.
        """
        if self._procsub is None:
            shell = self.login_shell()
            self._procsub = bool(shell) and any(
                # Match the basename: `/usr/bin/zsh` -> `zsh`. A substring test
                # over the whole path would let `/usr/bin/nozsh` through, and
                # would miss nothing a basename match catches.
                shell.rsplit("/", 1)[-1] == name  # type: ignore[union-attr]
                for name in _PROCSUB_SHELLS
            )
        return self._procsub

    @staticmethod
    def wrap_stderr(script: str) -> str:
        """Wrap ``script`` so its stderr arrives fenced in OSC markers.

        stderr is redirected into a process substitution that brackets it with
        :data:`_ERR_START`/:data:`_ERR_END` and forwards it to the shared PTY.
        Both streams stay on one fd -- a PTY has no second channel -- but the
        markers say which bytes were which, so the reader can separate them.

        ``cat`` rather than a ``while read -r line`` loop, deliberately. A read
        loop is line-buffered (so a progress bar or a prompt written to stderr
        without a trailing newline never appears at all), strips trailing
        whitespace, and lets ``echo -e`` interpret backslash escapes inside the
        payload. ``cat`` forwards bytes unchanged, which is the whole point of
        keeping the stream raw.

        The markers therefore bracket each *write* ``cat`` performs rather than
        each line, which is the granularity the ordering actually needs: stderr
        stays interleaved with stdout in real time instead of arriving as a
        trailing dump the way a temp-file redirect would give.
        """
        # The markers hold ESC and BEL, which cannot appear literally in a
        # single-line command, so they are written as printf %b escapes.
        start = "\\033]%d;PytruenasStderr\\007" % _OSC
        end = "\\033]%d;PytruenasStdout\\007" % _OSC
        # `printf %b` emits the opening marker, then `cat` streams stderr
        # through untouched, then the closing marker. One marker pair per
        # stderr burst, with no shell loop between the bytes and the pty.
        forward = f'{{ printf "%b" "{start}"; cat; printf "%b" "{end}"; }}'
        return f"{{ {script} ; }} 2> >({forward})"

    # -- execution ---------------------------------------------------------

    def run_script(
        self,
        script: str,
        *,
        timeout: "float | None" = None,
        sink: "_ty.Callable[[bytes], None] | None" = None,
        errsink: "_ty.Callable[[bytes], None] | None" = None,
        heredoc: bool = False,
        stdin: object = None,
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
        # A here-document is the one legal multi-line form: its newlines are
        # the document's own separators and the shell keeps reading until the
        # delimiter, so the pty stays in sync. Anything else with an embedded
        # newline submits a partial line and desynchronises every later read.
        if not heredoc and ("\n" in script or "\r" in script):
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
            #
            # The sentinel's separator depends on the shape of the command. A
            # here-document ends at a line containing ONLY its delimiter, so
            # appending `; printf ...` to that last line stops it terminating:
            # the shell keeps reading input forever and the command never runs.
            # A NEWLINE puts the sentinel on its own line, after the document,
            # where it is an ordinary next command. Everything else keeps `;`,
            # which is what makes the status apply to the command just run.
            separator = "\n" if heredoc else "; "
            ws.send_binary(
                f'{script}{separator}printf "{end}%s\\n" "$?"\n'.encode()
            )

            if stdin is not None:
                self._pump_stdin(ws, stdin)

            ws.settimeout(timeout)
            deadline = _time.monotonic() + timeout
            buffer = b""
            # How much of `buffer` the sink has already seen. Bytes are emitted
            # once and never re-sent, so this only ever moves forward.
            emitted = 0
            # Which stream the NEXT byte belongs to. This has to persist across
            # batches: a stderr burst can span two emits, and splitting each
            # chunk independently would put its tail back on stdout the moment
            # a batch boundary fell inside the region.
            in_err = [False]
            # Never emit a tail that could still be a partial marker -- of
            # EITHER kind. An OSC boundary split across two frames would
            # otherwise reach the terminal as escape-sequence garbage AND put
            # the following bytes on the wrong stream, so the longest marker
            # bounds how much is withheld, not just the sentinel.
            hold = (
                max(
                    len(end.encode()) + 12,  # + room for the status digits
                    len(_ERR_START),
                    len(_ERR_END),
                )
            )
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
                        self._emit(buffer[emitted:safe], sink, errsink, in_err)
                        emitted = safe
                        flush_at = _time.monotonic() + _FLUSH_INTERVAL
                if found:
                    if sink is not None:
                        self._emit(
                            self._tail(buffer[emitted:], end),
                            sink,
                            errsink,
                            in_err,
                        )
                    return (
                        self._strip(text, script, end),
                        buffer,
                        int(found.group(1)),
                    )

        self.close()
        raise _subprocess.TimeoutExpired(script, timeout)

    def _pump_stdin(self, ws: object, stdin: object) -> "_threading.Thread":
        """Forward a readable ``stdin`` to the pty on a background thread.

        The mirror of the output watcher: it reads the caller's handle and
        sends each chunk as a BINARY frame, so a stream the caller is still
        producing (a file, a pipe, another process's output) reaches the
        command as it arrives rather than having to be known up front.

        **Concurrency.** `run_script` holds `self._lock` and blocks in
        `ws.recv()` for the whole command, so this thread cannot take that
        lock -- it would deadlock immediately. `websocket-client` does not
        guarantee a send is safe against a CONCURRENT recv, so sends are
        serialised on a separate `_send_lock` that the reader never holds:
        recv is left free to block while a send completes under its own lock.

        The thread is a daemon and is never joined for longer than the command:
        a handle that never reaches EOF (an open pipe with no writer) must not
        outlive the call or wedge interpreter shutdown.

        **Startup race, and why the delay is not a tuning knob.** There is no
        signal for "the command is now reading stdin" -- the pty echoes the
        command line, and nothing distinguishes the shell still parsing it from
        the program having started. Writing immediately puts the payload into
        the terminal's input buffer AHEAD of the program, where the shell
        treats it as the next command line instead of as input. `_PUMP_DELAY`
        waits for the echo to drain first; measured against 26.0.0-BETA.1,
        under 0.3s the payload is consistently mis-delivered.

        This is a genuine limitation of driving a terminal rather than a pipe:
        the delay makes the common case work, it does not make the race
        impossible. `input=` has no such problem -- a here-document is part of
        the command line itself, so the shell delivers it with no timing
        involved -- and is the better choice whenever the data is known up
        front.
        """
        read = getattr(stdin, "read", None)
        if read is None:
            raise NotImplementedError(
                "stdin must be a readable object with a .read() method"
            )

        def _run() -> None:
            try:
                # See the docstring: let the command line's echo drain before
                # writing, or the payload is parsed as the next command.
                _time.sleep(_PUMP_DELAY)
                while True:
                    chunk = read(_BATCH)
                    if not chunk:
                        break
                    if isinstance(chunk, str):
                        chunk = chunk.encode("utf-8")
                    with self._send_lock:
                        ws.send_binary(chunk)  # type: ignore[attr-defined]
                # EOF on the handle is EOF for the command: ^D on a pty, which
                # is what a program blocking on read() is waiting for. Without
                # it `cat` never returns and the command hangs to its timeout.
                with self._send_lock:
                    ws.send_binary(b"\x04")  # type: ignore[attr-defined]
            except Exception:
                # A pump failure must not kill the command: the output watcher
                # is still reading, and the command may well complete without
                # the rest of its input. It surfaces as whatever the command
                # does with truncated stdin.
                pass

        thread = _threading.Thread(
            target=_run, name="pytruenas-webshell-stdin", daemon=True
        )
        thread.start()
        return thread

    @staticmethod
    def _emit(
        chunk: bytes,
        sink: "_ty.Callable[[bytes], None] | None",
        errsink: "_ty.Callable[[bytes], None] | None",
        in_err: "list[bool]",
    ) -> None:
        """Route one chunk to the stdout/stderr sinks, honouring OSC markers.

        ``in_err`` is a one-element list used as a mutable cell: the "which
        stream are we in" flag has to survive between calls, because a stderr
        region can span batches.

        With no ``errsink`` the markers are still REMOVED but both streams go
        to ``sink`` -- that is the merged view a plain terminal wants, minus
        this module's framing bytes, and it keeps the markers from being
        rendered as garbage by a terminal that ignores OSC 1337.
        """
        if not chunk:
            return
        rest = chunk
        while rest:
            if in_err[0]:
                stop = rest.find(_ERR_END)
                if stop < 0:
                    _send(errsink or sink, rest)
                    return
                _send(errsink or sink, rest[:stop])
                rest = rest[stop + len(_ERR_END) :]
                in_err[0] = False
                continue
            start = rest.find(_ERR_START)
            if start < 0:
                _send(sink, rest)
                return
            _send(sink, rest[:start])
            rest = rest[start + len(_ERR_START) :]
            in_err[0] = True

    @staticmethod
    def split_streams(data: bytes) -> "tuple[bytes, bytes]":
        """Split raw PTY bytes into ``(stdout, stderr)`` on the OSC markers.

        Everything between :data:`_ERR_START` and :data:`_ERR_END` came from
        the command's stderr; everything else is stdout. The markers themselves
        are dropped from both -- they are this module's framing, not output.

        Runs against the RAW stream. `clean_output` strips OSC sequences, so
        splitting the cleaned text would find no markers at all.

        An unterminated final region (the command died mid-write, or the
        buffer was cut at a batch boundary) counts as stderr through the end:
        the marker said the stream switched, and nothing said it switched back.
        """
        out = bytearray()
        err = bytearray()
        rest = data
        while True:
            start = rest.find(_ERR_START)
            if start < 0:
                out += rest
                break
            out += rest[:start]
            rest = rest[start + len(_ERR_START) :]
            stop = rest.find(_ERR_END)
            if stop < 0:
                err += rest
                break
            err += rest[:stop]
            rest = rest[stop + len(_ERR_END) :]
        return bytes(out), bytes(err)

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
        script = str(command)

        # Two different things, both deliverable through the PTY's input side:
        #
        # * `input=` is a value known in full up front, so it is embedded as a
        #   here-document -- one line of ordinary shell syntax, no second
        #   channel needed.
        # * `stdin=` is a file-like the caller keeps writing to, so it is
        #   PUMPED: a reader thread forwards it to the websocket as it
        #   produces bytes (see `WebShellSession.pump_stdin`).
        #
        # An int fd (subprocess.PIPE/DEVNULL) is neither: PIPE has no bytes to
        # read and DEVNULL means "no input", so both are rejected rather than
        # silently doing nothing.
        payload = options.get("input")
        stdin = options.get("stdin")
        if payload is not None and stdin is not None:
            raise ValueError("stdin and input arguments may not both be used")
        heredoc = False
        if payload is not None:
            script = _with_input(
                script, payload, encoding=options.get("encoding")
            )
            heredoc = True
        if isinstance(stdin, int):
            raise NotImplementedError(
                "the web shell needs a readable stdin object, not a file "
                "descriptor: the PTY has no fd a caller's pipe can be "
                "attached to"
            )
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

        # Splitting stderr costs an extra shell wrapper, so it is only done
        # when the caller can actually observe the difference -- either they
        # want stderr captured separately, or they gave it its own sink. The
        # probe is what decides whether the login shell can do it at all;
        # without process substitution the streams stay merged, which is
        # always correct, just less informative.
        want_split = stderr_target is not None and stderr_target != _subprocess.STDOUT
        split = want_split and self.session.supports_stderr_split()
        if split:
            script = self.session.wrap_stderr(script)

        errsink = None
        if split and stderr_target != _subprocess.PIPE:
            errsink = self._sink(stderr_target, encoding, errors)

        text, raw, returncode = self.session.run_script(
            script,
            timeout=_ty.cast("float | None", options.get("timeout")),
            sink=sink,
            errsink=errsink,
            heredoc=heredoc,
            stdin=stdin,
        )

        # The captured value is the CLEANED text: a caller parsing stdout wants
        # what the command printed, not the terminal's rendering of it. The
        # live sink above is the opposite case and deliberately gets `raw`.
        if split:
            # Split the RAW stream (the markers are stripped from the cleaned
            # text), then clean each side independently.
            out_raw, err_raw = self.session.split_streams(raw)
            # No separate marker-stripping pass: `_ANSI` already matches
            # `\x1b][^\x07]*\x07`, which is exactly the OSC form these use.
            out_text = clean_output(out_raw)
            err_text = clean_output(err_raw)
        else:
            out_text, err_text = text, ""

        def _value(rendered: str) -> "str | bytes":
            return rendered if text_mode else rendered.encode(encoding or "utf-8")

        # Already written by the sink; writing it again would duplicate it.
        stdout = _value(out_text) if stdout_target == _subprocess.PIPE else None
        # Without a split there is genuinely nothing to report: a PTY merges
        # the two, and that merged text is already on stdout. Putting it in
        # stderr as well would duplicate every line.
        stderr = (
            _value(err_text)
            if split and stderr_target == _subprocess.PIPE
            else None
        )
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
        :func:`hostctl.executor.dispatch_output`. ``sys.stdout.buffer``
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
