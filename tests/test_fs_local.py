"""Local filesystem backend round-trip (no server needed).

The local backend delegates to ``pathlib.Path``; these confirm the multi-backend
``Path`` proxy wires read/write/mkdir/exists through to it for a local client.
"""

from types import SimpleNamespace

import pytest

from pytruenas.fs import Path


def _local_client():
    """A minimal stand-in for TrueNASClient that reports as local."""
    api = SimpleNamespace(is_local=True, host="localhost", port=0)
    return SimpleNamespace(_api=api, fsbackend="local")


def test_write_read_roundtrip(tmp_path):
    client = _local_client()
    p = Path(str(tmp_path), "hello.txt", client=client, backend="local")
    p.write_text("hi there")
    assert p.read_text() == "hi there"
    assert p.exists()
    assert p.is_file()


def test_write_returns_bytes(tmp_path):
    client = _local_client()
    p = Path(str(tmp_path), "b.bin", client=client, backend="local")
    p.write_bytes(b"\x00\x01\x02")
    assert p.read() == b"\x00\x01\x02"  # Path.read() must return the bytes


def test_mkdir_and_nested(tmp_path):
    client = _local_client()
    d = Path(str(tmp_path), "a", "b", "c", client=client, backend="local")
    d.mkdir(parents=True, exist_ok=True)
    assert d.exists()
    assert d.is_dir()


def test_truediv_keeps_backend(tmp_path):
    client = _local_client()
    base = Path(str(tmp_path), client=client, backend="local")
    child = base / "sub"
    assert child._backends == ("local",)
    assert str(child).endswith("sub")
