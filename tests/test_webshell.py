"""The ``/_shell`` executor (step 10 of the hostctl migration).

Only the parts that can be tested without a TrueNAS box: output cleaning, URI
construction, and the guards on unsupported options. The wire protocol itself
was verified live against 26.0.0-BETA.1 (18/18), which is the only way to check
it -- a mocked PTY would just assert this module's own assumptions back at it.
"""

import io
import subprocess
import threading as _threading
from unittest.mock import MagicMock

import pytest

pytest.importorskip("hostctl")

from pytruenas.webshell import (  # noqa: E402
    WEBSHELL_PATH,
    WebShellExecutorProvider,
    WebShellSession,
    clean_output,
)

# -- output cleaning -------------------------------------------------------


def test_clean_output_strips_ansi():
    # Trailing newlines are preserved -- this cleans the *rendering*, not the
    # content; run_script() is what trims the final result.
    raw = b"\x1b[1m\x1b[7mhello\x1b[27m\x1b[0m\r\n"
    assert clean_output(raw).strip() == "hello"


def test_clean_output_strips_the_prompt():
    raw = b"output\r\nroot@TRUENAS[~]# \r\n"
    assert "root@" not in clean_output(raw)
    assert "output" in clean_output(raw)


def test_clean_output_strips_a_bare_redraw_prompt():
    """zsh redraws its line as a lone '#' padded to the terminal width.

    Easy to miss -- it looks like blank output rather than a prompt, and left a
    stray '#' on the end of every result until it was handled.
    """
    raw = b"real output\r\n#" + b" " * 60 + b"\r\n"
    assert clean_output(raw).strip() == "real output"


def test_clean_output_keeps_tabs_and_content():
    assert clean_output(b"tab\there\r\n").strip() == "tab\there"


def test_clean_output_decodes_invalid_utf8_without_raising():
    assert "hi" in clean_output(b"hi\xff\xfe\r\n")


# -- URI construction ------------------------------------------------------


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
    """nginx exposes the shell at /websocket/shell, not the internal /_shell.

    Connecting to /_shell on 443 does not fail cleanly: nginx serves the web UI
    there, so websocket-client follows a redirect into an https:// URL and its
    own parse_url rejects it with "scheme https is invalid".
    """
    client = _client()
    WebShellSession(client)._uri()
    client._http_target.assert_called_once_with(WEBSHELL_PATH)
    assert WEBSHELL_PATH == "/websocket/shell"


def test_uri_maps_https_to_wss_and_http_to_ws():
    assert WebShellSession(_client("https"))._uri().startswith("wss://")
    assert WebShellSession(_client("http"))._uri().startswith("ws://")


# -- guards on what a PTY cannot do ---------------------------------------


def _provider():
    client = MagicMock()
    client.config = MagicMock(is_local=False)
    return WebShellExecutorProvider(client)


def test_rejects_multi_line_scripts():
    """An embedded newline submits a partial line and desyncs every later read."""
    session = WebShellSession(MagicMock())
    with pytest.raises(ValueError, match="single-line"):
        session.run_script("echo a\necho b")


def test_rejects_stdin_redirection():
    """stdin stays rejected: the PTY has no input channel to attach to.

    stdout/stderr are NOT rejected any more -- the merged stream is written
    through to whatever the caller set, matching every other executor.
    """
    with pytest.raises(NotImplementedError, match="stdin"):
        _provider()._execute("true", stdin=subprocess.PIPE)


def test_rejects_an_fd_for_stdin():
    """An int fd has nothing to read and no pty fd to attach to."""
    with pytest.raises(NotImplementedError, match="descriptor|readable"):
        _provider()._execute("cat", stdin=subprocess.PIPE)


def test_rejects_stdin_and_input_together():
    with pytest.raises(ValueError, match="may not both"):
        _provider()._execute("cat", stdin=io.BytesIO(b"a"), input="b")


def test_rejects_argv_arguments():
    # A PTY takes one line of shell text, so the provider declares no `args`
    # capability and hostctl renders the whole invocation to a string.
    with pytest.raises(NotImplementedError, match="argv"):
        _provider()._execute("echo", "a", "b")


def test_declares_no_args_capability():
    assert "args" not in _provider().capabilities


# -- streaming output ------------------------------------------------------
#
# These drive run_script() against a fake websocket rather than a real PTY:
# the frames a PTY would send are exactly the input this logic has to handle,
# and scripting them is the only way to test *incremental* delivery at all --
# a live box hands back whatever timing it feels like.


class _FakeWS:
    """A websocket that replays a fixed frame sequence.

    `sent` records what run_script wrote, so a test can recover the generated
    sentinel and build a matching completion frame.
    """

    def __init__(self, frames):
        self._frames = list(frames)
        self.sent = []
        self.timeout = None

    def send_binary(self, data):
        self.sent.append(data)

    def settimeout(self, value):
        self.timeout = value

    def recv(self):
        if not self._frames:
            raise AssertionError("run_script read past the scripted frames")
        frame = self._frames.pop(0)
        return frame() if callable(frame) else frame

    def close(self):
        pass


def _session(frames):
    session = WebShellSession(MagicMock())
    session._ws = _FakeWS(frames)
    return session


def _end(session):
    """The sentinel run_script generated, recovered from what it sent."""
    sent = session._ws.sent[0].decode()
    return sent.split('printf "')[1].split("%s")[0]


def test_sink_receives_raw_bytes_preserving_ansi():
    """Colour must survive to the sink: raw bytes, not cleaned text.

    clean_output() strips exactly these escape sequences, so a sink fed the
    cleaned form would silently lose every colour the caller wanted to see.
    """
    session = _session([])
    chunks = []
    red = b"\x1b[31mDANGER\x1b[0m\r\n"
    session._ws = _FakeWS([red, lambda: f"{_end(session)}0\r\n".encode()])

    text, raw, code = session.run_script("echo x", sink=chunks.append)

    joined = b"".join(chunks)
    assert b"\x1b[31m" in joined, "ANSI was stripped before reaching the sink"
    assert b"DANGER" in joined
    assert code == 0
    # The cleaned return value is the opposite contract -- no escapes.
    assert "\x1b[31m" not in text and "DANGER" in text
    assert b"\x1b[31m" in raw


def test_sink_is_incremental_not_one_final_write():
    """Output arrives as it happens, not all at once when the command ends.

    A single write at completion is the behaviour this replaces, so the test
    asserts the sink saw data BEFORE the sentinel frame was ever read.
    """
    session = _session([])
    # Ordering, not totals: record how much the sink had received at the moment
    # each frame was read. Asserting only on the final total cannot distinguish
    # streaming from a single flush at completion -- the completion branch
    # writes the withheld remainder too, so both end with the same bytes.
    written = []
    events = []

    big = b"x" * 8192  # over _BATCH, so it flushes on arrival

    def frame_then_mark(data):
        def _f():
            events.append(("read", len(b"".join(written))))
            return data
        return _f

    session._ws = _FakeWS(
        [
            frame_then_mark(big),
            frame_then_mark(big),
            lambda: f"{_end(session)}0\r\n".encode(),
        ]
    )
    session.run_script("run", sink=written.append)

    # By the time the SECOND frame was read, the first must already have been
    # written out. Under buffer-until-done this is still 0.
    assert events[1][1] >= 4096, (
        "sink had received %d bytes when the 2nd frame arrived -- output is "
        "being buffered until completion, not streamed" % events[1][1]
    )


def test_sink_never_emits_the_sentinel():
    """The sentinel is internal bookkeeping and must not reach a terminal."""
    session = _session([])
    chunks = []
    session._ws = _FakeWS(
        [b"real output\r\n", lambda: f"{_end(session)}0\r\n".encode()]
    )

    session.run_script("echo hi", sink=chunks.append)

    joined = b"".join(chunks)
    assert b"real output" in joined
    assert b"__EN" not in joined, "the completion sentinel leaked to the sink"


def test_returncode_is_recovered_from_the_sentinel():
    session = _session([])
    session._ws = _FakeWS([lambda: f"{_end(session)}42\r\n".encode()])
    _, _, code = session.run_script("false")
    assert code == 42


def test_no_sink_still_returns_the_output():
    """Omitting the sink keeps the previous buffered behaviour intact."""
    session = _session([])
    session._ws = _FakeWS(
        [b"hello\r\n", lambda: f"{_end(session)}0\r\n".encode()]
    )
    text, raw, code = session.run_script("echo hello")
    assert "hello" in text and b"hello" in raw and code == 0


# -- stderr splitting ------------------------------------------------------
#
# These test the SPLITTER against bytes shaped like what the wrapper asks the
# shell to emit. That the appliance's shell actually produces those bytes is a
# separate claim, only checkable live -- see the module docstring.

_ERR_START = b"\x1b]1337;PytruenasStderr\x07"
_ERR_END = b"\x1b]1337;PytruenasStdout\x07"


def test_split_streams_separates_marked_regions():
    raw = b"out1" + _ERR_START + b"err1" + _ERR_END + b"out2"
    out, err = WebShellSession.split_streams(raw)
    assert out == b"out1out2"
    assert err == b"err1"


def test_split_streams_handles_no_markers():
    out, err = WebShellSession.split_streams(b"plain")
    assert out == b"plain" and err == b""


def test_split_streams_treats_an_unterminated_region_as_stderr():
    """The stream said it switched and never said it switched back."""
    out, err = WebShellSession.split_streams(b"a" + _ERR_START + b"boom")
    assert out == b"a" and err == b"boom"


def test_sinks_receive_their_own_streams():
    session = _session([])
    out_chunks, err_chunks = [], []
    body = b"to-out" + _ERR_START + b"to-err" + _ERR_END
    session._ws = _FakeWS([body, lambda: f"{_end(session)}0\r\n".encode()])

    session.run_script(
        "cmd", sink=out_chunks.append, errsink=err_chunks.append
    )

    assert b"to-out" in b"".join(out_chunks)
    assert b"to-err" in b"".join(err_chunks)
    # Neither sink may see the other's bytes, nor the framing itself.
    assert b"to-err" not in b"".join(out_chunks)
    assert b"\x1b]1337" not in b"".join(out_chunks + err_chunks)


def test_stderr_region_spanning_two_batches_stays_stderr():
    """The in-region flag has to persist across emits.

    A stderr burst longer than one batch would otherwise have its tail put
    back on stdout the moment a boundary fell inside the region.
    """
    session = _session([])
    out_chunks, err_chunks = [], []
    big = b"E" * 9000  # spans several _BATCH-sized emits
    session._ws = _FakeWS(
        [
            _ERR_START + big[:4500],
            big[4500:] + _ERR_END,
            lambda: f"{_end(session)}0\r\n".encode(),
        ]
    )

    session.run_script("cmd", sink=out_chunks.append, errsink=err_chunks.append)

    assert b"".join(err_chunks).count(b"E") == 9000
    assert b"E" not in b"".join(out_chunks)


def test_markers_are_stripped_when_there_is_no_errsink():
    """Merged view still must not render the framing as garbage."""
    session = _session([])
    chunks = []
    session._ws = _FakeWS(
        [
            b"a" + _ERR_START + b"b" + _ERR_END + b"c",
            lambda: f"{_end(session)}0\r\n".encode(),
        ]
    )
    session.run_script("cmd", sink=chunks.append)
    joined = b"".join(chunks)
    assert b"\x1b]1337" not in joined
    # Both streams still arrive -- merged is the point, not dropped.
    assert b"a" in joined and b"b" in joined and b"c" in joined


def test_wrap_stderr_uses_cat_not_a_read_loop():
    """A read loop is line-buffered and mangles the payload; cat is raw."""
    wrapped = WebShellSession.wrap_stderr("mycmd")
    assert "2> >(" in wrapped
    assert "cat" in wrapped
    assert "while read" not in wrapped
    assert "mycmd" in wrapped


# -- input delivery --------------------------------------------------------


def test_with_input_builds_a_quoted_heredoc():
    from pytruenas.webshell import _with_input

    script = _with_input("cat", "$HOME `id`")
    # Quoted delimiter: the payload must not be expanded by the shell.
    assert "<<'" in script
    assert "$HOME `id`" in script
    # Opens and closes with the same generated delimiter.
    delimiter = script.split("<<'")[1].split("'")[0]
    assert script.rstrip().endswith(delimiter)


def test_with_input_accepts_bytes():
    from pytruenas.webshell import _with_input

    assert "hello" in _with_input("cat", b"hello")


def test_heredoc_newlines_are_allowed_through_run_script():
    """A here-doc is the one legal multi-line form."""
    session = _session([])
    session._ws = _FakeWS([lambda: f"{_end(session)}0\r\n".encode()])
    # Would raise without heredoc=True.
    _, _, code = session.run_script("cat <<'X'\ndata\nX", heredoc=True)
    assert code == 0


def test_multi_line_still_rejected_without_heredoc():
    session = WebShellSession(MagicMock())
    with pytest.raises(ValueError, match="single-line"):
        session.run_script("echo a\necho b")


def test_stdin_is_pumped_to_the_websocket(monkeypatch):
    """A readable handle is forwarded as binary frames, then EOF.

    `_PUMP_DELAY` is patched out: it exists to lose a race against a REAL
    pty's echo (see `_pump_stdin`), and there is no pty here -- left in, the
    test would just sleep for it.
    """
    import pytruenas.webshell as ws_mod

    monkeypatch.setattr(ws_mod, "_PUMP_DELAY", 0)
    session = _session([])
    session._ws = _FakeWS([lambda: f"{_end(session)}0\r\n".encode()])

    session.run_script("cat", stdin=io.BytesIO(b"piped-payload"))

    # The pump runs on its own thread; wait for it rather than assuming it
    # won the race with this assertion.
    for thread in _threading.enumerate():
        if thread.name == "pytruenas-webshell-stdin":
            thread.join(timeout=5)

    # sent[0] is the command itself; the pump's writes follow.
    pumped = b"".join(session._ws.sent[1:])
    assert b"piped-payload" in pumped
    assert pumped.endswith(b"\x04"), "no EOF sent; a reader would hang"


# -- probe -----------------------------------------------------------------


def test_probe_declines_for_a_local_target():
    """A local target has the unix socket; a PTY would be strictly worse."""
    client = MagicMock()
    client.config = MagicMock(is_local=True)
    probe = WebShellExecutorProvider(client).probe()
    assert not probe.usable
    assert "local" in probe.reason


def test_probe_is_available_for_a_remote_target():
    assert _provider().probe().usable
