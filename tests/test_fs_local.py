"""client.path() type selection + local round-trip (no server needed)."""

from types import SimpleNamespace

from pathlib_next import LocalPath

from pytruenas.fs import TruenasPath, path


def _local_client():
    api = SimpleNamespace(is_local=True, host="localhost", port=0)
    return SimpleNamespace(_api=api, fsbackend="auto")


def _remote_client():
    api = SimpleNamespace(is_local=False, host="nas.example.com", port=0)
    return SimpleNamespace(_api=api, fsbackend="auto", api=SimpleNamespace())


def test_local_client_yields_localpath():
    p = path(_local_client(), "/etc/hosts")
    assert isinstance(p, LocalPath)


def test_remote_client_yields_truenaspath():
    p = path(_remote_client(), "/mnt/tank/x")
    assert isinstance(p, TruenasPath)
    assert p.path == "/mnt/tank/x"


def test_local_roundtrip(tmp_path):
    p = path(_local_client(), str(tmp_path), "hello.txt")
    assert isinstance(p, LocalPath)
    p.write_text("hi there")
    assert p.read_text() == "hi there"
    assert p.exists() and p.is_file()


def test_local_read_returns_bytes(tmp_path):
    p = path(_local_client(), str(tmp_path), "b.bin")
    p.write_bytes(b"\x00\x01\x02")
    assert p.read_bytes() == b"\x00\x01\x02"


def test_local_mkdir_nested(tmp_path):
    d = path(_local_client(), str(tmp_path), "a", "b", "c")
    d.mkdir(parents=True, exist_ok=True)
    assert d.exists() and d.is_dir()
