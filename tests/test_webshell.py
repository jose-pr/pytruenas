"""The ``/_shell`` executor (step 10 of the hostctl migration).

Only the parts that can be tested without a TrueNAS box: output cleaning, URI
construction, and the guards on unsupported options. The wire protocol itself
was verified live against 26.0.0-BETA.1 (18/18), which is the only way to check
it -- a mocked PTY would just assert this module's own assumptions back at it.
"""

import subprocess
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
    raw = b"output\r\nroot@ASGARD-ODIN[~]# \r\n"
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


@pytest.mark.parametrize("stream", ["stdin", "stdout", "stderr"])
def test_rejects_stream_redirection(stream):
    with pytest.raises(NotImplementedError, match="PTY|redirect"):
        _provider()._execute("true", **{stream: subprocess.PIPE})


def test_rejects_piped_input():
    with pytest.raises(NotImplementedError, match="here-string|pipe"):
        _provider()._execute("cat", input="data")


def test_rejects_argv_arguments():
    # A PTY takes one line of shell text, so the provider declares no `args`
    # capability and hostctl renders the whole invocation to a string.
    with pytest.raises(NotImplementedError, match="argv"):
        _provider()._execute("echo", "a", "b")


def test_declares_no_args_capability():
    assert "args" not in _provider().capabilities


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
