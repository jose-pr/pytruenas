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


# -- run() delegation to the hostctl host -------------------------------------
#
# These replace four tests that asserted client.py's own subprocess plumbing --
# the [executable, "-c", script] argv, the file-like stdin drain, and the
# root-shell lookup. That code is gone; hostctl owns it, and its equivalence
# was verified against the old implementation on a real POSIX target (TrueNAS
# 26.0.0-BETA.1), where every ported assertion passed identically on both.
#
# What pytruenas still owns is the *delegation*: that `.run()` reaches the
# right host with the caller's arguments intact. That is what is tested here,
# and unlike the originals these do not need a POSIX shell to be meaningful.


def test_run_delegates_to_the_host(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    host = MagicMock()
    host.run.return_value = subprocess.CompletedProcess("true", 0)
    monkeypatch.setattr(type(c), "host", property(lambda self: host))

    c.run("true", capture_output=True, check=False, encoding="utf-8")

    host.run.assert_called_once_with(
        "true", capture_output=True, check=False, encoding="utf-8"
    )


def test_run_forwards_multiple_commands_verbatim(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    host = MagicMock()
    monkeypatch.setattr(type(c), "host", property(lambda self: host))

    c.run("cd /", ("echo", "x"), cwd="/tmp")

    # Quoting and joining are the shell flavour's job now -- the client must
    # pass the commands through untouched rather than pre-rendering them.
    assert host.run.call_args[0] == ("cd /", ("echo", "x"))
    assert host.run.call_args.kwargs["cwd"] == "/tmp"


def test_run_result_is_returned_unchanged(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    expected = subprocess.CompletedProcess("x", 3, stdout="out", stderr="err")
    host = MagicMock()
    host.run.return_value = expected
    monkeypatch.setattr(type(c), "host", property(lambda self: host))

    assert c.run("x", check=False) is expected


def test_host_is_built_lazily_and_cached(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    assert c._host is None
    first = c.host
    assert c._host is first
    assert c.host is first


def test_local_client_builds_a_local_socket_config():
    c = TrueNASClient(None, autologin=False)
    config = c._as_config()
    assert config.is_local
    # No SSH target for a local client -> no SSH leg to compose.
    assert config.ssh is None


def test_remote_client_config_carries_the_resolved_target():
    with patch.object(TrueNASClient, "_openwss", return_value=MagicMock()):
        with patch("pytruenas.client._req.get") as get:
            get.return_value = MagicMock(url="https://nas", status_code=400)
            c = TrueNASClient("nas", "1-" + "a" * 64, autologin=False, sslverify=False)
    config = c._as_config()
    assert config.host == "nas"
    assert not config.is_local
    assert config.sslverify is False


def test_ssh_config_becomes_an_ssh_leg():
    """The renamed `.ssh_config` target is what composes the SSH transport."""
    with patch.object(TrueNASClient, "_openwss", return_value=MagicMock()):
        with patch("pytruenas.client._req.get") as get:
            get.return_value = MagicMock(url="https://nas", status_code=400)
            c = TrueNASClient("nas", autologin=False, sslverify=False)
    c.ssh_config = c.ssh_config._replace(username="root", password="pw")
    ssh = c._as_ssh_config()
    assert ssh is not None
    assert ssh.host == "nas"
    assert ssh.username == "root"
    assert ssh.password == "pw"


def test_client_keys_encoding_is_unpacked_into_a_real_field():
    """`client_keys|root` was a string hack; SshConfig has a real field."""
    with patch.object(TrueNASClient, "_openwss", return_value=MagicMock()):
        with patch("pytruenas.client._req.get") as get:
            get.return_value = MagicMock(url="https://nas", status_code=400)
            c = TrueNASClient("nas", autologin=False, sslverify=False)
    c.ssh_config = c.ssh_config._replace(
        username="client_keys|root", password="PRIVATEKEY"
    )
    ssh = c._as_ssh_config()
    assert ssh.username == "root"
    assert ssh.client_keys == [b"PRIVATEKEY"]
    assert ssh.password is None
