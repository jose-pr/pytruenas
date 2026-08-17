"""TnasWsPath (middleware filesystem.* backend) + TruenasPath (sftp->ws fallback).

All mocked -- no server. Asserts the right ``filesystem.*`` calls are made and
that TruenasPath falls back to the websocket leg when no SFTP is configured.
"""

import stat
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from pytruenas.fs import path as fs_path
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


# -- listing must not ask the server for ZFS-only columns ---------------------


#: Every column of `FilesystemDirQueryResultItem` (TrueNAS 26.0.0-BETA.1). Only
#: `zfs_attrs` is ZFS-only; it is the one that makes the whole call fail on a
#: filesystem that has no ZFS attributes, even though the schema says it is
#: nullable exactly for that case.
_LISTDIR_COLUMNS = (
    "name",
    "path",
    "realpath",
    "type",
    "size",
    "allocation_size",
    "mode",
    "mount_id",
    "acl",
    "uid",
    "gid",
    "is_mountpoint",
    "is_ctldir",
    "attributes",
    "xattrs",
    "zfs_attrs",
)

_TMP_ENTRIES = [
    {
        "name": "note.txt",
        "path": "/tmp/note.txt",
        "realpath": "/tmp/note.txt",
        "type": "FILE",
        "size": 5,
        "allocation_size": 4096,
        "mode": 0o100644,
        "mount_id": 27,
        "acl": False,
        "uid": 0,
        "gid": 0,
        "is_mountpoint": False,
        "is_ctldir": False,
        "attributes": [],
        "xattrs": [],
    },
    {
        "name": "sub",
        "path": "/tmp/sub",
        "realpath": "/tmp/sub",
        "type": "DIRECTORY",
        "size": 40,
        "allocation_size": 0,
        "mode": 0o40755,
        "mount_id": 27,
        "acl": False,
        "uid": 0,
        "gid": 0,
        "is_mountpoint": False,
        "is_ctldir": False,
        "attributes": [],
        "xattrs": [],
    },
]


def _non_zfs_middleware(method, *args, **kwds):
    """A `filesystem.*` server whose filesystem is not ZFS (a tmpfs `/tmp`).

    Models exactly what 26.0.0-BETA.1 does, measured on the appliance: an
    unrestricted `listdir` computes `zfs_attrs` for every entry and fails the
    call outright; a `select` that does not name that column succeeds, because
    an unrequested column is never computed. `stat` is unaffected either way,
    which is what made the bug read like a permissions problem.
    """
    from pytruenas.connection import ClientException

    path = args[0]
    if method == "filesystem.stat":
        entry = next((e for e in _TMP_ENTRIES if e["path"] == path), None)
        if entry is None:
            raise ClientException(f"[ENOENT] {path}: No such file or directory", 2)
        return {**entry, "mtime": 1700000000.0}
    if method != "filesystem.listdir":  # pragma: no cover - guard
        raise AssertionError(method)

    options = args[2] if len(args) > 2 else {}
    select = list(options.get("select") or ())
    if not select or "zfs_attrs" in select:
        raise ClientException(f"[EFAULT] {path}: ZFS attributes are not supported.", 14)
    unknown = set(select) - set(_LISTDIR_COLUMNS)
    assert not unknown, f"selected columns the API does not define: {sorted(unknown)}"
    return [{k: v for k, v in e.items() if k in select} for e in _TMP_ENTRIES]


def _non_zfs_client():
    """A client whose `api` is the real `Namespace`, so the wire call is real.

    `_client()` stubs `client.api.filesystem.listdir` itself, which cannot see
    the query options at all -- the defect here is precisely *what gets sent*,
    so the dispatcher has to be genuine and only the connection faked.
    """
    from pytruenas.namespace import Namespace

    client = MagicMock()
    client.conn.call.side_effect = _non_zfs_middleware
    client.api = Namespace(client)
    return client


def _listdir_calls(client):
    return [
        c for c in client.conn.call.call_args_list if c[0][0] == "filesystem.listdir"
    ]


def test_iterdir_works_on_a_filesystem_without_zfs_attributes():
    """Regression: `iterdir()` raised EFAULT on every non-ZFS path.

    `_listdir`/`_scandir` sent no query options, so the middleware computed the
    ZFS-only `zfs_attrs` column for each entry and failed the whole listing on
    `/tmp`, `/var/tmp`, `/dev`, `/proc`, `/sys` and any non-pool mount -- while
    `stat()` and `read_bytes()` on those same paths worked. Fails on the
    pre-fix code with `OSError: [Errno 14] ... ZFS attributes are not
    supported.`, exactly as it failed live.
    """
    client = _non_zfs_client()
    p = TnasWsPath("truenas+ws://nas/tmp", backend=TnasWsBackend(client))

    children = sorted(p.iterdir(), key=lambda c: c.name)
    assert [c.name for c in children] == ["note.txt", "sub"]
    assert children[1].is_dir() and not children[0].is_dir()


def test_scandir_seeds_the_stat_it_promises_without_zfs_columns():
    """The projection has to carry everything `_stat_from_info` reads.

    `_scandir`'s whole point is one round trip: a `select` narrow enough to
    dodge `zfs_attrs` but too narrow to type the entries would trade this bug
    for a silent one, so pin the seeded stat rather than the column list.
    """
    client = _non_zfs_client()
    p = TnasWsPath("truenas+ws://nas/tmp", backend=TnasWsBackend(client))

    seeded = dict(p._scandir())
    assert stat.S_ISDIR(seeded["sub"].st_mode)
    assert stat.S_ISREG(seeded["note.txt"].st_mode)
    assert seeded["note.txt"].st_size == 5

    # And the hint really is what a child answers from -- `lstat()` consumes it
    # instead of going back to the server.
    child = next(c for c in p.iterdir() if c.name == "sub")
    before = len(client.conn.call.call_args_list)
    assert child.lstat().st_mode == 0o40755
    assert len(client.conn.call.call_args_list) == before


def test_listdir_asks_only_for_the_name():
    """`_listdir` yields names, so it has no reason to pull anything else."""
    client = _non_zfs_client()
    p = TnasWsPath("truenas+ws://nas/tmp", backend=TnasWsBackend(client))

    assert sorted(p._listdir()) == ["note.txt", "sub"]
    (call,) = _listdir_calls(client)
    assert call[0][0] == "filesystem.listdir"
    assert call[0][1] == "/tmp"
    assert call[0][3] == {"select": ["name"]}


@pytest.mark.parametrize(
    "listing", [lambda p: list(p.iterdir()), lambda p: list(p._listdir())]
)
def test_every_listing_call_projects_away_the_zfs_column(listing):
    """One code path for both filesystem kinds: no retry, no error sniffing.

    Whatever a listing caller selects, it must be a non-empty projection that
    omits `zfs_attrs` -- that is the whole fix, and it is the same request on a
    ZFS pool as on a tmpfs, so there is never a second round trip.
    """
    client = _non_zfs_client()
    p = TnasWsPath("truenas+ws://nas/tmp", backend=TnasWsBackend(client))
    listing(p)

    calls = _listdir_calls(client)
    assert calls, "no filesystem.listdir call was made"
    assert len(calls) == 1, "the listing was retried -- it should never need to be"
    for call in calls:
        select = call[0][3]["select"]
        assert select and "zfs_attrs" not in select
        assert "name" in select


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


# -- the sftp:// URI must be built as a URI -----------------------------------


# RFC 3986 `pchar` plus `/`, spelled out here rather than imported from the
# module under test: the input side of these cases is a fixture, and the
# assertion is a *round-trip*, so borrowing the implementation's own constant
# for both halves would make the pin tautological.
_PCHAR = "/:@-._~!$&'()*+,;="


def _truenas_path(client, remote):
    """A `TruenasPath` whose `.path` really is `remote`.

    `TruenasPath` is itself a `UriPath`, so handing it a raw `truenas://` URI
    truncates the same way the SFTP leg used to -- the fixture has to encode
    too, or the precondition below fails before the leg is ever reached.
    """
    from urllib.parse import quote

    return TruenasPath(
        "truenas://nas" + quote(remote, safe=_PCHAR), backend=TnasWsBackend(client)
    )


@pytest.mark.parametrize(
    "remote",
    [
        "/mnt/tank/cache?v=2",  # truncated at the `?` -- read as a query
        "/mnt/tank/a#b",  # truncated at the `#` -- read as a fragment
        "/mnt/tank/sp ace",
        "/mnt/tank/100%",  # a lone `%` -- must not be re-encoded twice
        "/mnt/tank/report%20final.txt",  # a literal `%20`, NOT a space
        "/mnt/tank/café.txt",
    ],
)
def test_sftp_leg_survives_uri_syntax_in_a_filename(remote):
    """Regression: `_sftp()` interpolated the path into a URI unencoded.

    `SftpPath` parses that string and uridecodes the parts, so a `?` or `#` in
    a filename truncated the path into a query or fragment -- the operation
    then ran against a *shorter, different* file with no error -- and a genuine
    `%xx` decoded into another name again. hostctl fixed the identical defect
    on its own SFTP leg in 0.2.6; this hand-built URI never got it.

    What is pinned is the round-trip, not the encoded spelling.
    """
    client = _client(ssh=_ssh_config(host="nas", port=2222))
    p = _truenas_path(client, remote)
    assert p.path == remote  # precondition: the path really carries the name

    sftp = p._sftp()
    assert sftp is not None
    assert sftp.path == remote


def test_sftp_leg_encoding_leaves_uri_legal_characters_readable():
    """Encoding is minimal: `:` is legal in a path segment, so it stays.

    A naive `quote(path, safe="/")` would render a Windows-flavoured remote
    path as `/C%3A/Temp`, which is a different (and wrong) name.
    """
    client = _client(ssh=_ssh_config(host="nas", port=2222))
    p = _truenas_path(client, "/C:/Temp")
    sftp = p._sftp()
    assert str(sftp) == "sftp://nas:2222/C:/Temp"
    assert sftp.path == "/C:/Temp"


# -- the truenas:// URI is built the same way, one layer up --------------------


def _path_client(ssh=None):
    """A remote fake host shaped for `pytruenas.fs.path()`.

    `path()` reads `is_local`/`host` off the settings object (`_api` here, the
    pre-hostctl spelling it still accepts), while `TruenasPath._sftp()` reads
    the SSH target off `client.config.ssh` -- two different attributes, so both
    have to be real for a path built through `path()` to reach its SFTP leg.
    """
    return SimpleNamespace(
        _api=SimpleNamespace(is_local=False, host="nas", port=0),
        config=SimpleNamespace(ssh=ssh),
        api=SimpleNamespace(),
        fsbackend="auto",
    )


_URI_SYNTAX_NAMES = [
    "/mnt/tank/cache?v=2",  # truncated at the `?` -- read as a query
    "/mnt/tank/a#b",  # truncated at the `#` -- read as a fragment
    "/mnt/tank/sp ace",
    "/mnt/tank/100%",  # a lone `%` -- must not be re-encoded twice
    "/mnt/tank/report%20final.txt",  # a literal `%20`, NOT a space
    "/mnt/tank/café.txt",
]


@pytest.mark.parametrize("remote", _URI_SYNTAX_NAMES)
@pytest.mark.parametrize(
    "backend,expected",
    [("ws", TnasWsPath), ("api", TnasWsPath), ("auto", TruenasPath)],
)
def test_path_construction_survives_uri_syntax_in_a_filename(remote, backend, expected):
    """Regression: `_ws_uri`/`_truenas_uri` interpolated the path unencoded.

    Worse than the SFTP defect fixed in 0.4.4, because it corrupts `self.path`
    at *construction* -- before any leg is chosen -- so the websocket leg
    (`read_bytes`, `stat`, every `filesystem.*` call) addressed the truncated
    name too, not just the five SFTP-first operations.

    What is pinned is the round-trip, not the encoded spelling.
    """
    p = fs_path(_path_client(), remote, backend=backend)
    assert isinstance(p, expected)
    assert p.path == remote


def test_path_construction_leaves_uri_legal_characters_readable():
    """Encoding is minimal, as on the SFTP leg: `:` is legal in a segment."""
    p = fs_path(_path_client(), "/C:/Temp", backend="ws")
    assert str(p) == "truenas+ws://nas/C:/Temp"
    assert p.path == "/C:/Temp"


def test_path_construction_joins_segments_before_encoding():
    """A `/` between segments is a separator, not part of a name."""
    p = fs_path(_path_client(), "/mnt/tank", "a?b", "c#d", backend="ws")
    assert p.path == "/mnt/tank/a?b/c#d"
    assert p.name == "c#d"


@pytest.mark.parametrize("remote", _URI_SYNTAX_NAMES)
def test_sftp_leg_is_not_encoded_twice(remote):
    """The two encoding sites compose to exactly one round of encoding.

    Construction encodes into the `truenas://` URI and `_sftp()` encodes again
    into the `sftp://` one. That is correct only because `UriPath.path`
    *decodes*: the SFTP leg quotes the decoded name, never the already-quoted
    spelling. If either side were to encode an encoded value, `100%` would
    reach the host as `100%25` and `report%20final.txt` as
    `report%2520final.txt` -- a different file, silently.
    """
    client = _path_client(ssh=_ssh_config(host="nas", port=2222))
    p = fs_path(client, remote, backend="auto")
    assert p.path == remote

    sftp = p._sftp()
    assert sftp is not None
    assert sftp.path == remote  # one decode of one encode, not two of two


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


def test_connect_opts_delegate_to_sshconfig_connect_opts():
    """The mapping is hostctl's, not a hand-rolled copy of its field list.

    A local copy is how `known_hosts` went missing (see the test below), so
    pin the delegation itself: whatever `SshConfig.connect_opts()` produces is
    what the SFTP leg connects with.
    """
    from pytruenas.fs.truenas import _connect_opts_from_ssh

    ssh = _ssh_config(username="admin", password="pw")
    assert _connect_opts_from_ssh(ssh) == ssh.connect_opts()
    assert _connect_opts_from_ssh(ssh) == {"username": "admin", "password": "pw"}

    keyed = _ssh_config(client_keys=["PRIVATE"])
    assert _connect_opts_from_ssh(keyed) == keyed.connect_opts()


def test_connect_opts_carry_known_hosts():
    """Regression: the SFTP leg dropped the caller's host-key policy.

    `_connect_opts_from_ssh` hand-mapped username/client_keys/password only, so
    `known_hosts` never reached `asyncssh.connect()`. The SSH executor (which
    uses `SshConfig.connect_opts()`) enforced the configured policy while this
    leg ignored it -- proven live: a `known_hosts` file with no entry for the
    host made hostctl's ssh executor refuse to connect, and the SFTP leg
    connected anyway.
    """
    from pytruenas.fs.truenas import _connect_opts_from_ssh

    opts = _connect_opts_from_ssh(_ssh_config(known_hosts="/etc/ssh/known_hosts"))
    assert opts["known_hosts"] == "/etc/ssh/known_hosts"

    # `None` means "do not verify" and is a real, deliberate choice -- distinct
    # from the `()` default, which SshConfig treats as "unset" and omits.
    disabled = _connect_opts_from_ssh(_ssh_config(known_hosts=None))
    assert "known_hosts" in disabled and disabled["known_hosts"] is None

    assert "known_hosts" not in _connect_opts_from_ssh(_ssh_config())


def test_sftp_backend_is_built_with_the_configured_known_hosts():
    """The same regression, end to end through the leg the client really builds."""
    client = _client(ssh=_ssh_config(known_hosts="/etc/ssh/known_hosts"))
    p = TruenasPath("truenas://nas/etc/hosts", backend=TnasWsBackend(client))

    sftp = p._sftp()
    assert sftp is not None
    assert sftp.backend.connect_opts["known_hosts"] == "/etc/ssh/known_hosts"
