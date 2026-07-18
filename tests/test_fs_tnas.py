"""TnasWsPath (middleware filesystem.* backend) + TruenasPath (sftp->ws fallback).

All mocked -- no server. Asserts the right ``filesystem.*`` calls are made and
that TruenasPath falls back to the websocket leg when no SFTP is configured.
"""

import stat
from unittest.mock import MagicMock

import pytest

from pytruenas.fs.tnasws import TnasWsBackend, TnasWsPath, _stat_from_info
from pytruenas.fs.truenas import TruenasPath


def _client(**fs):
    client = MagicMock()
    for name, value in fs.items():
        getattr(client.api.filesystem, name).return_value = value
    return client


# -- TnasWsPath ---------------------------------------------------------------


def test_stat_maps_mode_and_exists():
    client = _client(stat={"mode": 0o40755, "size": 4096, "mtime": 10})
    p = TnasWsPath("truenas+ws://nas/etc", backend=TnasWsBackend(client))
    st = p.stat()
    assert stat.S_ISDIR(st.st_mode)
    assert p.exists() and p.is_dir()


def test_read_and_write_bytes():
    client = _client(stat={"mode": 0o100644}, get=b"hello")
    p = TnasWsPath("truenas+ws://nas/f.txt", backend=TnasWsBackend(client))
    assert p.read_bytes() == b"hello"
    p.write_bytes(b"data")
    fs = client.api.filesystem
    assert fs.put.call_args[0][0] == "/f.txt"
    assert fs.put.call_args[0][1] == {"append": False}


def test_read_write_text():
    client = _client(stat={"mode": 0o100644}, get=b"line")
    p = TnasWsPath("truenas+ws://nas/f.txt", backend=TnasWsBackend(client))
    assert p.read_text() == "line"
    p.write_text("hi")
    assert client.api.filesystem.put.called


def test_mkdir_and_chmod():
    client = _client()
    p = TnasWsPath("truenas+ws://nas/d", backend=TnasWsBackend(client))
    p.mkdir()
    assert client.api.filesystem.mkdir.call_args[0][0]["path"] == "/d"
    p.chmod(0o644)
    assert client.api.filesystem.setperm.called


def test_iterdir_uses_listdir():
    client = _client(
        listdir=[
            {"name": "a", "mode": 0o100644, "size": 1, "mtime": 1},
            {"name": "sub", "mode": 0o40755, "size": 0, "mtime": 1},
        ]
    )
    p = TnasWsPath("truenas+ws://nas/dir", backend=TnasWsBackend(client))
    names = sorted(child.name for child in p.iterdir())
    assert names == ["a", "sub"]


def test_unlink_shells_out():
    client = _client()
    p = TnasWsPath("truenas+ws://nas/f", backend=TnasWsBackend(client))
    p.unlink()
    assert client.run.call_args[0][0] == ("rm", "-f", "/f")


def test_stat_from_listdir_entry_without_mode():
    st = _stat_from_info({"name": "d", "type": "DIRECTORY"})
    assert stat.S_ISDIR(st.st_mode)


# -- TruenasPath fallback -----------------------------------------------------


def test_truenaspath_falls_back_to_ws_without_sftp():
    client = _client(stat={"mode": 0o100644}, get=b"x")
    client.shell.host = None  # no ssh target -> no sftp leg
    p = TruenasPath("truenas://nas/f.txt", backend=TnasWsBackend(client))
    assert p.read_text() == "x"          # ws leg
    p.unlink()                           # ws shell fallback
    assert client.run.call_args[0][0] == ("rm", "-f", "/f.txt")


def test_truenaspath_rename_without_sftp_raises():
    client = _client()
    client.shell.host = None
    p = TruenasPath("truenas://nas/f", backend=TnasWsBackend(client))
    with pytest.raises(NotImplementedError):
        p.rename("/g")


def test_truenaspath_resolve_falls_back_when_sftp_lacks_op():
    # pathlib_next's SftpPath has no resolve(); _try_sftp must surface that as
    # NotImplementedError so resolve() falls back to returning self, not crash
    # with AttributeError.
    client = _client()
    client.shell.host = "nas"
    client.shell.port = 22
    client.shell.username = "root"
    client.shell.password = None
    p = TruenasPath("truenas://nas/a/b", backend=TnasWsBackend(client))
    resolved = p.resolve()
    assert resolved.path == "/a/b"  # returned self, no AttributeError
