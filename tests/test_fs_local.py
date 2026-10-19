"""`client.path()` on the local socket target: plain local paths (no server)."""

from pathapi import LocalPath

from pytruenas import TrueNASClient
from pytruenas.fs import TrueNASWSPath


def _local_path(*segments):
    return TrueNASClient(autologin=False).path(*segments)


def test_a_local_client_serves_paths_from_the_local_provider():
    p = _local_path("/etc/hosts")
    assert p.provider.name == "local"
    assert isinstance(p._backend_path, LocalPath)


def test_a_remote_client_pins_the_websocket_leg_on_request():
    p = TrueNASClient("wss://nas.example.com", autologin=False).path(
        "/mnt/tank/x", backend="tnasws"
    )
    assert isinstance(p._backend_path, TrueNASWSPath)
    assert p._backend_path.path == "/mnt/tank/x"


def test_local_roundtrip(tmp_path):
    p = _local_path(str(tmp_path), "hello.txt")
    p.write_text("hi there")
    assert p.read_text() == "hi there"
    assert p.exists() and p.is_file()


def test_local_read_returns_bytes(tmp_path):
    p = _local_path(str(tmp_path), "b.bin")
    p.write_bytes(b"\x00\x01\x02")
    assert p.read_bytes() == b"\x00\x01\x02"


def test_local_mkdir_nested(tmp_path):
    d = _local_path(str(tmp_path), "a", "b", "c")
    d.mkdir(parents=True, exist_ok=True)
    assert d.exists() and d.is_dir()
