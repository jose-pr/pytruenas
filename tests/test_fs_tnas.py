"""TnasWsPath (middleware filesystem.* backend) + TruenasPath (sftp->ws fallback).

All mocked -- no server. Asserts the right ``filesystem.*`` calls are made and
that TruenasPath falls back to the websocket leg when no SFTP is configured.
"""

import stat
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from pytruenas.fs.tnasws import TnasWsBackend, TnasWsPath, _stat_from_info
from pytruenas.fs.truenas import TruenasPath


def _client(ssh=None, **fs):
    """A fake host: websocket-only by default, or carrying an SSH leg.

    The shape matters -- `TruenasPath._sftp()` reads the SSH target off
    `client.config.ssh` (a real `hostctl.host.SshConfig`), exactly as a live
    `TrueNASHost` carries it. A bare `MagicMock` would auto-vivify *any*
    attribute name and make the leg look configured no matter what it read,
    which is how the dead `client.ssh_config` lookup stayed green for a
    release.
    """
    client = MagicMock()
    client.config = SimpleNamespace(ssh=ssh)
    for name, value in fs.items():
        getattr(client.api.filesystem, name).return_value = value
    return client


def _ssh_config(**overrides):
    from hostctl.host import SshConfig

    opts = dict(host="nas", port=22, username="root", password=None)
    opts.update(overrides)
    return SshConfig(**opts)


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


# The SSH target is `client.config.ssh`, an `hostctl.host.SshConfig`. It was
# `client.ssh_config` before `TrueNASClient` merged into `TrueNASHost`, and
# that name no longer exists anywhere -- see
# `test_truenaspath_ignores_the_pre_merge_ssh_config_attribute`.


def test_truenaspath_falls_back_to_ws_without_sftp():
    client = _client(stat={"mode": 0o100644}, get=b"x")  # no ssh -> no sftp leg
    p = TruenasPath("truenas://nas/f.txt", backend=TnasWsBackend(client))
    assert p.read_text() == "x"  # ws leg
    p.unlink()  # ws shell fallback
    assert client.run.call_args[0][0] == ("rm", "-f", "/f.txt")


def test_truenaspath_rename_without_sftp_raises():
    client = _client()
    p = TruenasPath("truenas://nas/f", backend=TnasWsBackend(client))
    with pytest.raises(NotImplementedError):
        p.rename("/g")


def test_truenaspath_resolve_falls_back_when_sftp_lacks_op():
    # pathlib_next's SftpPath has no resolve(); _try_sftp must surface that as
    # NotImplementedError so resolve() falls back to returning self, not crash
    # with AttributeError.
    client = _client(ssh=_ssh_config())
    p = TruenasPath("truenas://nas/a/b", backend=TnasWsBackend(client))
    assert p._sftp() is not None  # the leg really is built here
    resolved = p.resolve()
    assert resolved.path == "/a/b"  # returned self, no AttributeError


def test_truenaspath_builds_the_sftp_leg_from_config_ssh():
    client = _client(ssh=_ssh_config(host="nas", port=2222, username="admin"))
    p = TruenasPath("truenas://nas/a/b", backend=TnasWsBackend(client))
    sftp = p._sftp()
    assert sftp is not None
    assert str(sftp) == "sftp://nas:2222/a/b"


def test_truenaspath_ignores_the_pre_merge_ssh_config_attribute():
    """`client.ssh_config` is gone; reading it built the leg off a Mock.

    Fails on the pre-fix lookup, which read `ssh_config` first and would have
    happily built an SFTP path out of this stray attribute.
    """
    client = _client()  # config.ssh is None -> websocket-only
    client.ssh_config = SimpleNamespace(
        host="nas", port=22, username="root", password=None
    )
    p = TruenasPath("truenas://nas/f", backend=TnasWsBackend(client))
    assert p._sftp() is None


# -- symlink_to(force=) must not remove before it can create ------------------


class _FakeSftp:
    """Just enough SFTP leg to record a `symlink_to`."""

    def __init__(self):
        self.calls = []

    def symlink_to(self, target, target_is_directory=False):
        self.calls.append((target, target_is_directory))


def test_symlink_to_force_does_not_remove_when_nothing_can_create(monkeypatch):
    """Regression: the removal used to run, and *then* the call failed.

    A websocket-only host has no way to make a symlink, so `force=True` was
    pure loss -- the existing target was deleted and `NotImplementedError`
    raised straight after.
    """
    client = _client(stat={"mode": 0o100644})  # target exists, is a file
    p = TruenasPath("truenas://nas/link", backend=TnasWsBackend(client))
    assert p._sftp() is None  # websocket-only

    with pytest.raises(NotImplementedError):
        p.symlink_to("/target", force=True)

    assert not client.run.called  # nothing was removed
    assert not client.api.filesystem.unlink.called


def test_symlink_to_force_still_removes_when_a_leg_can_create(monkeypatch):
    """The gate must not disable `force=` on a host that *does* have SFTP."""
    client = _client(stat={"mode": 0o100644}, ssh=_ssh_config())
    fake = _FakeSftp()
    monkeypatch.setattr(TruenasPath, "_sftp", lambda self: fake)

    p = TruenasPath("truenas://nas/link", backend=TnasWsBackend(client))
    p.symlink_to("/target", force=True)

    assert client.run.called  # the conflicting file was removed
    assert fake.calls == [("/target", False)]


def test_symlink_to_force_honours_onremove_veto(monkeypatch):
    client = _client(stat={"mode": 0o100644}, ssh=_ssh_config())
    fake = _FakeSftp()
    monkeypatch.setattr(TruenasPath, "_sftp", lambda self: fake)

    p = TruenasPath("truenas://nas/link", backend=TnasWsBackend(client))
    p.symlink_to("/target", force=True, onremove=lambda _p, _kind: False)

    assert not client.run.called  # veto -> no removal
    assert fake.calls == [("/target", False)]


def test_symlink_to_force_rejects_a_kind_it_was_not_allowed(monkeypatch):
    client = _client(stat={"mode": 0o100644}, ssh=_ssh_config())
    fake = _FakeSftp()
    monkeypatch.setattr(TruenasPath, "_sftp", lambda self: fake)

    p = TruenasPath("truenas://nas/link", backend=TnasWsBackend(client))
    with pytest.raises(FileExistsError):
        p.symlink_to("/target", force="link")  # existing target is a file

    assert not client.run.called
    assert fake.calls == []


def test_truenaspath_sftp_leg_reachable_on_a_real_host():
    """Construction only -- no network. Pins the real class's attribute shape."""
    from hostctl.host import SshConfig

    from pytruenas import TrueNASClient

    host = TrueNASClient(
        "wss://nas",
        autologin=False,
        ssh=SshConfig(host="nas", port=22, username="root", password="pw"),
    )
    p = TruenasPath("truenas://nas/etc/hosts", backend=TnasWsBackend(host))
    assert p._sftp() is not None


def test_connect_opts_prefer_real_sshconfig_fields():
    from pytruenas.fs.truenas import _connect_opts_from_ssh

    opts = _connect_opts_from_ssh(_ssh_config(username="admin", password="pw"))
    assert opts == {"username": "admin", "password": "pw"}

    keyed = _connect_opts_from_ssh(_ssh_config(client_keys=["PRIVATE"]))
    assert keyed == {"username": "root", "client_keys": [b"PRIVATE"]}
