"""Namespace child-cache hygiene + ioerror mapping (ops_hardening plan)."""

import errno
import gc
import weakref
from unittest.mock import MagicMock

from pytruenas import _conn
from pytruenas.namespace import Namespace, ioerror


def test_children_are_cached_per_instance():
    ns = Namespace(MagicMock(), "pool")
    a = ns.dataset
    b = ns.dataset
    assert a is b  # same child returned (cache hit)
    assert ns["dataset"] is a


def test_namespaces_are_collectable_after_client_drop():
    # functools.cache on the methods used to pin every Namespace for the process
    # lifetime (keyed on self). A per-instance dict must let them be collected.
    ns = Namespace(MagicMock(), "pool")
    child = ns.dataset.snapshot
    ref = weakref.ref(child)
    del ns, child
    gc.collect()
    assert ref() is None  # collected, not pinned by a global cache


def test_ioerror_maps_known_errno():
    err = _conn.ClientException.__new__(_conn.ClientException)
    err.error = "[EEXIST] file already exists"
    mapped = ioerror(err)
    assert isinstance(mapped, OSError)
    assert mapped.errno == errno.EEXIST


def test_ioerror_unknown_prefix_returns_original():
    # A bracketed prefix that is NOT a real errno name must return the original
    # exception (previously it produced IOError(None, msg), losing the type).
    err = _conn.ClientException.__new__(_conn.ClientException)
    err.error = "[ENOTAREALERRNO] something"
    assert ioerror(err) is err


def test_ioerror_no_bracket_returns_original():
    err = _conn.ClientException.__new__(_conn.ClientException)
    err.error = "plain message, no bracket"
    assert ioerror(err) is err
