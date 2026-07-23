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


def test_timeout_none_waits_for_a_delayed_response():
    # timeout=None must wait indefinitely (used by core.job_wait for long jobs),
    # NOT fall back to the default and time out. A response arriving after the
    # client's short default call_timeout (2s here) must still be returned.
    fake = _FakeWS()
    c = _client_with(fake)  # call_timeout=2

    def _answer_late(req):
        # respond after longer than the default timeout would allow
        def _later():
            time.sleep(0.3)
            fake.push(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": "late"}))
        threading.Thread(target=_later, daemon=True).start()
        return None

    fake.responder = _answer_late
    try:
        assert c.call("core.job_wait", timeout=None) == "late"
    finally:
        c.close()


def test_unexpected_kwarg_is_logged_not_swallowed(caplog):
    import logging

    fake = _FakeWS()
    fake.responder = lambda req: {"jsonrpc": "2.0", "id": req["id"], "result": 1}
    c = _client_with(fake)
    try:
        with caplog.at_level(logging.DEBUG, logger="pytruenas.jsonrpc"):
            assert c.call("core.ping", nonsense_kwarg=1) == 1
        assert any("nonsense_kwarg" in r.message for r in caplog.records)
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


# -- event subscriptions ----------------------------------------------------

#: A ``responder`` that answers core.subscribe with a canned id and
#: core.unsubscribe with True, so subscribe()/unsubscribe() complete.
def _subscribe_responder(sub_id="sub-1"):
    def responder(req):
        if req["method"] == "core.subscribe":
            return {"jsonrpc": "2.0", "id": req["id"], "result": sub_id}
        if req["method"] == "core.unsubscribe":
            return {"jsonrpc": "2.0", "id": req["id"], "result": True}
        return {"jsonrpc": "2.0", "id": req["id"], "result": None}
    return responder


def _notification(collection, msg="added", fields=None):
    # An id-less collection_update, exactly as the live middleware sends it.
    return json.dumps({
        "jsonrpc": "2.0",
        "method": "collection_update",
        "params": {"msg": msg, "collection": collection, "fields": fields or {}},
    })


def test_notification_routes_to_subscription():
    fake = _FakeWS()
    fake.responder = _subscribe_responder("id-77")
    c = _client_with(fake)
    try:
        sub = c.subscribe("alert.list")
        assert sub.id == "id-77"
        fake.push(_notification("alert.list", "added", {"id": 5, "level": "WARNING"}))
        events = sub.events(timeout=2)
        ev = next(events)
        assert ev.collection == "alert.list"
        assert ev.msg == "added"
        assert ev.fields == {"id": 5, "level": "WARNING"}
    finally:
        c.close()


def test_notification_fires_callback():
    fake = _FakeWS()
    fake.responder = _subscribe_responder()
    c = _client_with(fake)
    got = []
    try:
        c.subscribe("reporting.realtime", callback=got.append)
        fake.push(_notification("reporting.realtime", "changed", {"cpu": 1}))
        # give the reader thread a moment to route + invoke the callback
        for _ in range(50):
            if got:
                break
            time.sleep(0.02)
        assert len(got) == 1 and got[0].collection == "reporting.realtime"
    finally:
        c.close()


def test_unmatched_notification_dropped_without_disturbing_calls():
    fake = _FakeWS()
    fake.responder = _subscribe_responder()
    c = _client_with(fake)
    try:
        c.subscribe("alert.list")
        # a notification for an event nobody subscribed to
        fake.push(_notification("something.else"))
        # a normal call still resolves (reader unaffected)
        fake.responder = lambda req: {"jsonrpc": "2.0", "id": req["id"], "result": "ok"}
        assert c.call("core.ping") == "ok"
    finally:
        c.close()


def test_two_subscribers_same_collection_both_receive():
    fake = _FakeWS()
    fake.responder = _subscribe_responder()
    c = _client_with(fake)
    try:
        a = c.subscribe("alert.list")
        b = c.subscribe("alert.list")
        fake.push(_notification("alert.list", "removed", {"id": 9}))
        ea = next(a.events(timeout=2))
        eb = next(b.events(timeout=2))
        assert ea.msg == eb.msg == "removed"
    finally:
        c.close()


def test_raising_callback_is_contained():
    fake = _FakeWS()
    fake.responder = _subscribe_responder()
    c = _client_with(fake)
    try:
        def boom(_ev):
            raise RuntimeError("callback blew up")

        c.subscribe("alert.list", callback=boom)
        fake.push(_notification("alert.list"))
        # reader survives: a subsequent call still works
        fake.responder = lambda req: {"jsonrpc": "2.0", "id": req["id"], "result": 1}
        assert c.call("core.ping") == 1
    finally:
        c.close()


def test_queue_full_drops_oldest_and_counts():
    fake = _FakeWS()
    fake.responder = _subscribe_responder()
    c = _client_with(fake)
    try:
        sub = c.subscribe("alert.list", maxsize=2)
        for i in range(5):  # 5 events into a size-2 queue
            fake.push(_notification("alert.list", "added", {"n": i}))
        # let the reader drain the inbox
        for _ in range(50):
            if sub.dropped >= 3:
                break
            time.sleep(0.02)
        assert sub.dropped == 3  # 5 pushed, 2 retained -> 3 dropped
        kept = [ev.fields["n"] for ev in sub.events(timeout=0.2)]
        assert kept == [3, 4]  # the two NEWEST survive (oldest dropped)
    finally:
        c.close()


def test_close_wakes_events_iterator():
    fake = _FakeWS()
    fake.responder = _subscribe_responder()
    c = _client_with(fake)
    sub = c.subscribe("alert.list")
    collected = []

    def _consume():
        for ev in sub.events(timeout=5):
            collected.append(ev)

    t = threading.Thread(target=_consume, daemon=True)
    t.start()
    time.sleep(0.1)
    c.close()  # must wake the blocked events() consumer
    t.join(timeout=3)
    assert not t.is_alive()  # iterator ended cleanly on close


def test_unsubscribe_stops_delivery_and_sends_unsubscribe():
    fake = _FakeWS()
    fake.responder = _subscribe_responder("theid")
    c = _client_with(fake)
    try:
        sub = c.subscribe("alert.list")
        sub.unsubscribe()
        # core.unsubscribe was sent with the returned id
        methods = [json.loads(s) for s in fake.sent]
        unsub = [m for m in methods if m["method"] == "core.unsubscribe"]
        assert unsub and unsub[0]["params"] == ["theid"]
        # a later notification is dropped (no sink)
        fake.push(_notification("alert.list"))
        assert list(sub.events(timeout=0.2)) == []
    finally:
        c.close()
