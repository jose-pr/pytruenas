"""Cases where the client returned or recorded the WRONG value.

Not wrong messages -- wrong answers: a filter that vanished, a timestamp off by
its own milliseconds, a no-op update that rewrote a field forever. Each one is
measured against the released 0.5.0 behaviour in the commit that fixes it.
"""

import datetime as dt
import errno
import threading
from unittest.mock import MagicMock

import pytest

from pytruenas import connection as jsonrpc
from pytruenas.connection import ClientException
from pytruenas.namespace import Namespace
from pytruenas.utils import query as q
from test_jsonrpc_client import _FakeWS, _client_with


def _client():
    c = MagicMock()
    c.logger = MagicMock()
    return c


# -- the call contract ----------------------------------------------------


def test_a_keyword_parameter_is_refused_not_dropped():
    """`query(filters=[...])` sent NO filters and returned every row: the
    keyword reached call()'s **_ignored and was logged at debug level."""
    c = _client()
    with pytest.raises(TypeError, match="positional parameters only"):
        Namespace(c, "user").query(filters=[["uid", "=", 0]])
    assert not c.conn.call.called
    with pytest.raises(TypeError, match="filters"):
        Namespace(c, "user").query(filters=[], options={})


def test_the_transfer_and_timeout_keywords_still_pass():
    c = _client()
    Namespace(c, "core")(_method="ping", _timeout=5)
    assert c.conn.call.call_args[1]["timeout"] == 5
    # The upstream-client compatibility names stay accepted.
    Namespace(c, "core")(_method="ping", job=True)
    # And the transfer helpers keep their own keywords.
    Namespace(c, "filesystem")(_method="get", _filetransfer=True, filename="x")
    assert c.download.called


def test_the_query_helpers_still_take_keywords():
    """`_query`/`_get` build filters FROM keywords -- that is their job."""
    c = _client()
    c.conn.call.return_value = []
    Namespace(c, "user")._query(username="root")
    args = c.conn.call.call_args[0]
    assert args[0] == "user.query" and args[1] == [("username", "=", "root")]


# -- job ids --------------------------------------------------------------


def test_a_boolean_result_is_not_a_job_id():
    """bool is a subclass of int, so a method answering True had its answer
    waited on as job id 1."""
    c = _client()
    ns = Namespace(c, "user")

    def answers(update_result):
        def call(method, *a, **k):
            if method == "user.update":
                return update_result
            return {"id": 7, "locked": False}  # get_instance / query

        return call

    c.conn.call.side_effect = answers(True)
    ns._update(7, locked=True)
    assert not c.wait.called
    # A real job id still waits.
    c.wait.reset_mock()
    c.conn.call.side_effect = answers(42)
    ns._update(7, locked=True)
    c.wait.assert_called_once()
    assert c.wait.call_args[0][0] == 42


def test_updating_a_missing_record_says_which_one():
    """It surfaced as AttributeError from diff(None, ...), naming neither the
    record nor the collection."""
    c = _client()
    c.conn.call.return_value = None  # _get finds nothing
    with pytest.raises(FileNotFoundError, match="user: no record with id=9"):
        Namespace(c, "user")._update(9, locked=True)


# -- ejson ----------------------------------------------------------------


@pytest.mark.parametrize(
    "when",
    [
        dt.datetime(2026, 7, 19, 3, 42, 0, 600000, tzinfo=dt.timezone.utc),
        dt.datetime(2026, 1, 1, 0, 0, 0, 1000, tzinfo=dt.timezone.utc),
        dt.datetime(1969, 12, 31, 23, 59, 59, 250000, tzinfo=dt.timezone.utc),
        dt.datetime(2026, 7, 19, 3, 42, tzinfo=dt.timezone.utc),
    ],
)
def test_a_timestamp_round_trips_with_its_milliseconds(when):
    """The sub-second part was added twice: .600 came back 1.2 s late."""
    assert jsonrpc.loads(jsonrpc.dumps({"t": when}))["t"] == when


def test_an_undecodable_response_fails_its_own_call():
    """The response HAD arrived; dropping it made the caller wait out the whole
    timeout (or forever, with timeout=None)."""
    fake = _FakeWS()
    c = _client_with(fake, call_timeout=5)
    fake.responder = lambda req: None
    out = []

    def call():
        try:
            out.append(c.call("system.info", timeout=5))
        except BaseException as exc:  # noqa: BLE001
            out.append(exc)

    t = threading.Thread(target=call)
    t.start()
    while not fake.sent:
        pass
    import json

    call_id = json.loads(fake.sent[0])["id"]
    fake.push(
        '{"jsonrpc": "2.0", "id": "%s", "result": {"$date": "nonsense"}}' % call_id
    )
    t.join(5)
    assert len(out) == 1 and isinstance(out[0], ClientException)
    assert out[0].errno == errno.EPROTO and "undecodable" in str(out[0])
    # The connection itself is still usable.
    fake.responder = lambda req: {"jsonrpc": "2.0", "id": req["id"], "result": "pong"}
    assert c.call("core.ping") == "pong"
    c.close()


# -- diff -----------------------------------------------------------------


def test_a_property_shaped_value_is_compared_by_its_value():
    """pool.dataset reports a property as {"value": ..., "parsed": ...} while a
    caller sets the scalar, so every upsert rewrote the field and reported a
    change that never happened."""
    current = {
        "quota": {"value": "10G", "parsed": 10737418240, "rawvalue": "10737418240"},
        "comments": {"value": "hi", "parsed": "hi"},
    }
    assert q.diff(current, {"quota": "10G"}) == {}
    assert q.diff(current, {"quota": 10737418240}) == {}
    assert q.diff(current, {"comments": "hi"}) == {}
    # A real change is still reported.
    assert q.diff(current, {"quota": "20G"}) == {"quota": "20G"}


def test_a_partial_dict_compares_on_its_own_keys_only():
    current = {"opts": {"a": 1, "b": 2}}
    assert q.diff(current, {"opts": {"a": 1}}) == {}
    assert q.diff(current, {"opts": {"a": 2}}) == {"opts": {"a": 2}}


def test_the_sentinels_have_the_same_shape():
    """MISSING was a class while EXCLUDE was an instance, so the two read
    differently at every `is` check."""
    assert not isinstance(q.MISSING, type)
    assert q.diff({}, {"x": None}) == {"x": None}  # absent != reported None
    assert not hasattr(q, "merge")  # untested, unused leftover
