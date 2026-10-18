"""The web-shell executor: commands through a login-shell terminal.

The framed protocol itself is hostctl's (``hostctl.console.PosixConsoleProfile``)
and is tested there. What is tested here is pytruenas's half:

* the websocket as a console stream (``_WebSocketStream``);
* the session and the ``ConsoleExecutor`` call surface, against an emulator
  of the TrueNAS zsh terminal (echo with redraw sequences, a banner, output cut
  into small fragments);
* the same against a real ``sh`` behind a pipe (Git Bash's on Windows), whose
  echo the fake websocket adds, and on a POSIX machine a real shell in a pty.

Everything an echo-parsing implementation got wrong on a real appliance stays
pinned (each was measured live on TrueNAS 26.0.0-BETA.1): the echo came back
inside stdout, output with no trailing newline was dropped, ``input=`` hung, a
``^C`` in ``input=`` ran the rest as a root command, and unread ``stdin=`` was
executed by the shell.
"""

import base64
import io
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
from unittest.mock import MagicMock

import pytest

from hostctl.exceptions import OperationNotStartedError
from hostctl.provider import ExecutorProvider

import pytruenas.webshell as ws_mod
from pytruenas.webshell import (
    WEBSHELL_PATH,
    WebShellExecutor,
    WebShellExecutorProvider,
    WebShellSession,
    _WebSocketStream,
    clean_output,
)

# -- output cleaning (a display helper; never applied to command output) ------


def test_clean_output_strips_ansi_prompt_and_cr():
    raw = b"\x1b[1mhello\x1b[0m\r\nroot@TRUENAS[~]# \r\n"
    text = clean_output(raw)
    assert "hello" in text and "root@" not in text and "\r" not in text


def test_clean_output_keeps_tabs_and_decodes_invalid_utf8():
    assert "a\tb" in clean_output(b"a\tb\n")
    assert isinstance(clean_output(b"\xff\xfe ok"), str)


# -- connection target ---------------------------------------------------------


def _client(scheme="https", host="nas"):
    client = MagicMock()
    target = MagicMock()
    target.scheme = scheme
    target._replace.return_value.uri = (
        f"{'wss' if scheme == 'https' else 'ws'}://{host}{WEBSHELL_PATH}"
    )
    client._http_target.return_value = target
    return client


def test_uri_uses_the_public_websocket_path():
    """nginx exposes the shell at /websocket/shell, not the internal /_shell."""
    client = _client()
    WebShellSession(client)._uri()
    client._http_target.assert_called_once_with(WEBSHELL_PATH)
    assert WEBSHELL_PATH == "/websocket/shell"


def test_uri_maps_https_to_wss_and_http_to_ws():
    assert WebShellSession(_client("https"))._uri().startswith("wss://")
    assert WebShellSession(_client("http"))._uri().startswith("ws://")


# -- the websocket as a console stream -----------------------------------------


class _Socket:
    """A websocket-client stand-in serving queued frames."""

    def __init__(self, *frames):
        self.frames = list(frames)
        self.sent = []
        self.timeouts = []
        self.connected = True

    def settimeout(self, value):
        self.timeouts.append(value)

    def recv(self):
        import websocket

        if not self.connected:
            raise websocket.WebSocketConnectionClosedException("closed")
        if not self.frames:
            raise websocket.WebSocketTimeoutException("timed out")
        return self.frames.pop(0)

    def send_binary(self, data):
        self.sent.append(data)


def test_stream_reads_at_most_size_and_keeps_the_rest():
    stream = _WebSocketStream(_Socket(b"abcdef"))
    assert stream.read(4, timeout=1) == b"abcd"
    assert stream.read(4, timeout=1) == b"ef"


def test_stream_read_times_out_empty_and_bounds_the_wait():
    socket = _Socket()
    stream = _WebSocketStream(socket)
    assert stream.read(10, timeout=0.2) == b""
    assert stream.read(10, timeout=0) == b""
    assert socket.timeouts == [0.2, 0.001]


def test_stream_encodes_a_text_frame_and_writes_binary():
    socket = _Socket("é")
    stream = _WebSocketStream(socket)
    assert stream.read(timeout=1) == "é".encode()
    stream.write(bytearray(b"x"))
    assert socket.sent == [b"x"]


def test_a_write_does_not_inherit_the_last_read_s_timeout():
    """The socket has one timeout for both directions: a draining read leaves
    it at a millisecond, and live a 2 KiB send of typed input then timed out."""
    socket = _Socket()
    stream = _WebSocketStream(socket)
    stream.read(10, timeout=0)
    stream.write(b"x")
    assert socket.timeouts == [0.001, ws_mod._WRITE_TIMEOUT]
    assert ws_mod._WRITE_TIMEOUT >= 10


def test_stream_raises_connection_error_once_closed():
    socket = _Socket()
    socket.connected = False
    with pytest.raises(ConnectionError):
        _WebSocketStream(socket).read(timeout=1)
    closing = _Socket("")
    closing.connected = False
    with pytest.raises(ConnectionError):
        _WebSocketStream(closing).read(timeout=1)


# -- an emulated TrueNAS terminal ----------------------------------------------

_APPEND = re.compile(r"printf %s '([A-Za-z0-9+/=]*)' >> \S+/([a-z])\b")


class _Terminal(_Socket):
    """Emulates the TrueNAS zsh web-shell terminal at the websocket boundary.

    Reads what ``PosixConsoleProfile`` types the way a shell would: base64
    chunks appended to the command (``c``) and input (``i``) files, an
    acknowledgement marker per batch, and the main line, on which it runs
    ``responder(command, stdin_bytes, merged)`` -> ``(stdout, stderr, rc)`` and
    sends the framed result in small fragments. Every line is echoed with zsh's
    redraw sequence first.
    """

    def __init__(self, responder=None, fragment=5, delay=0.0, silent=False):
        super().__init__(b"Welcome to TrueNAS\r\nroot@TRUENAS[~]# ")
        self.responder = responder or (lambda cmd, data, merged: (b"", b"", 0))
        self.fragment = fragment
        self.delay = delay
        self.silent = silent
        self.files = {}
        self._ready_at = 0.0

    def send_binary(self, data):
        import websocket

        if not self.connected:
            raise websocket.WebSocketConnectionClosedException("closed")
        self.sent.append(data)
        if data == b"\x03":
            return
        for line in data.decode("ascii").splitlines():
            self.frames.append(line[:30].encode() + b"\r\x1b[K" + line[30:].encode())
            self.frames.append(b"\r\n")
            for chunk, name in _APPEND.findall(line):
                self.files[name] = self.files.get(name, "") + chunk
            ack = re.search(r'"__AK" "(\w+)__"', line)
            if ack:
                self.frames.append(f"__AK{ack.group(1)}__\r\n".encode())
            start = re.search(r'"__ST" "(\w+)__"', line)
            if start and not self.silent:
                self._run(start.group(1), line)

    def _run(self, token, main):
        command = base64.b64decode(self.files.pop("c", "")).decode()
        data = base64.b64decode(self.files.pop("i", ""))
        out, err, rc = self.responder(command, data, "2>&1" in main)
        body = (
            f"__ST{token}__".encode()
            + out
            + f"__OUT{token}__".encode()
            + err
            + f"__EN{token}_{rc}_EN__\r\nroot@TRUENAS[~]# ".encode()
        )
        self._ready_at = time.monotonic() + self.delay
        for offset in range(0, len(body), self.fragment):
            self.frames.append(body[offset : offset + self.fragment])

    def recv(self):
        import websocket

        if self.delay and time.monotonic() < self._ready_at:
            time.sleep(0.01)
            raise websocket.WebSocketTimeoutException("timed out")
        if self.connected and not self.frames:
            time.sleep(0.01)
        return super().recv()

    def close(self):
        self.connected = False


def _session(terminal):
    session = WebShellSession(MagicMock())
    session._ws = terminal
    session._stream = _WebSocketStream(terminal)
    return session


def _provider(terminal):
    client = MagicMock()
    client.config = MagicMock(is_local=False)
    provider = WebShellExecutorProvider(client)
    provider._session = _session(terminal)
    return provider


def _run(terminal, command, *args, **options):
    return _provider(terminal).execute(command, *args, **options)


def _echo(cmd, data, merged):
    """Respond like `sh -c`: stdout "out:<cmd>", stderr "err", stdin echoed."""
    out = b"out:" + cmd.encode() + (b"|in:" + data if data else b"")
    return (out + (b"err" if merged else b""), b"" if merged else b"err", 0)


def test_the_executor_is_hostctl_s_console_executor():
    from hostctl.console import ConsoleExecutor

    provider = _provider(_Terminal())
    assert isinstance(provider.executor, WebShellExecutor)
    assert isinstance(provider.executor, ConsoleExecutor)
    assert "args" not in provider.capabilities


def test_default_capture_returns_exactly_what_the_command_printed():
    """Live with an echo parser: stdout was the whole echoed wrapper + marker."""
    result = _run(_Terminal(_echo), "echo hi")
    assert result.stdout == b"out:echo hi"
    assert result.stderr == b"err"
    assert result.returncode == 0
    assert result.args == "echo hi"


def test_text_mode_decodes():
    result = _run(_Terminal(_echo), "x", text=True)
    assert result.stdout == "out:x" and result.stderr == "err"


def test_stderr_to_stdout_merges():
    result = _run(_Terminal(_echo), "x", stderr=subprocess.STDOUT)
    assert result.stdout == b"out:xerr" and result.stderr is None


@pytest.mark.parametrize(
    "value",
    ["hé\n\x03rm -rf /\n", b"\x00\x01\xff", bytearray(b"ba"), memoryview(b"mv")],
)
def test_input_reaches_the_command_byte_for_byte(value):
    expected = value.encode() if isinstance(value, str) else bytes(value)
    result = _run(_Terminal(_echo), "cat", input=value)
    assert result.stdout == b"out:cat|in:" + expected


def test_long_input_is_typed_without_waiting_for_acknowledgements():
    """The middleware keeps reading the terminal, so no batch waits for the
    shell: one round trip per 2 KiB made 1 MiB of input take minutes."""
    payload = os.urandom(20000)
    terminal = _Terminal(_echo)
    result = _run(terminal, "cat " + "x" * 3000, input=payload)
    assert result.stdout == b"out:cat " + b"x" * 3000 + b"|in:" + payload
    typed = b"".join(terminal.sent).decode("ascii")
    assert "__AK" not in typed
    assert max(len(piece) for piece in terminal.sent) <= 2048
    assert all(32 <= ord(ch) < 127 for ch in typed.replace("\n", ""))
    assert "!" not in typed


def test_a_stdin_object_is_read_and_delivered_as_input():
    """Pumping stdin into the terminal let unread bytes run as a root command."""
    result = _run(_Terminal(_echo), "cat", stdin=io.BytesIO(b"data"))
    assert result.stdout == b"out:cat|in:data"


def test_devnull_stdin_is_no_input_and_a_pipe_is_rejected():
    result = _run(_Terminal(_echo), "true", stdin=subprocess.DEVNULL)
    assert result.stdout == b"out:true"
    with pytest.raises(ValueError, match="PIPE"):
        _run(_Terminal(_echo), "cat", stdin=subprocess.PIPE)


def test_input_and_stdin_together_and_argv_are_rejected():
    with pytest.raises(ValueError, match="may not both"):
        _run(_Terminal(_echo), "cat", stdin=io.BytesIO(b"a"), input="b")
    with pytest.raises(NotImplementedError, match="native arguments"):
        _run(_Terminal(_echo), "echo", "a", "b")


def test_check_raises_with_the_command_not_the_input():
    """The exception must not carry the input (it may be a password)."""
    failing = _Terminal(lambda cmd, data, merged: (b"", b"bad", 2))
    with pytest.raises(subprocess.CalledProcessError) as caught:
        _run(failing, "login", input="hunter2", check=True)
    assert caught.value.returncode == 2
    assert "hunter2" not in repr(caught.value.cmd)
    result = _run(_Terminal(lambda c, d, m: (b"", b"", 3)), "false", check=False)
    assert result.returncode == 3


def test_uncaptured_output_goes_to_its_targets():
    out, err = io.BytesIO(), io.BytesIO()
    result = _run(_Terminal(_echo), "x", capture_output=False, stdout=out, stderr=err)
    assert result.stdout is None and result.stderr is None
    assert out.getvalue() == b"out:x" and err.getvalue() == b"err"


def test_timeout_interrupts_closes_and_raises_the_hostctl_shape():
    terminal = _Terminal(silent=True)
    provider = _provider(terminal)
    started = time.monotonic()
    with pytest.raises(subprocess.TimeoutExpired) as caught:
        provider.execute("sleep 100", timeout=0.3)
    assert time.monotonic() - started < 3
    assert caught.value.orphaned is False
    assert terminal.sent[-1] == b"\x03" and not terminal.connected
    assert provider._session._ws is None


def test_timeout_none_waits_past_the_poll_interval():
    result = _run(_Terminal(_echo, delay=0.6), "slow")
    assert result.stdout == b"out:slow" and result.returncode == 0


def test_the_next_command_after_a_timeout_reconnects():
    provider = _provider(_Terminal(silent=True))
    with pytest.raises(subprocess.TimeoutExpired):
        provider.execute("sleep 100", timeout=0.2)
    fresh = _Terminal(_echo)
    provider.session.connect = lambda: provider.session.__dict__.update(
        _ws=fresh, _stream=_WebSocketStream(fresh)
    )
    assert provider.execute("echo again").stdout == b"out:echo again"


def test_a_command_that_ends_the_shell_raises_and_closes_the_session():
    terminal = _Terminal(silent=True)
    provider = _provider(terminal)
    threading.Timer(0.2, terminal.close).start()
    with pytest.raises(ConnectionError):
        provider.execute("exit 3", timeout=5)
    assert provider._session._ws is None


def test_a_terminal_gone_before_typing_declines_and_closes_the_session():
    """A failed write before the command line: nothing ran, so the host may
    try its next provider."""
    terminal = _Terminal()
    terminal.close()
    provider = _provider(terminal)
    with pytest.raises(OperationNotStartedError):
        provider.execute("true", timeout=5)
    assert provider._session._ws is None


def test_a_web_shell_that_cannot_connect_declines_with_the_cause():
    """A refused connection lets the host try another provider."""
    provider = _provider(_Terminal())
    provider._session._ws = None

    def refuse():
        raise OSError("connection refused")

    provider.session.connect = refuse
    with pytest.raises(OperationNotStartedError) as caught:
        provider.execute("true")
    assert caught.value.reason == "web shell unavailable: OSError: connection refused"

    fresh = _Terminal(_echo)
    provider.session.connect = lambda: provider.session.__dict__.update(
        _ws=fresh, _stream=_WebSocketStream(fresh)
    )
    assert provider.execute("echo next").stdout == b"out:echo next"


def test_a_failed_write_before_typing_falls_back_to_the_next_provider(caplog):
    from pytruenas.host import TrueNASConfig, TrueNASHost

    host = TrueNASHost(TrueNASConfig.from_target("wss://nas", autologin=False))
    terminal = _Terminal()
    terminal.close()
    webshell = _provider(terminal)
    other = ExecutorProvider(
        "other",
        lambda command, *a, **k: subprocess.CompletedProcess(command, 0, b"other", b""),
    )
    host.replace_providers(executor=(webshell, other))
    with caplog.at_level("WARNING"):
        assert host.run("true").stdout == b"other"
    assert any(
        "fell back from webshell to other" in record.getMessage()
        for record in caplog.records
    )


def test_probe_declines_for_a_local_target_and_accepts_a_remote_one():
    client = MagicMock()
    client.config = MagicMock(is_local=True)
    probe = WebShellExecutorProvider(client).probe()
    assert not probe.usable and "local" in probe.reason
    assert _provider(_Terminal()).probe().usable


# -- a real shell behind a pipe ------------------------------------------------

_SH = shutil.which("sh")
_HAS_SH = bool(_SH) and all(shutil.which(tool) for tool in ("base64", "mktemp"))
_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


class _PipeShell(_Socket):
    """A websocket whose far end is a real ``sh`` reading its stdin.

    A pipe has no echo, so this one adds it -- with zsh's redraw sequence --
    before the shell's own output, the way the appliance's terminal does.
    """

    def __init__(self):
        super().__init__()
        self.process = subprocess.Popen(
            [_SH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=_NO_WINDOW,
        )
        self._output = queue.Queue()
        threading.Thread(target=self._pump, daemon=True).start()
        self.timeout = None

    def _pump(self):
        while True:
            data = os.read(self.process.stdout.fileno(), 65536)
            self._output.put(data)
            if not data:
                return

    def settimeout(self, value):
        self.timeout = value

    def send_binary(self, data):
        self.sent.append(data)
        if data != b"\x03":
            for line in data.splitlines():
                self._output.put(line[:20] + b"\r\x1b[K" + line[20:] + b"\r\n")
        self.process.stdin.write(data)
        self.process.stdin.flush()

    def recv(self):
        import websocket

        try:
            data = self._output.get(timeout=self.timeout)
        except queue.Empty:
            raise websocket.WebSocketTimeoutException("timed out") from None
        if not data:
            self.connected = False
            raise websocket.WebSocketConnectionClosedException("closed")
        return data

    def close(self):
        self.connected = False
        if self.process.poll() is None:
            self.process.kill()
        self.process.wait()
        self.process.stdin.close()
        self.process.stdout.close()


@pytest.fixture
def pipe_shell():
    socket = _PipeShell()
    provider = _provider(_Terminal())
    provider._session._ws = socket
    provider._session._stream = _WebSocketStream(socket)
    yield provider
    socket.close()


@pytest.mark.skipif(not _HAS_SH, reason="needs sh, base64 and mktemp on PATH")
def test_real_shell_round_trip(pipe_shell, tmp_path):
    run = pipe_shell.execute
    assert run("echo hi").stdout == b"hi\n"
    assert run("printf abc").stdout == b"abc"
    split = run("echo out; echo err >&2")
    assert (split.stdout, split.stderr) == (b"out\n", b"err\n")
    assert run("exit_with() { return $1; }; exit_with 3", check=False).returncode == 3
    assert run("cat", input=bytes(range(256))).stdout == bytes(range(256))


@pytest.mark.skipif(not _HAS_SH, reason="needs sh, base64 and mktemp on PATH")
def test_real_shell_never_runs_input_as_a_command(pipe_shell, tmp_path):
    marker = (tmp_path / "injected").as_posix()
    hostile = f"x\x03touch '{marker}'\n\ttab !! end\n"
    assert pipe_shell.execute("cat", input=hostile).stdout == hostile.encode()
    pipe_shell.execute("true", stdin=io.BytesIO(f"touch '{marker}'\n".encode()))
    pipe_shell.execute("true")
    assert not os.path.exists(marker), "input reached the shell as a command"


@pytest.mark.skipif(not _HAS_SH, reason="needs sh, base64 and mktemp on PATH")
def test_real_shell_large_output_and_input(pipe_shell):
    big = pipe_shell.execute("head -c 262144 /dev/zero | tr '\\0' a").stdout
    assert big == b"a" * 262144
    payload = os.urandom(50000)
    assert pipe_shell.execute("cat", input=payload).stdout == payload


# -- a real shell in a real pty (POSIX) ----------------------------------------

_REAL_PTY = sys.platform != "win32" and all(
    shutil.which(tool) for tool in ("sh", "base64", "mktemp", "stty")
)


class _PtyWebSocket(_Socket):
    """A websocket whose far end is an interactive shell in a real pty.

    Stands in for the middleware's ``os.forkpty()`` + login shell: real echo,
    real line discipline, real parsing.
    """

    def __init__(self, shell="sh"):
        import pty

        super().__init__()
        self.pid, self.fd = pty.fork()
        if self.pid == 0:  # pragma: no cover - child
            os.environ["PS1"] = "root@TRUENAS[~]# "
            os.execvp(shell, [shell, "-i"])
        self.timeout = None

    def send_binary(self, data):
        os.write(self.fd, data)

    def settimeout(self, value):
        self.timeout = value

    def recv(self):
        import select

        import websocket

        ready, _, _ = select.select([self.fd], [], [], self.timeout)
        if not ready:
            raise websocket.WebSocketTimeoutException("timed out")
        try:
            data = os.read(self.fd, 65536)
        except OSError:
            data = b""
        if not data:
            raise websocket.WebSocketConnectionClosedException("closed")
        return data

    def close(self):
        if self.connected:
            self.connected = False
            os.close(self.fd)
            os.kill(self.pid, 9)
            os.waitpid(self.pid, 0)


@pytest.fixture
def real_shell():
    socket = _PtyWebSocket()
    provider = _provider(_Terminal())
    provider._session._ws = socket
    provider._session._stream = _WebSocketStream(socket)
    yield provider
    socket.close()


@pytest.mark.skipif(not _REAL_PTY, reason="needs a POSIX pty and sh/base64/mktemp/stty")
def test_real_pty_round_trip(real_shell, tmp_path):
    run = real_shell.execute
    assert run("echo hi").stdout == b"hi\n"
    assert run("printf abc").stdout == b"abc"
    split = run("echo out; echo err >&2")
    assert (split.stdout, split.stderr) == (b"out\n", b"err\n")
    assert run("sh -c 'exit 3'", check=False).returncode == 3

    marker = tmp_path / "injected"
    hostile = f"x\x03touch {marker}\n\ttab !! end\n"
    assert run("cat", input=hostile).stdout == hostile.encode()
    run("true", stdin=io.BytesIO(f"touch {marker}\n".encode()))
    time.sleep(0.5)
    assert not marker.exists(), "input reached the shell as a command"

    big = run("head -c 262144 /dev/zero | tr '\\0' a").stdout
    assert big == b"a" * 262144
