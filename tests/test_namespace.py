"""Namespace attribute proxy + DbAction (create/update/upsert/get) logic.

All mocked at ``client.websocket.call`` -- no server. Exercises the method
name-building, the ``_query``/``_get`` filter shaping, and the
create/update/upsert decision tree in ``DbAction.execute``.
"""

from unittest.mock import MagicMock

import pytest

from pytruenas.namespace import DbAction, Namespace
from pytruenas.utils import query as q


def _client():
    """A client whose websocket.call records (method, args, kwargs) and returns
    a configurable value."""
    client = MagicMock()
    client.logger = MagicMock()
    return client


def test_attribute_access_builds_dotted_method():
    ns = Namespace(_client())
    assert str(ns.user) == "user"
    assert str(ns.pool.dataset) == "pool.dataset"


def test_call_invokes_websocket_with_method_name():
    client = _client()
    client.websocket.call.return_value = [{"id": 1}]
    ns = Namespace(client, "user")
    result = ns.query([], {})
    assert result == [{"id": 1}]
    method = client.websocket.call.call_args[0][0]
    assert method == "user.query"


def test_query_builds_filters_from_kwargs():
    client = _client()
    client.websocket.call.return_value = []
    Namespace(client, "user")._query(username="root", uid=q.GT(0))
    method, filters, opts = client.websocket.call.call_args[0]
    assert method == "user.query"
    assert ("username", "=", "root") in filters
    assert ("uid", ">", 0) in filters


def test_get_by_id_uses_get_instance():
    client = _client()
    client.websocket.call.return_value = {"id": 7, "username": "svc"}
    got = Namespace(client, "user")._get(7)
    assert got == {"id": 7, "username": "svc"}
    assert client.websocket.call.call_args[0][0] == "user.get_instance"


def test_get_by_filter_uses_query_limit_1():
    client = _client()
    client.websocket.call.return_value = [{"id": 7, "username": "svc"}]
    got = Namespace(client, "user")._get(username="svc")
    assert got == {"id": 7, "username": "svc"}
    assert client.websocket.call.call_args[0][0] == "user.query"


def test_get_id_and_filter_together_raises():
    with pytest.raises(ValueError):
        Namespace(_client(), "user")._get(7, username="svc")


def test_get_missing_returns_none():
    client = _client()
    # get_instance raising FileNotFoundError (via _ioerror) -> None
    ns = Namespace(client, "user")
    ns.get_instance = MagicMock(side_effect=FileNotFoundError())
    assert ns._get(999) is None


# -- DbAction.execute decision tree -------------------------------------------


def _namespace_with(existing=None, create_ret=1, update_ret=1):
    """A Namespace with _get/create/update/config stubbed for DbAction tests."""
    client = _client()
    ns = Namespace(client, "user")
    ns._get = MagicMock(return_value=existing)
    ns.create = MagicMock(return_value=create_ret)
    ns.update = MagicMock(return_value=update_ret)
    ns.config = MagicMock(return_value={})
    # job_wait passthrough (results here aren't ints needing a wait)
    return ns, client


def test_upsert_creates_when_absent():
    # A tuple selector ("username",) resolves the row by that field; _get None
    # (absent) + UPSERT -> create.
    ns, _ = _namespace_with(existing=None)
    ns._upsert(("username",), username="svc", full_name="Service")
    ns.create.assert_called_once()
    ns.update.assert_not_called()


def test_upsert_updates_when_present():
    # _get returns an existing row -> UPSERT updates it (diff of changed fields).
    ns, _ = _namespace_with(existing={"id": 5, "username": "svc", "full_name": "old"})
    ns._upsert(("username",), username="svc", full_name="new")
    ns.update.assert_called_once()
    ns.create.assert_not_called()


def test_update_on_absent_selector_raises_not_found():
    # _update (not upsert) with a tuple selector whose row does not exist ->
    # FileNotFoundError (update must not create).
    ns, _ = _namespace_with(existing=None)
    with pytest.raises(FileNotFoundError):
        DbAction.UPDATE.execute(ns, ("username",), username="ghost")
