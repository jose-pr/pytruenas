"""The web-shell executor: commands through a login-shell terminal.

Three layers are tested separately:

* what is TYPED (``command_lines``): nothing the terminal's line editor could
  interpret -- the command and its input travel base64-encoded;
* how output is FRAMED (``_Frame``): only markers the command printed count,
  never the terminal's echo of what was typed;
* the session and provider, against an emulator of the TrueNAS zsh terminal
  (echo with redraw sequences, a banner, output cut into small fragments), and,
  on a POSIX machine, against a real shell in a real pty.

Everything the old implementation got wrong on a real appliance is pinned here
(each was measured live on TrueNAS 26.0.0-BETA.1 before the rewrite): the echo
and the completion marker came back inside stdout, output with no trailing
newline was dropped, ``input=`` with a stderr split hung, a ``^C`` in ``input=``
ran the rest as a root command, unread ``stdin=`` was executed by the shell, and
output handling was quadratic.
"""

import base64
import io
import os
import re
import shutil
import subprocess
import sys
import time
from unittest.mock import MagicMock

import pytest

from hostctl.provider import OperationNotStarted

import pytruenas.webshell as ws_mod
from pytruenas.webshell import (
    WEBSHELL_PATH,
    WebShellExecutorProvider,
    WebShellSession,
    _Frame,
    clean_output,
)

TOKEN = "0123456789abcdef"

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


# -- what is typed -------------------------------------------------------------

HOSTILE = "printf 'a\\tb'; echo \"!!\" `x`\n\x03\x04\x1b[A\tdone"


def _decoded_command(lines):
    main = lines[-1]
    encoded = re.search(r"printf %s '([^']*)' \| base64 -d", main).group(1)
    return base64.b64decode(encoded).decode()


def _decoded_input(lines):
    chunks = [re.match(r"printf %s '([^']*)' >> ", line) for line in lines]
    return base64.b64decode("".join(m.group(1) for m in chunks if m))


def test_typed_lines_carry_nothing_a_line_editor_would_interpret():
    """No control characters, TABs, `!` or embedded newlines are typed.

    A `^C` inside `input=` used to break out of the here-document and run the
    rest of the payload as a root command (measured live); a TAB triggered
    completion; `!` history expansion.
    """
    payload = HOSTILE.encode() + bytes(range(256))
    lines = WebShellSession.command_lines(HOSTILE, TOKEN, input=payload)
    for line in lines:
        assert all(32 <= ord(ch) < 127 for ch in line), line
        assert "!" not in line
    assert _decoded_command(lines) == HOSTILE
    assert _decoded_input(lines) == payload


def test_long_input_is_split_across_bounded_lines():
    payload = os.urandom(20000)
    lines = WebShellSession.command_lines("cat", TOKEN, input=payload)
    assert len(lines) > 3
    assert max(len(line) for line in lines[1:-2]) <= ws_mod._CHUNK + 64
    assert _decoded_input(lines) == payload


def test_no_typed_line_contains_a_marker_contiguously():
    """So the terminal's echo of the line can never be taken for output."""
    for line in WebShellSession.command_lines("true", TOKEN, input=b"x"):
        assert f"__ST{TOKEN}__" not in line
        assert f"__OUT{TOKEN}__" not in line
        assert not re.search(rf"__EN{TOKEN}_\d+_EN__", line)


def test_stdin_is_dev_null_without_input_and_stderr_mode_is_chosen():
    plain = WebShellSession.command_lines("true", TOKEN)[-1]
    assert "< /dev/null" in plain and "2>&1" not in plain
    merged = WebShellSession.command_lines("true", TOKEN, merge_stderr=True)[-1]
    assert "2>&1" in merged


# -- framing -------------------------------------------------------------------


def _stream(out=b"", err=b"", rc=0, echo=True):
    """The bytes a TrueNAS zsh terminal sends for one command."""
    lines = WebShellSession.command_lines("cmd", TOKEN)
    junk = b"Welcome to TrueNAS\r\nroot@TRUENAS[~]# "
    if echo:
        for line in lines:
            # zsh redraws long lines with CR + erase-line inside the echo.
            text = line.encode()
            junk += text[:40] + b"\r\x1b[K" + text[40:] + b"\r\n"
    body = (
        f"__ST{TOKEN}__".encode()
        + out
        + f"__OUT{TOKEN}__".encode()
        + err
        + f"__EN{TOKEN}_{rc}_EN__".encode()
    )
    return junk + body + b"\r\nroot@TRUENAS[~]# "


def _feed_all(data, size):
    frame = _Frame(TOKEN)
    emitted_out = emitted_err = b""
    for offset in range(0, len(data), size):
        out, err = frame.feed(data[offset : offset + size])
        emitted_out += out
        emitted_err += err
        if frame.state == "done":
            break
    return frame, emitted_out, emitted_err


@pytest.mark.parametrize("size", [1, 2, 3, 5, 7, 13, 64, 100000])
def test_frame_ignores_echo_and_banner_at_every_split(size):
    data = _stream(out=b"hi\n", err=b"oops\n", rc=3)
    frame, out, err = _feed_all(data, size)
    assert (bytes(frame.out), bytes(frame.err), frame.returncode) == (
        b"hi\n",
        b"oops\n",
        3,
    )
    assert (out, err) == (b"hi\n", b"oops\n")  # emitted == captured


def test_frame_keeps_output_without_a_trailing_newline_and_exact_bytes():
    payload = b"abc"
    frame, _, _ = _feed_all(_stream(out=payload), 4)
    assert bytes(frame.out) == b"abc"
    binary = bytes(range(256)) + b"\r\n\r"
    frame, _, _ = _feed_all(_stream(out=binary), 9)
    assert bytes(frame.out) == binary


def test_frame_emits_a_short_line_on_the_frame_that_carries_it():
    """Streamed stdout is real-time: no whole-marker hold-back.

    Holding back a marker's length (23 bytes) delayed every short line until
    later output pushed it out -- measured live as four 1 s-apart lines arriving
    together at the end.
    """
    frame = _Frame(TOKEN)
    frame.feed(b"echo...\r\n" + f"__ST{TOKEN}__".encode())
    for line in (b"line1\n", b"line2\n", b"line3\n"):
        out, _ = frame.feed(line)
        assert out == line


def test_frame_holds_back_only_a_partial_marker():
    frame = _Frame(TOKEN)
    frame.feed(f"__ST{TOKEN}__".encode())
    out, _ = frame.feed(b"data__OU")
    assert out == b"data"
    out, _ = frame.feed(f"T{TOKEN}__".encode())
    assert out == b"" and frame.state == "err"


def test_frame_is_linear_in_output_size():
    """The old parser re-cleaned and re-scanned the whole buffer per frame:
    64 KiB of output exceeded a 240 s timeout (measured live)."""
    data = _stream(out=b"a" * (4 * 1024 * 1024))
    started = time.monotonic()
    frame, _, _ = _feed_all(data, 1024)
    assert frame.returncode == 0 and len(frame.out) == 4 * 1024 * 1024
    assert time.monotonic() - started < 10


# -- session and provider against a terminal emulator --------------------------


class _Terminal:
    """Emulates the TrueNAS zsh web-shell terminal at the websocket boundary.

    Understands exactly what `command_lines` types: echoes each line (with
    redraw sequences), and when the main line arrives runs ``responder(command,
    stdin_bytes, merged)`` -> ``(stdout, stderr, rc)`` and sends the framed
    result in small fragments, like a real pty.
    """

    def __init__(self, responder=None, fragment=5, delay=0.0, silent=False):
        self.responder = responder or (lambda cmd, data, merged: (b"", b"", 0))
        self.fragment = fragment
        self.delay = delay
        self.silent = silent
        self.sent = []
        self.frames = [b"root@TRUENAS[~]# "]
        self.timeout = None
        self.closed = False
        self._lines = []

    def send_binary(self, data):
        self.sent.append(data)
        if data == b"\x03":
            return
        line = data.decode().rstrip("\n")
        self._lines.append(line)
        self.frames.append(line[:30].encode() + b"\r\x1b[K" + line[30:].encode())
        if "stty -opost" in line and not self.silent:
            self._run(line)

    def _run(self, main):
        token = re.search(r'"__ST" "(\w+)__"', main).group(1)
        command = _decoded_command([main])
        data = (
            _decoded_input(self._lines)
            # Matches the decode line whether or not the file is redirected.
            if 'base64 -d < "$' in " ".join(self._lines)
            else b""
        )
        merged = "2>&1" in main
        out, err, rc = self.responder(command, data, merged)
        body = (
            f"__ST{token}__".encode()
            + out
            + f"__OUT{token}__".encode()
            + err
            + f"__EN{token}_{rc}_EN__\r\nroot@TRUENAS[~]# ".encode()
        )
        self._scheduled = time.monotonic() + self.delay
        for offset in range(0, len(body), self.fragment):
            self.frames.append(body[offset : offset + self.fragment])

    def settimeout(self, value):
        self.timeout = value

    def recv(self):
        import websocket

        if self.closed:
            raise websocket.WebSocketConnectionClosedException("closed")
        if self.delay and time.monotonic() < getattr(self, "_scheduled", 0):
            time.sleep(min(self.timeout or 0.01, 0.01))
            raise websocket.WebSocketTimeoutException("timed out")
        if not self.frames:
            time.sleep(min(self.timeout or 0.01, 0.05))
            raise websocket.WebSocketTimeoutException("timed out")
        return self.frames.pop(0)

    def close(self):
        self.closed = True


def _session(terminal):
    session = WebShellSession(MagicMock())
    session._ws = terminal
    return session


def _provider(terminal):
    client = MagicMock()
    client.config = MagicMock(is_local=False)
    provider = WebShellExecutorProvider(client)
    provider._session = _session(terminal)
    return provider


def _echo(cmd, data, merged):
    """Respond like `sh -c`: stdout "out:<cmd>", stderr "err", stdin echoed."""
    out = b"out:" + cmd.encode() + (b"|in:" + data if data else b"")
    return (out + (b"err" if merged else b""), b"" if merged else b"err", 0)


def test_default_capture_returns_exactly_what_the_command_printed():
    """Live before the rewrite: stdout was the whole echoed wrapper + marker."""
    result = _provider(_Terminal(_echo))._execute("echo hi")
    assert result.stdout == b"out:echo hi"
    assert result.stderr == b"err"
    assert result.returncode == 0
    assert result.args == "echo hi"


def test_text_mode_decodes():
    result = _provider(_Terminal(_echo))._execute("x", text=True)
    assert result.stdout == "out:x" and result.stderr == "err"


def test_stderr_to_stdout_merges():
    result = _provider(_Terminal(_echo))._execute("x", stderr=subprocess.STDOUT)
    assert result.stdout == b"out:xerr" and result.stderr is None


@pytest.mark.parametrize(
    "value",
    ["hé\n\x03rm -rf /\n", b"\x00\x01\xff", bytearray(b"ba"), memoryview(b"mv")],
)
def test_input_reaches_the_command_byte_for_byte(value):
    expected = value.encode() if isinstance(value, str) else bytes(value)
    result = _provider(_Terminal(_echo))._execute("cat", input=value)
    assert result.stdout == b"out:cat|in:" + expected


def test_a_stdin_object_is_read_and_delivered_as_input():
    """Pumping stdin into the terminal let unread bytes run as a root command."""
    result = _provider(_Terminal(_echo))._execute("cat", stdin=io.BytesIO(b"data"))
    assert result.stdout == b"out:cat|in:data"


def test_devnull_stdin_is_no_input_and_pipes_or_fds_are_rejected():
    result = _provider(_Terminal(_echo))._execute("true", stdin=subprocess.DEVNULL)
    assert result.stdout == b"out:true"
    for bad in (subprocess.PIPE, 7):
        with pytest.raises(NotImplementedError):
            _provider(_Terminal(_echo))._execute("cat", stdin=bad)


def test_input_and_stdin_together_and_argv_are_rejected():
    with pytest.raises(ValueError, match="may not both"):
        _provider(_Terminal(_echo))._execute("cat", stdin=io.BytesIO(b"a"), input="b")
    with pytest.raises(NotImplementedError, match="argv"):
        _provider(_Terminal(_echo))._execute("echo", "a", "b")
    assert "args" not in _provider(_Terminal(_echo)).capabilities


def test_check_raises_with_the_command_not_the_input():
    """The exception must not carry the input (it may be a password)."""
    failing = _Terminal(lambda cmd, data, merged: (b"", b"bad", 2))
    with pytest.raises(subprocess.CalledProcessError) as caught:
        _provider(failing)._execute("login", input="hunter2", check=True)
    assert caught.value.returncode == 2
    assert "hunter2" not in repr(caught.value.cmd)


def test_uncaptured_output_goes_to_its_targets():
    out, err = io.BytesIO(), io.BytesIO()
    result = _provider(_Terminal(_echo))._execute(
        "x", capture_output=False, stdout=out, stderr=err
    )
    assert result.stdout is None and result.stderr is None
    assert out.getvalue() == b"out:x" and err.getvalue() == b"err"


def test_timeout_interrupts_closes_and_raises_the_hostctl_shape():
    terminal = _Terminal(silent=True)
    session = _session(terminal)
    with pytest.raises(subprocess.TimeoutExpired) as caught:
        session.execute("sleep 100", timeout=0.3)
    assert caught.value.orphaned is False
    assert terminal.sent[-1] == b"\x03" and terminal.closed
    assert session._ws is None


def test_timeout_none_waits_past_the_poll_interval(monkeypatch):
    monkeypatch.setattr(ws_mod, "_POLL", 0.05)
    terminal = _Terminal(_echo, delay=0.4)
    out, err, rc = _session(terminal).execute("slow", timeout=None)
    assert out == b"out:slow" and rc == 0


def test_a_connection_lost_before_the_command_started_did_not_run_it():
    terminal = _Terminal(silent=True)
    terminal.closed = True
    with pytest.raises(OperationNotStarted):
        _session(terminal).execute("true", timeout=5)


def test_probe_declines_for_a_local_target_and_accepts_a_remote_one():
    client = MagicMock()
    client.config = MagicMock(is_local=True)
    probe = WebShellExecutorProvider(client).probe()
    assert not probe.usable and "local" in probe.reason
    assert _provider(_Terminal()).probe().usable


# -- a real shell in a real pty (POSIX) ----------------------------------------

_REAL_PTY = sys.platform != "win32" and all(
    shutil.which(tool) for tool in ("sh", "base64", "mktemp", "stty")
)


class _PtyWebSocket:
    """A websocket whose far end is an interactive shell in a real pty.

    Stands in for the middleware's ``os.forkpty()`` + login shell: real echo,
    real line discipline, real parsing.
    """

    def __init__(self, shell="sh"):
        import pty

        self.pid, self.fd = pty.fork()
        if self.pid == 0:  # pragma: no cover - child
            os.environ["PS1"] = "root@TRUENAS[~]# "
            os.execvp(shell, [shell, "-i"])
        self.timeout = None
        self.closed = False

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
        if not self.closed:
            self.closed = True
            os.close(self.fd)
            os.kill(self.pid, 9)
            os.waitpid(self.pid, 0)


@pytest.fixture
def real_shell():
    ws = _PtyWebSocket()
    provider = _provider(_Terminal())
    provider._session._ws = ws
    yield provider
    ws.close()


@pytest.mark.skipif(not _REAL_PTY, reason="needs a POSIX pty and sh/base64/mktemp/stty")
def test_real_pty_round_trip(real_shell, tmp_path):
    run = real_shell._execute
    assert run("echo hi").stdout == b"hi\n"
    assert run("printf abc").stdout == b"abc"
    split = run("echo out; echo err >&2")
    assert (split.stdout, split.stderr) == (b"out\n", b"err\n")
    assert run("sh -c 'exit 3'").returncode == 3

    marker = tmp_path / "injected"
    hostile = f"x\x03touch {marker}\n\ttab !! end\n"
    assert run("cat", input=hostile).stdout == hostile.encode()
    run("true", stdin=io.BytesIO(f"touch {marker}\n".encode()))
    time.sleep(0.5)
    assert not marker.exists(), "input reached the shell as a command"

    big = run("head -c 262144 /dev/zero | tr '\\0' a").stdout
    assert big == b"a" * 262144
