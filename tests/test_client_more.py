"""Extra TrueNASClient coverage: download URL building, run() capture/input
branches, dump_api, and upload's token-generation path.

All offline: local targets skip the HTTP probe, and API/subprocess/requests are
mocked so no server or shell round-trips are needed (except the two tests gated
on a real POSIX shell, matching test_client.py).
"""

import errno
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

    def fake_request(method, url, verify=None, timeout=None):
        captured["url"] = url
        captured["verify"] = verify
        return MagicMock(content=b"payload", raise_for_status=lambda: None)

    monkeypatch.setattr(
        "requests.Session.request", lambda self, *a, **k: fake_request(*a, **k)
    )
    monkeypatch.setattr("time.sleep", lambda _s: None)
    # The job is still running on the first poll: the fetch must wait for it.
    states = iter(["RUNNING", "SUCCESS"])
    polled = []

    def get_jobs(filters):
        polled.append(filters)
        assert "url" not in captured, "fetched before the job finished"
        return [{"id": 11, "state": next(states), "progress": {}, "result": None}]

    c.api.core.get_jobs.side_effect = get_jobs

    out = c.download("config.save", filename="cfg", buffered=True, wait=True)
    assert out == b"payload"
    assert "/_download/11" in captured["url"]
    # buffered=True blocks on THE job it started (11) before fetching
    assert polled == [[["id", "=", 11]]] * 2


def _streamed_download(monkeypatch, state):
    """A client whose unbuffered download job ends in `state`; returns the
    client and the order of events (`GET`, then each job poll)."""
    c = TrueNASClient(None, autologin=False)
    c.api = MagicMock()
    c.api.core.download.return_value = (33, "/_download/33?auth=x")
    events = []

    def fake_get(self, method, url, **kwargs):
        events.append("GET")
        return MagicMock(content=b"partial", raise_for_status=lambda: None)

    def get_jobs(filters):
        events.append("poll")
        return [
            {
                "id": 33,
                "state": state,
                "progress": {},
                "result": None,
                "error": "[EIO] read failed",
                "exc_info": {},
            }
        ]

    monkeypatch.setattr("requests.Session.request", fake_get)
    c.api.core.get_jobs.side_effect = get_jobs
    return c, events


def test_a_streamed_download_checks_its_job_after_the_fetch(monkeypatch):
    """The job streams into the response, so it is checked after the GET; a
    wait before it would never see the job finish."""
    c, events = _streamed_download(monkeypatch, "SUCCESS")
    assert c.download("filesystem.get", "/mnt/f") == b"partial"
    assert events == ["GET", "poll"]


def test_a_streamed_download_whose_job_failed_raises(monkeypatch):
    from pytruenas.connection import JobFailed

    c, _events = _streamed_download(monkeypatch, "FAILED")
    with pytest.raises(JobFailed):
        c.download("filesystem.get", "/mnt/f")


def test_read_bytes_of_a_failed_download_is_an_oserror(monkeypatch):
    """Through the real `Namespace`: `filesystem.get` is a download."""
    from pytruenas.fs.tnasws import _for_host

    class Middleware:
        _closed = type("Open", (), {"is_set": lambda self: False})()

        def call(self, method, *params, **kwds):
            if method == "core.download":
                return [33, "/_download/33?auth=x"]
            assert method == "core.get_jobs", method
            return [
                {
                    "id": 33,
                    "state": "FAILED",
                    "progress": {},
                    "error": "[EIO] read failed",
                    "exc_info": {},
                }
            ]

    monkeypatch.setattr(
        "requests.Session.request",
        lambda self, method, url, **kwargs: MagicMock(
            content=b"partial", raise_for_status=lambda: None
        ),
    )
    c = TrueNASClient("wss://nas", autologin=False)
    c._conn = Middleware()
    with pytest.raises(OSError) as error:
        _for_host(c, "/mnt/f").read_bytes()
    assert error.value.errno == errno.EIO


def test_download_no_wait_returns_a_handle_that_can_still_fetch(monkeypatch):
    """It returned the job id and discarded the link, so the bytes of a
    `wait=False` download could never be fetched."""
    c = TrueNASClient(None, autologin=False)
    c.api = MagicMock()
    c.api.core.download.return_value = (22, "/_download/22?auth_token=SECRET")
    c.api.core.get_jobs.return_value = [
        {"id": 22, "state": "SUCCESS", "progress": {}, "result": None}
    ]
    fetched = []

    def fake_request(self, method, url, **kwargs):
        fetched.append(url)
        return MagicMock(content=b"payload", raise_for_status=lambda: None)

    monkeypatch.setattr("requests.Session.request", fake_request)
    pending = c.download("config.save", wait=False)
    assert fetched == []  # wait=False GETs nothing until asked
    assert pending.job_id == 22 and "SECRET" not in repr(pending)
    assert pending.fetch() == b"payload"
    assert "/_download/22" in fetched[0]


def test_a_failed_download_does_not_name_its_token(monkeypatch):
    """requests names the URL, and a download link carries its auth_token."""
    import requests

    c = TrueNASClient(None, autologin=False)
    c.api = MagicMock()
    c.api.core.download.return_value = (5, "/_download/5?auth_token=SECRET-TOKEN")

    def fake_request(self, method, url, **kwargs):
        raise requests.ConnectionError(f"Max retries exceeded with url: {url}")

    monkeypatch.setattr("requests.Session.request", fake_request)
    with pytest.raises(ConnectionError) as raised:
        c.download("config.save")
    assert not isinstance(raised.value, requests.RequestException)
    assert "SECRET-TOKEN" not in str(raised.value)
    assert "auth_token=<redacted>" in str(raised.value)
    assert raised.value.__cause__ is None and raised.value.__suppress_context__


@pytest.mark.parametrize(
    "raised, expected",
    [
        ("ReadTimeout", "CallTimeout"),
        ("ConnectTimeout", "TimeoutError"),
        ("ChunkedEncodingError", "ClientException"),
    ],
)
def test_a_side_channel_raises_no_requests_exception(monkeypatch, raised, expected):
    import builtins

    import requests

    import pytruenas

    c = TrueNASClient(None, autologin=False)
    c.api = MagicMock()
    c.api.core.download.return_value = (5, "/_download/5?auth_token=SECRET-TOKEN")

    def fake_request(self, method, url, **kwargs):
        raise getattr(requests.exceptions, raised)(f"failed: {url}")

    monkeypatch.setattr("requests.Session.request", fake_request)
    cls = getattr(pytruenas, expected, None) or getattr(builtins, expected)
    with pytest.raises(cls) as caught:
        c.download("config.save")
    assert not isinstance(caught.value, requests.RequestException)
    assert "SECRET-TOKEN" not in str(caught.value)


def test_a_wrapped_socket_error_is_raised_as_it_is(monkeypatch):
    """requests wraps urllib3's error, which wraps the socket's."""
    import requests
    import urllib3

    refused = ConnectionRefusedError(111, "Connection refused")
    try:
        try:
            raise refused
        except OSError as exc:
            raise urllib3.exceptions.NewConnectionError(None, "no connection") from exc
    except urllib3.exceptions.NewConnectionError as exc:
        wrapped = requests.ConnectionError(
            urllib3.exceptions.MaxRetryError(None, "/_download/5", reason=exc)
        )

    c = TrueNASClient(None, autologin=False)
    c.api = MagicMock()
    c.api.core.download.return_value = (5, "/_download/5?auth_token=T")

    def fake_request(self, method, url, **kwargs):
        raise wrapped

    monkeypatch.setattr("requests.Session.request", fake_request)
    with pytest.raises(ConnectionRefusedError) as caught:
        c.download("config.save")
    assert caught.value is refused


def test_upload_generates_token_when_absent(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    c.api = MagicMock()
    c.api.auth.generate_token.return_value = "gen-tok"
    captured = {}

    def fake_request(method, url, headers=None, verify=None, files=None, timeout=None):
        captured["headers"] = headers
        captured["files"] = files
        return MagicMock(json=lambda: {"job_id": 3})

    monkeypatch.setattr(
        "requests.Session.request", lambda self, *a, **k: fake_request(*a, **k)
    )
    # a str file is encoded; no token supplied -> generate_token path
    jobid = c.upload("hello", "filesystem.put", wait=False)
    assert jobid == 3
    c.api.auth.generate_token.assert_called_once()
    assert captured["headers"]["Authorization"] == "Token gen-tok"
    assert captured["files"]["file"] == b"hello"


@pytest.mark.parametrize(
    "transfer",
    [
        lambda c: c.upload(b"x", "filesystem.put", foo=1),
        lambda c: c.download("filesystem.get", "/f", foo=1),
    ],
    ids=["upload", "download"],
)
def test_a_side_channel_takes_no_stray_keyword(transfer):
    """A keyword reached `auth.generate_token`/`core.download`, which refused it
    naming a method the caller never called."""
    c = TrueNASClient("wss://nas", autologin=False)
    c._conn = MagicMock()
    with pytest.raises(TypeError, match="unexpected keyword argument 'foo'"):
        transfer(c)
    assert not c._conn.call.called


# --------------------------------------------------------------- dump_api ----


def test_dump_api_compresses_on_the_target_and_verifies_the_transfer(
    monkeypatch, tmp_path
):
    """The dump is built and gzipped on the target, then fetched and checked.

    It used to capture ``middlewared --dump-api`` straight from ``run()``'s
    stdout, which cannot work: the dump is 24 MB on 26.0 and pushing that
    through the web shell's PTY lost the connection, so a host with no SSH --
    the case the web shell exists for -- could not dump its API at all.
    """
    import gzip
    import hashlib
    import json

    monkeypatch.setenv("PYTRUENAS_CACHE", str(tmp_path))
    blob = gzip.compress(json.dumps({"versions": []}).encode())
    digest = hashlib.sha256(blob).hexdigest()
    commands = []

    def fake_run(self, cmd, *a, **k):
        commands.append(cmd)
        if "--dump-api" in cmd:
            gz = "/var/db/system/pytruenas-apidump.Ab12Cd.gz"  # what mktemp named
            out = f"{gz}\n{len(blob)}\n{digest}\n"
            return subprocess.CompletedProcess(cmd, 0, out, "")
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(TrueNASClient, "run", fake_run)
    monkeypatch.setattr(
        TrueNASClient, "path", lambda self, p, backend=None: _FakeBlob(blob)
    )

    c = TrueNASClient(None, autologin=False)
    # cache=False keeps this off the version lookup, which would need a live API.
    assert c.dump_api(cache=False) == {"versions": []}
    assert any("gzip -9" in cmd for cmd in commands)
    assert any(cmd.startswith("rm -f ") for cmd in commands)


class _FakeBlob:
    def __init__(self, blob):
        self._blob = blob

    def read_bytes(self):
        return self._blob


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
    assert [p.name for p in c.executor_providers] == ["local"]


def test_remote_client_carries_the_target():
    c = TrueNASClient(
        "wss://nas", credentials="1-" + "a" * 64, autologin=False, verify=False
    )
    assert c._config.host == "nas"
    assert not c._config.is_local
    assert c._config.verify is False


def test_verify_is_one_value_for_every_transport():
    # Every leg -- the web shell, the JSON-RPC and REST legs -- reads
    # `client.config.verify`, the one value the caller set.
    c = TrueNASClient(
        "wss://nas", credentials="1-" + "a" * 64, autologin=False, verify=False
    )
    assert c.config.verify is False
    d = TrueNASClient("wss://nas", credentials="1-" + "a" * 64, autologin=False)
    assert d.config.verify is True


def _webshell_sslopt(monkeypatch, **kwargs) -> dict:
    """Run WebShellSession.connect() against a stub and report the sslopt used."""
    import sys
    import types

    from pytruenas.webshell import WebShellSession

    seen: dict = {}

    class _StubWS:
        def __init__(self, sslopt=None):
            seen["sslopt"] = sslopt
            self.frames = ['{"msg": "connected", "id": "shell-1"}']

        def connect(self, uri, **options):
            seen["connect_timeout"] = options.get("timeout")

        def send(self, payload):
            pass

        def settimeout(self, timeout):
            pass

        def recv(self):
            # The session's greeting, then the end of the banner drain loop:
            # connect() reads until it times out.
            if self.frames:
                return self.frames.pop()
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
    # Opening the shell must not block forever on an unresponsive endpoint.
    assert seen["connect_timeout"] and seen["connect_timeout"] > 0
    return seen["sslopt"]


def test_webshell_sslopt_follows_the_flag(monkeypatch):
    import ssl

    # verify=False must reach the socket the web shell actually opens --
    # this is the leg that was reading a nonexistent client attribute.
    assert _webshell_sslopt(monkeypatch, verify=False) == {"cert_reqs": ssl.CERT_NONE}
    # A caller's context is the one the web shell uses.
    mine = ssl.create_default_context()
    assert _webshell_sslopt(monkeypatch, verify=mine) == {"context": mine}
    # Verifying: the shared context (pytruenas._tls), not ad-hoc options.
    assert set(_webshell_sslopt(monkeypatch)) == {"context"}


@pytest.mark.requires("asyncssh")
def test_shell_string_becomes_an_ssh_leg():
    c = TrueNASClient("wss://nas", autologin=False, shell="ssh://root:pw@nas")
    ssh = c._config.ssh
    assert ssh is not None
    assert (ssh.host, ssh.username, ssh.password) == ("nas", "root", "pw")
    assert "ssh" in [p.name for p in c.executor_providers]


def test_client_keys_encoding_is_unpacked_into_a_real_field():
    """`client_keys|root` was a string hack; SSHConfig has a real field."""
    c = TrueNASClient(
        "wss://nas", autologin=False, shell="ssh://client_keys|root:PRIVATEKEY@nas"
    )
    ssh = c._config.ssh
    assert ssh.username == "root"
    assert ssh.client_keys == [b"PRIVATEKEY"]
    assert ssh.password is None


# ------------------------------------------------------------------- wait ----
#
# `core.job_wait` is itself a job, so calling it returned a new job id at once
# instead of blocking (measured on 26.0.0-BETA.1) -- every "wait" returned
# before the job finished. `wait`/`job_updates` poll `core.get_jobs` instead.


def _job_client(monkeypatch, *records):
    """A client whose `core.get_jobs` answers with `records`, one per poll."""
    monkeypatch.setattr("time.sleep", lambda _s: None)
    c = TrueNASClient("wss://nas", autologin=False)
    feed = iter(records)
    polls = []

    def get_jobs(filters):
        polls.append(filters)
        return [next(feed)]

    c.api = MagicMock()
    c.api.core.get_jobs.side_effect = get_jobs
    return c, polls


def _job(state, percent=0, text="", **extra):
    return {
        "id": 5,
        "state": state,
        "progress": {"percent": percent, "description": text},
        **extra,
    }


def test_job_updates_yield_each_change_once_and_end_with_the_final_record(
    monkeypatch,
):
    c, polls = _job_client(
        monkeypatch,
        _job("WAITING"),
        _job("RUNNING", 10, "copying"),
        _job("RUNNING", 10, "copying"),  # unchanged: not yielded again
        _job("RUNNING", 60, "copying"),
        _job("SUCCESS", 100, "done", result={"ok": 1}),
    )
    seen = [(j["state"], j["progress"]["percent"]) for j in c.job_updates(5)]
    assert seen == [("WAITING", 0), ("RUNNING", 10), ("RUNNING", 60), ("SUCCESS", 100)]
    assert polls[0] == [["id", "=", 5]] and len(polls) == 5


def test_wait_reports_progress_to_a_callback_and_returns_the_result(monkeypatch):
    c, _ = _job_client(
        monkeypatch,
        _job("RUNNING", 50, "half"),
        _job("SUCCESS", 100, "done", result=["a"]),
    )
    progress = []
    assert c.wait(5, callback=lambda job: progress.append(job["progress"]["percent"]))
    assert progress == [50, 100]


def test_wait_raises_jobfailed_with_the_middleware_errno(monkeypatch):
    from pytruenas.connection import JobFailed

    failed = _job(
        "FAILED",
        error="[EFAULT] Service not running after start",
        exc_info={"type": "CallError", "errno": 14, "extra": None},
    )
    c, _ = _job_client(monkeypatch, _job("RUNNING"), failed)
    with pytest.raises(JobFailed) as caught:
        c.wait(5)
    assert caught.value.errno == 14
    assert "Service not running" in str(caught.value)
    assert caught.value.job["state"] == "FAILED"


def test_wait_times_out_without_stopping_the_job(monkeypatch):
    from pytruenas.connection import CallTimeout

    c, _ = _job_client(monkeypatch, *[_job("RUNNING", i) for i in range(100)])
    with pytest.raises(CallTimeout):
        c.wait(5, timeout=0)
