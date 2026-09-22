"""Logging in, reconnecting and the lazy connection (host.login / host.conn)."""

import threading
import time

import pytest

from pytruenas import TrueNASClient
from pytruenas.auth import ApiKeyAuth, AuthenticationError, Credentials


class _Conn:
    """A stand-in websocket connection: only what login/conn look at."""

    opened = 0

    def __init__(self, delay=0.0):
        time.sleep(delay)
        type(self).opened += 1
        self._closed = threading.Event()

    def close(self):
        self._closed.set()


class _Creds(Credentials):
    """Records each login and answers like the legacy methods do."""

    def __init__(self, result=True):
        self.result = result
        self.calls = []

    def login(self, client):
        self.calls.append(("login", client.conn))
        return self.result

    def login_ex(self, client, *, login_options=None, otp_provider=None):
        self.calls.append(("login_ex", login_options, otp_provider))
        return {"response_type": "SUCCESS"}


@pytest.fixture
def host(monkeypatch):
    _Conn.opened = 0
    h = TrueNASClient("wss://nas", autologin=False)
    monkeypatch.setattr(h, "_openwss", _Conn)
    return h


def test_a_refused_legacy_login_raises_and_closes(host, monkeypatch):
    """auth.login_with_api_key answers a wrong key with False (measured on
    26.0), which was ignored: the session stayed open and unauthenticated."""
    creds = ApiKeyAuth("1-" + "x" * 64)
    monkeypatch.setattr(
        type(host), "api", property(lambda self: _Api(lambda *a: False))
    )
    with pytest.raises(AuthenticationError, match="login_with_api_key failed"):
        host.login(creds)
    assert host._conn is None and host._last_login is None


class _Api:
    def __init__(self, answer):
        self.auth = {"login_with_api_key": answer, "login": answer}


def test_a_successful_legacy_login_returns_its_result(host, monkeypatch):
    monkeypatch.setattr(type(host), "api", property(lambda self: _Api(lambda *a: True)))
    assert host.login(ApiKeyAuth("1-" + "x" * 64)) is True


def test_a_reconnect_repeats_the_login_that_was_used(host):
    """It used the config's credentials, or none at all with autologin=False,
    so a dropped session came back unauthenticated or as someone else."""
    creds = _Creds()
    otp = lambda: "123456"  # noqa: E731
    host.login(
        creds, login_ex=True, login_options={"user_info": False}, otp_provider=otp
    )
    host._conn.close()  # the server dropped it
    host.conn
    assert creds.calls == [("login_ex", {"user_info": False}, otp)] * 2
    assert _Conn.opened == 2


def test_no_login_means_no_replay(host):
    host.conn
    host._conn.close()
    host.conn
    assert _Conn.opened == 2 and host._last_login is None


def test_concurrent_first_use_opens_one_connection(host, monkeypatch):
    """Unlocked, every thread saw no connection and opened its own; all but
    one were leaked."""
    monkeypatch.setattr(host, "_openwss", lambda: _Conn(delay=0.05))
    seen = []
    threads = [
        threading.Thread(target=lambda: seen.append(host.conn)) for _ in range(8)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert _Conn.opened == 1
    assert len({id(c) for c in seen}) == 1
