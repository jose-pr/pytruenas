"""A peer that stops reading cannot hold a call, or close(), past its timeout.

The peer is a websocket whose send blocks until the socket is shut down, which
is what a blocking send does once a peer that stopped reading has filled the
socket buffers (measured over TLS on loopback: `call(16 MB, timeout=3)` and a
`close()` behind it both blocked for good).
"""

import threading
import time

import pytest

from pytruenas.connection import CallTimeout, ConnectionClosed, TrueNASWSConnection


class _DeafPeerWS:
    def __init__(self):
        self.down = threading.Event()

    def send(self, payload):
        self.down.wait()
        raise OSError("socket shut down")

    def recv(self):
        self.down.wait()
        raise OSError("socket shut down")

    def shutdown(self):
        self.down.set()

    def close(self):
        if not self.down.is_set():
            raise AssertionError("close() reached the websocket under a blocked send")


@pytest.fixture
def conn(monkeypatch):
    monkeypatch.setattr(TrueNASWSConnection, "_connect", lambda self: _DeafPeerWS())
    conn = TrueNASWSConnection("ws://nas/api/current").connect()
    yield conn
    conn.close()


def test_a_send_blocked_past_the_timeout_raises_call_timeout(conn):
    """The call's timeout covered only the wait for the response."""
    started = time.monotonic()
    with pytest.raises(CallTimeout):
        conn.call("filesystem.put", "x", timeout=0.5)
    assert time.monotonic() - started < 5
    assert conn._closed.is_set()  # the frame may be half sent: unusable


def test_close_does_not_wait_for_a_blocked_send(conn):
    raised = []

    def send():
        try:
            conn.call("filesystem.put", "x", timeout=None)
        except ConnectionClosed as exc:
            raised.append(exc)

    sender = threading.Thread(target=send, daemon=True)
    sender.start()
    time.sleep(0.2)
    started = time.monotonic()
    conn.close()
    assert time.monotonic() - started < 5
    sender.join(5)
    assert raised and not sender.is_alive()


def test_building_a_connection_does_no_io(monkeypatch):
    opened = []
    monkeypatch.setattr(
        TrueNASWSConnection, "_connect", lambda self: opened.append(1) or _DeafPeerWS()
    )
    conn = TrueNASWSConnection("ws://nas/api/current")
    assert opened == []
    with conn:
        assert opened == [1]
