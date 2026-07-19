"""Extra TrueNASClient coverage: download URL building, run() capture/input
branches, dump_api, and upload's token-generation path.

All offline: local targets skip the HTTP probe, and API/subprocess/requests are
mocked so no server or shell round-trips are needed (except the two tests gated
on a real POSIX shell, matching test_client.py).
"""

import os
import subprocess
from unittest.mock import MagicMock

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
    monkeypatch.setattr("requests.get",
                        MagicMock(side_effect=AssertionError("should not GET")))
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
        TrueNASClient, "run",
        lambda self, *a, **k: subprocess.CompletedProcess(a, 0, stdout=b"{}"),
    )
    assert c.dump_api() == {}


# -------------------------------------------------------------------- run ----

@pytest.mark.skipif(not _has_posix_shell(), reason="needs a POSIX shell")
def test_run_capture_stdout_only():
    c = TrueNASClient(None, autologin=False)
    r = c.run("printf hi", executable=_posix_shell(), capture_output="stdout",
              check=False, encoding="utf-8")
    assert r.stdout == "hi"
    # stderr was not captured
    assert r.stderr is None


@pytest.mark.skipif(not _has_posix_shell(), reason="needs a POSIX shell")
def test_run_string_input_is_fed_to_stdin():
    c = TrueNASClient(None, autologin=False)
    r = c.run("cat", executable=_posix_shell(), input="abc",
              capture_output="stdout", check=False, encoding="utf-8")
    assert r.stdout == "abc"


@pytest.mark.skipif(not _has_posix_shell(), reason="needs a POSIX shell")
def test_run_str_input_with_text_encoding_no_double_encode():
    # Regression: str input + encoding="utf-8" used to pre-encode to bytes AND
    # pass encoding to subprocess, which then called .encode() on bytes and
    # crashed with AttributeError. Verified live on TrueNAS 26.0. Both str and
    # bytes input must work whether or not a text encoding is given.
    c = TrueNASClient(None, autologin=False)
    r1 = c.run("cat", executable=_posix_shell(), input="xy",
               capture_output="stdout", check=False, encoding="utf-8")
    assert r1.stdout == "xy"
    # bytes input WITH a text encoding must also round-trip (decoded for text mode)
    r2 = c.run("cat", executable=_posix_shell(), input=b"zz",
               capture_output="stdout", check=False, encoding="utf-8")
    assert r2.stdout == "zz"


@pytest.mark.skipif(not _has_posix_shell(), reason="needs a POSIX shell")
def test_run_joins_multiple_cmds_and_quotes_cwd():
    c = TrueNASClient(None, autologin=False)
    # two commands joined by ';' both run; cwd is normalised to posix
    r = c.run("cd /", ("echo", "x"), executable=_posix_shell(),
              capture_output="stdout", check=False, encoding="utf-8", cwd="/tmp")
    assert r.stdout.strip() == "x"


def test_run_input_and_stdin_conflict_raises():
    c = TrueNASClient(None, autologin=False)
    with pytest.raises(ValueError):
        c.run("true", executable="/bin/sh", input=b"x", stdin=subprocess.PIPE)


# -- run() local-branch internals, subprocess mocked (platform-independent) ---

def _mock_subprocess_run(monkeypatch):
    """Patch subprocess.run in client.py to record its call and return a dummy."""
    calls = {}

    def fake_run(command, **kw):
        calls["command"] = command
        calls["kw"] = kw
        return subprocess.CompletedProcess(command, 0, stdout=b"", stderr=b"")

    monkeypatch.setattr("pytruenas.client.subprocess.run", fake_run)
    return calls


def test_run_capture_true_pipes_both_streams(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    calls = _mock_subprocess_run(monkeypatch)
    c.run("true", executable="/bin/sh", capture_output=True)
    assert calls["kw"]["stdout"] == subprocess.PIPE
    assert calls["kw"]["stderr"] == subprocess.PIPE
    # command is [executable, "-c", script]
    assert calls["command"][:2] == ["/bin/sh", "-c"]


def test_run_reads_from_filelike_stdin(monkeypatch):
    import io

    c = TrueNASClient(None, autologin=False)
    calls = _mock_subprocess_run(monkeypatch)
    c.run("cat", executable="/bin/sh", stdin=io.BytesIO(b"streamed"))
    # a readable file-like stdin is drained into `input` and stdin cleared
    assert calls["kw"]["input"] == b"streamed"
    assert calls["kw"]["stdin"] is None


def test_run_default_shell_from_api_when_remote(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    calls = _mock_subprocess_run(monkeypatch)
    # force the non-local shell lookup: no shell.path, not local -> api.user._get
    c.api = MagicMock()
    c.api.user._get.return_value = {"shell": "/usr/bin/zsh"}
    monkeypatch.setattr(type(c._api), "is_local", property(lambda self: False))
    c.run("true", capture_output=False)
    assert calls["command"][0] == "/usr/bin/zsh"


def test_run_default_shell_falls_back_to_bash_on_error(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    calls = _mock_subprocess_run(monkeypatch)
    c.api = MagicMock()
    c.api.user._get.side_effect = RuntimeError("no api")
    monkeypatch.setattr(type(c._api), "is_local", property(lambda self: False))
    c.run("true", capture_output=False)
    assert calls["command"][0] == "/bin/bash"
