"""Namespace.__call__ retry + timeout semantics (jsonrpc_call_reliability).

Regression coverage for the bug where an ECONNABORTED call fell through the
retry loop and returned None (which _get reads as "missing" -> upsert creates a
duplicate). The loop must retry, then RAISE -- never return None.

Only a request the server never received is retried (ConnectionClosed with
sent=False): one lost after sending may already have run, and the retry used to
replay creates, deletes and job starts.
"""

import errno
from unittest.mock import MagicMock

import pytest

from pytruenas import connection as _conn
from pytruenas.namespace import Namespace


def _client():
    c = MagicMock()
    c.logger = MagicMock()
    return c


def _unsent():
    return _conn.ConnectionClosed(sent=False)


def test_permanent_abort_retries_then_raises():
    c = _client()
    c.conn.call.side_effect = _unsent()
    ns = Namespace(c, "user")
    with pytest.raises(_conn.ClientException) as ei:
        ns.query([], {})
    assert ei.value.errno == errno.ECONNABORTED
    # default _tries=1 -> one initial attempt + one retry == 2 calls
    assert c.conn.call.call_count == 2


def test_abort_then_success_returns_result(monkeypatch):
    c = _client()
    calls = {"n": 0}

    def flaky(method, *a, **k):
        calls["n"] += 1
        if calls["n"] == 1:
            raise _unsent()
        return [{"id": 1}]

    c.conn.call.side_effect = flaky
    # avoid the real 1s sleep between attempts
    monkeypatch.setattr("pytruenas.namespace._time.sleep", lambda *_: None)
    ns = Namespace(c, "user")
    assert ns.query([], {}) == [{"id": 1}]
    assert calls["n"] == 2


def test_retry_drops_the_connection_it_used(monkeypatch):
    c = _client()
    c.conn.call.side_effect = _unsent()
    monkeypatch.setattr("pytruenas.namespace._time.sleep", lambda *_: None)
    with pytest.raises(_conn.ClientException):
        Namespace(c, "user").query([], {})
    # the host drops (and closes) exactly the connection the attempt used
    c._drop_conn.assert_called_with(c.conn)


@pytest.mark.parametrize(
    "error",
    [
        _conn.ConnectionClosed(sent=True),
        # A bare ECONNABORTED says nothing about whether it was sent.
        _conn.ClientException("closed", errno.ECONNABORTED),
    ],
)
def test_a_call_that_may_have_run_is_not_replayed(error):
    c = _client()
    c.conn.call.side_effect = error
    with pytest.raises(_conn.ClientException) as ei:
        Namespace(c, "user").create({"username": "bob"})
    assert ei.value.errno == errno.ECONNABORTED
    assert c.conn.call.call_count == 1


def test_non_abort_error_raises_immediately():
    c = _client()
    c.conn.call.side_effect = _conn.ClientException("boom", errno.EINVAL)
    with pytest.raises(_conn.ClientException):
        Namespace(c, "user").query([], {})
    assert c.conn.call.call_count == 1  # no retry for non-abort


def test_timeout_threaded_through_to_call():
    c = _client()
    c.conn.call.return_value = {"ok": True}
    Namespace(c, "core")(_method="ping", _timeout=None)
    # _timeout=None must reach websocket.call as timeout=None (wait forever)
    _, kwargs = c.conn.call.call_args
    assert kwargs.get("timeout") is None


def test_timeout_omitted_by_default():
    c = _client()
    c.conn.call.return_value = {"ok": True}
    Namespace(c, "core")(_method="ping")
    _, kwargs = c.conn.call.call_args
    assert "timeout" not in kwargs  # default sentinel -> client default used
