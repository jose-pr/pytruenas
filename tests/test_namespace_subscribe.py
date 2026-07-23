"""Namespace / client subscribe surface (Phase 2 of event subscriptions).

Mocked at ``client.websocket.subscribe`` -- no server. Exercises event-name
derivation from the namespace path and the ``event=`` override; the routing and
queue mechanics live in test_jsonrpc_client.py.
"""

from unittest.mock import MagicMock

import pytest

from pytruenas.namespace import Namespace


def _client():
    client = MagicMock()
    client.logger = MagicMock()
    # websocket.subscribe echoes the event name so we can assert what was passed
    client.websocket.subscribe.side_effect = lambda ev, cb=None, **kw: ("SUB", ev, cb, kw)
    return client


def test_subscribe_derives_event_name_from_namespace_path():
    client = _client()
    ns = Namespace(client, "alert", "list")
    sub = ns.subscribe()
    # the namespace's dotted path is the event name
    assert client.websocket.subscribe.call_args[0][0] == "alert.list"
    assert sub[1] == "alert.list"


def test_subscribe_passes_callback_and_maxsize():
    client = _client()
    cb = lambda ev: None
    ns = Namespace(client, "reporting", "realtime")
    ns.subscribe(cb, maxsize=10)
    args, kwargs = client.websocket.subscribe.call_args
    assert args[0] == "reporting.realtime"
    assert args[1] is cb
    assert kwargs["maxsize"] == 10


def test_subscribe_event_override():
    client = _client()
    # from a different namespace, subscribe to an explicit event name
    ns = Namespace(client, "something")
    ns.subscribe(event="alert.list")
    assert client.websocket.subscribe.call_args[0][0] == "alert.list"


def test_subscribe_on_root_without_event_raises():
    client = _client()
    root = Namespace(client)  # empty namespace path
    with pytest.raises(ValueError):
        root.subscribe()


def test_subscribe_is_a_real_method_not_a_child_namespace():
    # a real method must shadow __getattr__'s child-namespace routing
    client = _client()
    ns = Namespace(client, "alert", "list")
    assert callable(ns.subscribe)
    # ...whereas an unknown attribute IS a child namespace
    assert str(ns.foo) == "alert.list.foo"


def test_client_level_subscribe_delegates_to_websocket():
    from pytruenas.client import TrueNASClient

    client = MagicMock(spec=TrueNASClient)
    # call the real method against a mock self
    TrueNASClient.subscribe(client, "alert.list", None)
    client.websocket.subscribe.assert_called_once()
    assert client.websocket.subscribe.call_args[0][0] == "alert.list"
