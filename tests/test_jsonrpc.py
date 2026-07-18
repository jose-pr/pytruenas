"""Lean JSON-RPC client: extended-JSON round-trip and error parsing.

These exercise the pure pieces (ejson + exception mapping) without a live
websocket; connection behavior is covered by integration use against a real
server, not unit tests.
"""

from datetime import date, datetime, time, timezone

import pytest

from pytruenas import jsonrpc
from pytruenas.jsonrpc import (
    ClientException,
    ValidationErrors,
    _parse_error,
    dumps,
    loads,
)


def test_ejson_datetime_roundtrip():
    dt = datetime(2026, 7, 17, 12, 30, 5, tzinfo=timezone.utc)
    assert loads(dumps({"when": dt}))["when"] == dt


def test_ejson_date_roundtrip():
    d = date(2026, 7, 17)
    assert loads(dumps({"d": d}))["d"] == d


def test_ejson_time_roundtrip():
    t = time(16, 22, 6)
    assert loads(dumps({"t": t}))["t"] == t


def test_ejson_set_roundtrip():
    s = {1, 2, 3}
    assert loads(dumps({"s": s}))["s"] == s


def test_plain_json_untouched():
    obj = {"a": 1, "b": [1, 2, {"c": "x"}], "n": None, "ok": True}
    assert loads(dumps(obj)) == obj


def test_parse_validation_error():
    err = _parse_error(
        {
            "code": -32602,
            "message": "Invalid params",
            "data": {"extra": [["user.name", "required", 22]]},
        }
    )
    assert isinstance(err, ValidationErrors)
    assert "user.name" in str(err)


def test_parse_call_error_carries_errno():
    err = _parse_error(
        {
            "code": -32001,
            "data": {"reason": "[EPERM] denied", "error": 1, "trace": None, "extra": []},
        }
    )
    assert isinstance(err, ClientException)
    assert err.errno == 1
    assert "denied" in str(err)


def test_parse_generic_error():
    err = _parse_error({"code": -32603, "message": "boom"})
    assert isinstance(err, ClientException)
    assert str(err) == "boom"


def test_unix_socket_default_uri():
    # Constructing with no uri should target the local socket; we don't connect
    # here (no server), just check the URI is composed. Patch _connect out.
    import threading

    created = {}

    class _FakeWS:
        def recv(self):
            raise OSError("closed")

        def close(self):
            pass

    def fake_connect(self):
        created["uri"] = self.uri
        return _FakeWS()

    orig = jsonrpc.Client._connect
    jsonrpc.Client._connect = fake_connect
    try:
        c = jsonrpc.Client()
        assert created["uri"].startswith("ws+unix://")
        c.close()
    finally:
        jsonrpc.Client._connect = orig
