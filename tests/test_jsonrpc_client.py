"""The lean JSON-RPC Client's call/response/error machinery, with a fake socket.

No real server: a ``_FakeWS`` echoes canned responses so we exercise request
framing, response demux by id, error mapping, timeout, and connection-closed
propagation.
"""

import json
import threading
import time

import pytest

from pytruenas import jsonrpc
from pytruenas.jsonrpc import CallTimeout, Client, ClientException, ValidationErrors


class _FakeWS:
    """A fake websocket: records sent frames, and lets the test push responses
    that the client's reader thread will receive via recv()."""

    def __init__(self):
        self.sent = []
        self._inbox = []
        self._cond = threading.Condition()
        self._closed = False
        self.responder = None  # optional: (request_dict) -> response_dict

    def send(self, data):
        self.sent.append(data)
        if self.responder is not None:
            req = json.loads(data)
            resp = self.responder(req)
            if resp is not None:
                self.push(json.dumps(resp))

    def push(self, raw):
        with self._cond:
            self._inbox.append(raw)
            self._cond.notify_all()

    def recv(self):
        with self._cond:
            while not self._inbox and not self._closed:
                self._cond.wait(timeout=1)
            if self._closed and not self._inbox:
                raise OSError("closed")
            return self._inbox.pop(0)

    def close(self):
        with self._cond:
            self._closed = True
            self._cond.notify_all()


def _client_with(fake):
    """Build a Client whose _connect returns ``fake`` (no real connection)."""
    orig = Client._connect
    Client._connect = lambda self: fake
    try:
        return Client("ws://x/api/current", call_timeout=2)
    finally:
        Client._connect = orig


def test_call_returns_result():
    fake = _FakeWS()
    fake.responder = lambda req: {"jsonrpc": "2.0", "id": req["id"], "result": {"ok": 1}}
    c = _client_with(fake)
    try:
        assert c.call("core.ping") == {"ok": 1}
        # request was well-formed
        sent = json.loads(fake.sent[0])
        assert sent["method"] == "core.ping" and sent["jsonrpc"] == "2.0" and "id" in sent
    finally:
        c.close()


def test_call_ignores_compat_kwargs():
    fake = _FakeWS()
    fake.responder = lambda req: {"jsonrpc": "2.0", "id": req["id"], "result": 42}
    c = _client_with(fake)
    try:
        # job=/background=/callback= are accepted and ignored (upstream-compat).
        assert c.call("core.job_wait", 1, job=True, background=False, callback=None) == 42
    finally:
        c.close()


def test_validation_error_mapped():
    fake = _FakeWS()
    fake.responder = lambda req: {
        "jsonrpc": "2.0", "id": req["id"],
        "error": {"code": -32602, "data": {"extra": [["user.name", "required", 22]]}},
    }
    c = _client_with(fake)
    try:
        with pytest.raises(ValidationErrors):
            c.call("user.create", {})
    finally:
        c.close()


def test_call_error_carries_errno():
    fake = _FakeWS()
    fake.responder = lambda req: {
        "jsonrpc": "2.0", "id": req["id"],
        "error": {"code": -32001, "data": {"reason": "[EPERM] no", "error": 1}},
    }
    c = _client_with(fake)
    try:
        with pytest.raises(ClientException) as ei:
            c.call("something")
        assert ei.value.errno == 1
    finally:
        c.close()


def test_timeout_raises_calltimeout():
    fake = _FakeWS()  # no responder -> the call never gets an answer
    c = _client_with(fake)
    try:
        with pytest.raises(CallTimeout):
            c.call("core.ping", timeout=0.1)
    finally:
        c.close()


def test_closed_connection_fails_pending():
    fake = _FakeWS()
    c = _client_with(fake)
    try:
        # close while a call is waiting -> the waiter is failed with ECONNABORTED.
        def _close_soon():
            time.sleep(0.1)
            fake.close()

        threading.Thread(target=_close_soon, daemon=True).start()
        with pytest.raises(ClientException):
            c.call("core.ping", timeout=2)
    finally:
        c.close()


def test_ejson_roundtrip_over_the_wire():
    from datetime import datetime, timezone

    dt = datetime(2026, 7, 18, 12, 0, 0, tzinfo=timezone.utc)
    fake = _FakeWS()
    fake.responder = lambda req: {"jsonrpc": "2.0", "id": req["id"], "result": req["params"][0]}
    c = _client_with(fake)
    try:
        # a datetime param should serialize out and come back as a datetime.
        assert c.call("echo", dt) == dt
    finally:
        c.close()
