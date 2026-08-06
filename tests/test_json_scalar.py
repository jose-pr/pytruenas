"""Wrapper objects reach the API as the scalars it expects.

The natural way to hold a value in Python is often a small wrapper --
`IPv4Address`, a MAC type, a `PurePath`, a domain object around a string. Two
things then go wrong without normalization:

* serializing raises `TypeError: not JSON serializable`, so the call fails; and
* `diff()` compares the wrapper against the plain string the API reported, they
  are never equal, and the field looks changed on every call -- so an upsert
  rewrites it forever and reports a change that did not happen.

The ordering constraint is the subtle part: the middleware's EXTENDED types
(datetime, set, IP *interface*) round-trip through wrapper objects like
`{"$date": ...}` and must keep that exact shape. A blanket `str()` ahead of
them would silently send the wrong form, so the fallback runs only after they
are handled.
"""

import pathlib
from datetime import date, datetime, time, timezone
from ipaddress import IPv4Address, IPv4Interface, IPv6Interface

import pytest

from pytruenas.connection import dumps, loads
from pytruenas.utils.io import json_scalar
from pytruenas.utils.query import diff


class Mac:
    """A wrapper with no __json__ -- str() is the right answer."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Structured:
    """A type that declares its own JSON form, and it is not a string."""

    def __json__(self):
        return {"kind": "structured", "n": 1}


class Exploding:
    def __json__(self):
        raise RuntimeError("boom")


# -- json_scalar ------------------------------------------------------------


def test_uses_dunder_json_when_present():
    assert json_scalar(Structured()) == {"kind": "structured", "n": 1}


def test_dunder_json_may_return_a_non_string():
    """The whole point of the hook: str() cannot express a dict or a list."""
    assert isinstance(json_scalar(Structured()), dict)


def test_falls_back_to_str_for_a_plain_wrapper():
    assert json_scalar(Mac("aa:bb:cc:dd:ee:ff")) == "aa:bb:cc:dd:ee:ff"
    assert json_scalar(IPv4Address("10.0.0.1")) == "10.0.0.1"
    assert json_scalar(pathlib.PurePosixPath("/mnt/tank")) == "/mnt/tank"


def test_dunder_json_is_read_from_the_type_not_the_instance():
    """A mapping carrying a '__json__' KEY is not implementing the protocol."""
    assert json_scalar({"__json__": "not a hook"}) == {"__json__": "not a hook"}


def test_json_native_values_are_left_alone():
    for value in ("s", 1, 1.5, True, None):
        assert json_scalar(value) is value


def test_a_raising_dunder_json_is_not_swallowed():
    """It is an explicit claim the type can serialize itself; a failure is a bug.

    Falling back to str() here would send a repr-ish string to the API.
    """
    with pytest.raises(RuntimeError, match="boom"):
        json_scalar(Exploding())


# -- serialization ----------------------------------------------------------


def test_wrappers_serialize_instead_of_raising():
    assert loads(dumps({"ip": IPv4Address("10.0.0.1")})) == {"ip": "10.0.0.1"}
    assert loads(dumps({"mac": Mac("aa:bb")})) == {"mac": "aa:bb"}
    assert loads(dumps({"p": pathlib.PurePosixPath("/mnt/x")})) == {"p": "/mnt/x"}


def test_dunder_json_survives_serialization():
    assert loads(dumps({"w": Structured()})) == {"w": {"kind": "structured", "n": 1}}


@pytest.mark.parametrize(
    "value",
    [
        datetime(2026, 1, 1, tzinfo=timezone.utc),
        date(2026, 1, 1),
        time(1, 2, 3),
        {1, 2},
        IPv4Interface("10.0.0.1/24"),
        IPv6Interface("::1/128"),
    ],
)
def test_extended_types_keep_their_wrapper_form(value):
    """The ordering guard: these must NOT be flattened to str by the fallback.

    Each round-trips through its own {"$...": ...} envelope; a blanket str()
    ahead of them would send text where the middleware expects the envelope.
    """
    assert loads(dumps({"v": value})) == {"v": value}


def test_an_unserializable_native_still_raises():
    """The fallback must not turn a genuine encoder error into a silent str()."""

    with pytest.raises(TypeError):
        dumps({"v": object().__reduce__})


# -- diff -------------------------------------------------------------------


def test_diff_ignores_a_wrapper_that_matches_the_reported_value():
    """Otherwise the field is 'changed' forever and every upsert rewrites it."""
    assert diff({"ip": "10.0.0.1"}, {"ip": IPv4Address("10.0.0.1")}) == {}


def test_diff_still_reports_a_real_change():
    wanted = IPv4Address("10.0.0.9")
    assert diff({"ip": "10.0.0.1"}, {"ip": wanted}) == {"ip": wanted}


def test_diff_keeps_the_callers_original_value():
    """Comparison normalizes; the value SENT is whatever the caller passed."""
    wanted = IPv4Address("10.0.0.9")
    assert diff({"ip": "10.0.0.1"}, {"ip": wanted})["ip"] is wanted


def test_diff_reports_a_missing_field_as_changed():
    assert diff({}, {"ip": IPv4Address("10.0.0.1")}) != {}


def test_diff_treats_an_unnormalizable_value_as_changed():
    """Reporting a spurious change is recoverable; skipping a real one is not."""
    value = Exploding()
    assert diff({"v": "anything"}, {"v": value}) == {"v": value}


def test_diff_is_unchanged_for_ordinary_scalars():
    assert diff({"a": 1, "b": "x"}, {"a": 1, "b": "x"}) == {}
    assert diff({"a": 1}, {"a": 2}) == {"a": 2}
