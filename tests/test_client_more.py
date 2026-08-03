"""Extra TrueNASClient coverage: download URL building, run() capture/input
branches, dump_api, and upload's token-generation path.

All offline: local targets skip the HTTP probe, and API/subprocess/requests are
mocked so no server or shell round-trips are needed (except the two tests gated
on a real POSIX shell, matching test_client.py).
"""

import os
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from pytruenas import TrueNASClient


def _posix_shell():
    for sh in ("/bin/sh", "/bin/bash"):
        if os.path.exists(sh):
            return sh
    return None


def _has_posix_shell():
    return _posix_shell() is not None


# ---------------------------------------------------------------- download ----


def test_download_buffered_builds_target_and_waits(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    c.api = MagicMock()
    # core.download returns (jobid, link); local scheme is ws -> http
    c.api.core.download.return_value = (11, "/_download/11?auth=x")

    captured = {}

    def fake_get(url, verify=None):
        captured["url"] = url
        captured["verify"] = verify
        return MagicMock(content=b"payload", raise_for_status=lambda: None)

    monkeypatch.setattr("requests.get", fake_get)

    out = c.download("config.save", filename="cfg", buffered=True, wait=True)
    assert out == b"payload"
    assert "/_download/11" in captured["url"]
    # buffered=True must block on the job before fetching
    c.api.core.job_wait.assert_called_once()


def test_download_no_wait_returns_jobid(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    c.api = MagicMock()
    c.api.core.download.return_value = (22, "/_download/22")
    # wait=False must NOT touch requests.get at all
    monkeypatch.setattr(
        "requests.get", MagicMock(side_effect=AssertionError("should not GET"))
    )
    assert c.download("config.save", wait=False) == 22


def test_upload_generates_token_when_absent(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    c.api = MagicMock()
    c.api.auth.generate_token.return_value = "gen-tok"
    captured = {}

    def fake_post(url, headers=None, verify=None, files=None):
        captured["headers"] = headers
        captured["files"] = files
        return MagicMock(json=lambda: {"job_id": 3})

    monkeypatch.setattr("requests.post", fake_post)
    # a str file is encoded; no token supplied -> generate_token path
    jobid = c.upload("hello", "filesystem.put", wait=False)
    assert jobid == 3
    c.api.auth.generate_token.assert_called_once()
    assert captured["headers"]["Authorization"] == "Token gen-tok"
    assert captured["files"]["file"] == b"hello"


# --------------------------------------------------------------- dump_api ----


def test_dump_api_parses_run_output(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    monkeypatch.setattr(
        TrueNASClient,
        "run",
        lambda self, *a, **k: subprocess.CompletedProcess(a, 0, stdout=b"{}"),
    )
    assert c.dump_api() == {}


# -------------------------------------------------------------------- run ----


@pytest.mark.skipif(not _has_posix_shell(), reason="needs a POSIX shell")
def test_run_capture_stdout_only():
    c = TrueNASClient(None, autologin=False)
    r = c.run(
        "printf hi",
        executable=_posix_shell(),
        capture_output="stdout",
        check=False,
        encoding="utf-8",
    )
    assert r.stdout == "hi"
    # stderr was not captured
    assert r.stderr is None


@pytest.mark.skipif(not _has_posix_shell(), reason="needs a POSIX shell")
def test_run_string_input_is_fed_to_stdin():
    c = TrueNASClient(None, autologin=False)
    r = c.run(
        "cat",
        executable=_posix_shell(),
        input="abc",
        capture_output="stdout",
        check=False,
        encoding="utf-8",
    )
    assert r.stdout == "abc"


@pytest.mark.skipif(not _has_posix_shell(), reason="needs a POSIX shell")
def test_run_str_input_with_text_encoding_no_double_encode():
    # Regression: str input + encoding="utf-8" used to pre-encode to bytes AND
    # pass encoding to subprocess, which then called .encode() on bytes and
    # crashed with AttributeError. Verified live on TrueNAS 26.0. Both str and
    # bytes input must work whether or not a text encoding is given.
    c = TrueNASClient(None, autologin=False)
    r1 = c.run(
        "cat",
        executable=_posix_shell(),
        input="xy",
        capture_output="stdout",
        check=False,
        encoding="utf-8",
    )
    assert r1.stdout == "xy"
    # bytes input WITH a text encoding must also round-trip (decoded for text mode)
    r2 = c.run(
        "cat",
        executable=_posix_shell(),
        input=b"zz",
        capture_output="stdout",
        check=False,
        encoding="utf-8",
    )
    assert r2.stdout == "zz"


@pytest.mark.skipif(not _has_posix_shell(), reason="needs a POSIX shell")
def test_run_joins_multiple_cmds_and_quotes_cwd():
    c = TrueNASClient(None, autologin=False)
    # two commands joined by ';' both run; cwd is normalised to posix
    r = c.run(
        "cd /",
        ("echo", "x"),
        executable=_posix_shell(),
        capture_output="stdout",
        check=False,
        encoding="utf-8",
        cwd="/tmp",
    )
    assert r.stdout.strip() == "x"


def test_run_input_and_stdin_conflict_raises():
    c = TrueNASClient(None, autologin=False)
    with pytest.raises(ValueError):
        c.run("true", executable="/bin/sh", input=b"x", stdin=subprocess.PIPE)


# -- construction ------------------------------------------------------------
#
# These replace a block that tested the client->host bridge: a lazily built
# `.host`, `_as_config()`, `_as_ssh_config()`, and `run()` forwarding to the
# host. There is no bridge any more -- the two classes were merged, so `run()`
# is inherited from hostctl rather than delegated, and the config is built
# once at construction.


def test_local_client_uses_the_socket_and_no_ssh_leg():
    c = TrueNASClient(None, autologin=False)
    assert c._config.is_local
    # Nothing to SSH to: commands already run on this machine.
    assert c._config.ssh is None
    assert [p.name for p in c._executor_selector.providers] == ["local"]


def test_remote_client_carries_the_target():
    c = TrueNASClient("wss://nas", "1-" + "a" * 64, autologin=False, sslverify=False)
    assert c._config.host == "nas"
    assert not c._config.is_local
    assert c._config.sslverify is False


def test_sslverify_reaches_every_transport():
    # The web shell reads `client.sslverify`, the JSON-RPC and REST legs read
    # `client._config.sslverify`. They must be the one value the caller set --
    # the property existing at all is the regression: without it the web shell
    # raised AttributeError on every wss:// connect.
    c = TrueNASClient("wss://nas", "1-" + "a" * 64, autologin=False, sslverify=False)
    assert c.sslverify is False
    assert c.sslverify is c._config.sslverify

    d = TrueNASClient("wss://nas", "1-" + "a" * 64, autologin=False)
    assert d.sslverify is True


def _webshell_sslopt(monkeypatch, **kwargs) -> dict:
    """Run WebShellSession.connect() against a stub and report the sslopt used."""
    import sys
    import types

    from pytruenas.webshell import WebShellSession

    seen: dict = {}

    class _StubWS:
        def __init__(self, sslopt=None):
            seen["sslopt"] = sslopt

        def connect(self, uri):
            pass

        def send(self, payload):
            pass

        def settimeout(self, timeout):
            pass

        def recv(self):
            # Ends the banner drain loop: connect() reads until it times out.
            raise TimeoutError

    monkeypatch.setitem(
        sys.modules, "websocket", types.SimpleNamespace(WebSocket=_StubWS)
    )

    client = TrueNASClient("wss://nas", autologin=False, **kwargs)
    # The token call is the only real I/O left in connect(); stub the API leg.
    monkeypatch.setattr(
        type(client),
        "api",
        property(
            lambda self: types.SimpleNamespace(
                auth=types.SimpleNamespace(
                    generate_token=lambda *a, **k: "tok",
                )
            )
        ),
    )
    WebShellSession(client).connect()
    return seen["sslopt"]


def test_webshell_sslopt_follows_the_flag(monkeypatch):
    import ssl

    # sslverify=False must reach the socket the web shell actually opens --
    # this is the leg that was reading a nonexistent client attribute.
    assert _webshell_sslopt(monkeypatch, sslverify=False) == {
        "cert_reqs": ssl.CERT_NONE
    }
    assert _webshell_sslopt(monkeypatch) == {}


def test_shell_string_becomes_an_ssh_leg():
    c = TrueNASClient("wss://nas", autologin=False, shell="ssh://root:pw@nas")
    ssh = c._config.ssh
    assert ssh is not None
    assert (ssh.host, ssh.username, ssh.password) == ("nas", "root", "pw")
    assert "ssh" in [p.name for p in c._executor_selector.providers]


def test_client_keys_encoding_is_unpacked_into_a_real_field():
    """`client_keys|root` was a string hack; SshConfig has a real field."""
    c = TrueNASClient(
        "wss://nas", autologin=False, shell="ssh://client_keys|root:PRIVATEKEY@nas"
    )
    ssh = c._config.ssh
    assert ssh.username == "root"
    assert ssh.client_keys == [b"PRIVATEKEY"]
    assert ssh.password is None
