"""What `_create`/`_upsert`/`_update` put on the wire.

Driven through the real `Namespace` over a faked `conn.call`, so the
assertion is the `(method, params)` the middleware would receive, not that a
mocked helper was called.
"""

import pytest

from pytruenas import TrueNASClient


class _Collection:
    """A faked `conn` serving one collection, `group`, holding `records`."""

    def __init__(self, *records):
        self.records = list(records)
        self.wire = []
        self._closed = type("Open", (), {"is_set": lambda self: False})()

    def call(self, method, *params, **kwds):
        self.wire.append((method, params))
        if method == "group.query":
            filters = params[0] if params else []
            rows = [
                r for r in self.records if all(r.get(k) == v for k, _op, v in filters)
            ]
            return rows[:1]
        if method == "group.get_instance":
            return next(r for r in self.records if r["id"] == params[0])
        if method == "group.create":
            created = {"id": 9, **params[0]}
            self.records.append(created)
            return created
        if method == "group.update":
            record = next(r for r in self.records if r["id"] == params[0])
            record.update(params[1])
            return record
        raise AssertionError(f"unexpected call {method}{params}")

    def sent(self, method):
        return [params for name, params in self.wire if name == method]


def _group(collection):
    host = TrueNASClient("wss://nas.example", autologin=False)
    host._conn = collection
    return host.api.group


def test_create_sends_every_field():
    collection = _Collection()
    result = _group(collection)._create(name="svc", gid=5000, smb=False)
    assert collection.sent("group.create") == [
        ({"name": "svc", "gid": 5000, "smb": False},)
    ]
    assert result == {"id": 9, "name": "svc", "gid": 5000, "smb": False}


def test_create_leaves_out_the_id_and_create_exclude():
    collection = _Collection()
    _group(collection)._create(
        ("create_exclude", ["sudo"]), id=4, name="svc", sudo=True
    )
    assert collection.sent("group.create") == [({"name": "svc"},)]


def test_upsert_of_a_missing_record_creates_it_with_every_field():
    collection = _Collection({"id": 1, "name": "other", "gid": 1})
    _group(collection)._upsert(("name",), name="svc", gid=5000)
    assert collection.sent("group.query") == [([("name", "=", "svc")], {"limit": 1})]
    assert collection.sent("group.create") == [({"name": "svc", "gid": 5000},)]
    assert not collection.sent("group.update")


def test_upsert_of_an_existing_record_updates_only_what_differs():
    collection = _Collection({"id": 1, "name": "svc", "gid": 1, "smb": False})
    result = _group(collection)._upsert(("name",), name="svc", gid=5000, smb=False)
    assert collection.sent("group.update") == [(1, {"gid": 5000})]
    assert not collection.sent("group.create")
    assert result["gid"] == 5000


def test_upsert_with_nothing_to_change_sends_no_write():
    collection = _Collection({"id": 1, "name": "svc", "gid": 5000})
    _group(collection)._upsert(("name",), name="svc", gid=5000)
    assert not collection.sent("group.update")
    assert not collection.sent("group.create")


def test_update_of_a_missing_record_raises_without_creating():
    collection = _Collection()
    with pytest.raises(FileNotFoundError):
        _group(collection)._update(("name",), name="svc", gid=5000)
    assert not collection.sent("group.create")
