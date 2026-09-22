"""Connection lifecycle: what a dropped connection does to a call, what a bad
message does to the reader, and whether the socket is ever released.

Each of these was a way for the connection to end up wedged, leaked, or to have
a non-idempotent call run twice.
"""

import errno
import threading

import pytest

from pytruenas import connection as jsonrpc
from pytruenas.connection import ConnectionClosed, TrueNASWSConnection as Client
from test_jsonrpc_client import _FakeWS, _client_with


def test_a_call_lost_after_sending_says_so():
    """The server may have run it, so the retry layer must not replay it."""
    fake = _FakeWS()
    fake.responder = lambda req: None  # accept the request, answer nothing
    c = _client_with(fake)
    done = []

    def call():
        try:
            c.call("user.create", {"username": "bob"}, timeout=5)
        except Exception as exc:  # noqa: BLE001
            done.append(exc)

    t = threading.Thread(target=call)
    t.start()
    while not fake.sent:
        pass
    fake.close()  # the connection drops with the request in flight
    t.join(5)
    assert len(done) == 1 and isinstance(done[0], ConnectionClosed)
    assert done[0].sent is True and done[0].errno == errno.ECONNABORTED


def test_a_call_on_a_closed_connection_was_never_sent():
    fake = _FakeWS()
    c = _client_with(fake)
    fake.close()
    c._reader.join(5)
    # timeout=None would hang forever if the check-and-register raced.
    with pytest.raises(ConnectionClosed) as ei:
        c.call("user.query", timeout=None)
    assert ei.value.sent is False and not fake.sent


def test_a_send_failure_was_never_sent():
    fake = _FakeWS()
    c = _client_with(fake)

    def boom(_data):
        raise OSError("broken pipe")

    fake.send = boom
    with pytest.raises(ConnectionClosed) as ei:
        c.call("user.query")
    assert ei.value.sent is False
    c.close()


def test_a_parameter_json_cannot_encode_is_the_callers_error():
    """It was reported as ECONNABORTED -- so the retry layer reconnected and
    sent it again -- rather than as a bad argument."""
    fake = _FakeWS()
    c = _client_with(fake)
    try:
        with pytest.raises(TypeError, match="not JSON-encodable"):
            c.call("user.create", object())
        assert not fake.sent and not c._closed.is_set() and not c._pending
    finally:
        c.close()


def test_the_reader_survives_a_failing_subscription_callback():
    """An exception outside recv() killed the reader without running its tail:
    the connection was never marked closed and every later call hung."""
    fake = _FakeWS()
    fake.responder = lambda req: {"jsonrpc": "2.0", "id": req["id"], "result": 1}
    c = _client_with(fake)
    try:
        c.subscribe("alert.list", callback=lambda event: 1 / 0)
        fake.push(
            jsonrpc.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "collection_update",
                    "params": {"collection": "alert.list", "msg": "added"},
                }
            )
        )
        # A notification with no params dict used to raise here too.
        fake.push(
            jsonrpc.dumps(
                {"jsonrpc": "2.0", "method": "collection_update", "params": 5}
            )
        )
        assert c.call("core.ping") == 1
        assert c._reader.is_alive()
    finally:
        c.close()


def test_a_blocking_call_from_a_callback_is_refused_not_deadlocked():
    fake = _FakeWS()
    fake.responder = lambda req: {"jsonrpc": "2.0", "id": req["id"], "result": 1}
    c = _client_with(fake)
    failures = []
    try:
        c.subscribe(
            "alert.list",
            callback=lambda event: failures.append(
                _capture(lambda: c.call("core.ping"))
            ),
        )
        fake.push(
            jsonrpc.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "collection_update",
                    "params": {"collection": "alert.list"},
                }
            )
        )
        c.call("core.ping")  # ordered after the notification on the reader
        assert failures and isinstance(failures[0], RuntimeError)
        assert "subscription callback" in str(failures[0])
    finally:
        c.close()


def _capture(fn):
    try:
        fn()
    except BaseException as exc:  # noqa: BLE001
        return exc
    return None


def test_a_server_close_releases_the_socket():
    """close() returned early once the reader had set _closed, so a connection
    the server dropped kept its socket (and its fd) for the process' life."""
    fake = _FakeWS()
    c = _client_with(fake)
    fake.close()
    c._reader.join(5)
    assert getattr(fake, "shutdowns", 0) == 1
    c.close()  # still idempotent
    assert fake.shutdowns == 1


def test_close_releases_the_socket_once():
    fake = _FakeWS()
    c = _client_with(fake)
    c.close()
    c.close()
    assert fake.shutdowns == 1


def test_opening_a_connection_has_a_timeout(monkeypatch):
    """Without one, an unresponsive host blocked the caller forever; the value
    must not stay on as the reader's recv timeout."""
    seen = {}

    class _WS:
        def __init__(self, sslopt=None):
            pass

        def connect(self, uri, timeout=None, **kw):
            seen["timeout"] = timeout

        def settimeout(self, value):
            seen["settimeout"] = value

        def recv(self):
            raise OSError("done")

        def shutdown(self):
            pass

    monkeypatch.setattr(jsonrpc._websocket, "WebSocket", _WS)
    Client("wss://nas/api/current", connect_timeout=7)
    assert seen == {"timeout": 7, "settimeout": None}
