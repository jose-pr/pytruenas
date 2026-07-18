"""Query filter / option / diff helpers (utils.query)."""

from pytruenas.utils import query as q


def test_eq_filter_from_kwargs():
    filters = q.filter_from_kwargs(username="root", uid=0)
    assert ("username", "=", "root") in filters
    assert ("uid", "=", 0) in filters


def test_explicit_operators():
    filters = q.filter_from_kwargs(uid=q.GT(1000), name=q.RE("^ad"))
    assert ("uid", ">", 1000) in filters
    assert ("name", "~", "^ad") in filters


def test_exclude_is_dropped():
    filters = q.filter_from_kwargs(a=1, b=q.EXCLUDE)
    assert filters == [("a", "=", 1)]


def test_options_merge():
    opts = q.Option.options({"limit": 1}, ("offset", 5), q.Option("count", True))
    assert opts == {"limit": 1, "offset": 5, "count": True}


def test_diff():
    base = {"a": 1, "b": 2, "c": 3}
    against = {"a": 1, "b": 20, "d": 4}
    assert q.diff(base, against) == {"b": 20, "d": 4}


def test_in_nin():
    filters = q.filter_from_kwargs(id=q.IN([1, 2]), name=q.NIN(["x"]))
    assert ("id", "in", [1, 2]) in filters
    assert ("name", "nin", ["x"]) in filters
