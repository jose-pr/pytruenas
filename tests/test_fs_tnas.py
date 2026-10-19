"""TnasWsPath (the middleware filesystem.* backend), fs.path() and fs.symlink_to().

All mocked -- no server. Asserts the right ``filesystem.*`` calls are made, and
that a host path names the decoded file on every leg.
"""

import stat
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from pytruenas import TrueNASClient
from pytruenas.fs import path as fs_path
from pytruenas.fs import symlink_to as fs_symlink_to
from pytruenas.fs.tnasws import TnasWsBackend, TnasWsPath, _stat_from_info


def _client(ssh=None, **fs):
    """A fake host for a `TnasWsPath`: websocket-only by default.

    `config.ssh` is a real attribute (or a real `hostctl.SSHConfig`): a bare
    `MagicMock` would auto-vivify any attribute name.
    """
    client = MagicMock()
    client.config = SimpleNamespace(ssh=ssh)
    for name, value in fs.items():
        getattr(client.api.filesystem, name).return_value = value
    return client


def _ssh_config(**overrides):
    from hostctl import SSHConfig

    opts = dict(host="nas", port=22, username="root", password=None)
    opts.update(overrides)
    return SSHConfig(**opts)


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
    # The middleware takes the mode as octal digits; "420" would be decimal.
    sent = client.api.filesystem.setperm.call_args[0][0]
    assert (sent["path"], sent["mode"]) == ("/d", "644")


class _JobMiddleware:
    """A faked `conn` where `filesystem.setperm`/`chown` start job 77."""

    def __init__(self, state="SUCCESS", error="[EPERM] setperm failed", errno=None):
        self.wire = []
        self.job = {
            "id": 77,
            "state": state,
            "result": None,
            "error": error,
            "exc_info": {"errno": errno},
            "progress": {},
        }
        self._closed = type("Open", (), {"is_set": lambda self: False})()

    def call(self, method, *params, **kwds):
        self.wire.append(method)
        if method == "core.get_jobs":
            return [self.job]
        return 77


def _job_path(middleware):
    from pytruenas import TrueNASClient

    host = TrueNASClient("wss://nas.example", autologin=False)
    host._conn = middleware
    return fs_path(host, "/mnt/tank/f", backend="ws")


@pytest.mark.parametrize(
    "change",
    [lambda p: p.chmod(0o600), lambda p: p.chown(0, 0)],
    ids=["chmod", "chown"],
)
def test_a_permission_change_returns_once_its_job_is_done(change):
    middleware = _JobMiddleware()
    change(_job_path(middleware))
    assert middleware.wire[-1] == "core.get_jobs"


@pytest.mark.parametrize(
    "change",
    [lambda p: p.chmod(0o600), lambda p: p.chown(0, 0)],
    ids=["chmod", "chown"],
)
def test_a_failed_permission_job_raises_the_matching_oserror(change):
    with pytest.raises(PermissionError):
        change(_job_path(_JobMiddleware(state="FAILED")))


def test_a_failed_job_without_an_errno_name_is_still_an_oserror():
    import errno

    middleware = _JobMiddleware(state="FAILED", error="ACL is in the way", errno=None)
    with pytest.raises(OSError) as error:
        _job_path(middleware).chmod(0o600)
    assert error.value.errno == errno.EIO
    assert error.value.filename == "/mnt/tank/f"


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


def _removal_client(returncode=0, stderr=b"", stat=None):
    """A websocket-only host whose `rm`/`rmdir` exits `returncode`.

    `stat` is what `filesystem.stat` answers afterwards; an exception instance
    is raised instead (`FileNotFoundError` for a path that is gone).
    """
    import subprocess

    client = _client()
    client.run.side_effect = lambda cmd, **kw: subprocess.CompletedProcess(
        cmd, returncode, b"", stderr
    )
    if isinstance(stat, BaseException):
        client.api.filesystem.stat.side_effect = stat
    else:
        client.api.filesystem.stat.return_value = stat
    return client


def _ws(client, path="/f"):
    return TnasWsPath(f"truenas+ws://nas{path}", backend=TnasWsBackend(client))


def test_unlink_removes_without_forcing():
    """`rm -f` exits 0 for a missing file, so it cannot report one."""
    client = _removal_client()
    _ws(client).unlink()
    assert client.run.call_args[0][0] == ("rm", "--", "/f")
    assert client.run.call_args[1]["check"] is False
    assert not client.api.filesystem.stat.called


def test_unlink_of_a_missing_file_raises_file_not_found():
    gone = FileNotFoundError(2, "No such file or directory")
    client = _removal_client(1, b"rm: cannot remove '/f': No such file", gone)
    with pytest.raises(FileNotFoundError):
        _ws(client).unlink()
    _ws(client).unlink(missing_ok=True)


def test_unlink_of_a_directory_raises_is_a_directory():
    client = _removal_client(1, b"rm: cannot remove '/d': Is a directory", {})
    client.api.filesystem.stat.return_value = {"type": "DIRECTORY"}
    with pytest.raises(IsADirectoryError):
        _ws(client, "/d").unlink()


def test_unlink_refused_raises_permission_error():
    client = _removal_client(
        1, b"rm: cannot remove '/f': Permission denied", {"type": "FILE"}
    )
    with pytest.raises(PermissionError) as error:
        _ws(client).unlink()
    assert error.value.filename == "/f"


def test_rmdir_of_a_non_empty_directory_raises_enotempty():
    import errno

    client = _removal_client(1, b"", {"type": "DIRECTORY"})
    client.api.filesystem.listdir.return_value = [{"name": "child"}]
    with pytest.raises(OSError) as error:
        _ws(client, "/d").rmdir()
    assert error.value.errno == errno.ENOTEMPTY
    assert client.run.call_args[0][0] == ("rmdir", "--", "/d")


def test_rmdir_of_a_file_raises_not_a_directory():
    client = _removal_client(1, b"rmdir: failed: Not a directory", {"type": "FILE"})
    with pytest.raises(NotADirectoryError):
        _ws(client).rmdir()


def test_rmdir_of_a_missing_directory_raises_file_not_found():
    gone = FileNotFoundError(2, "No such file or directory")
    with pytest.raises(FileNotFoundError):
        _ws(_removal_client(1, b"", gone), "/d").rmdir()


def test_stat_from_listdir_entry_without_mode():
    st = _stat_from_info({"name": "d", "type": "DIRECTORY"})
    assert stat.S_ISDIR(st.st_mode)


def test_stat_follows_a_symlink_to_its_target():
    link = {"type": "SYMLINK", "mode": 0o120777, "realpath": "/mnt/tank/dir"}
    target = {"type": "DIRECTORY", "mode": 0o40755, "uid": 1000, "gid": 100}
    client = _client()
    client.api.filesystem.stat.side_effect = lambda path, **kw: (
        link if path == "/mnt/tank/link" else target
    )
    p = _ws(client, "/mnt/tank/link")
    assert p.is_dir()
    assert p.stat().st_uid == 1000
    assert stat.S_ISLNK(p.stat(follow_symlinks=False).st_mode)
    assert p.is_symlink()


def test_stat_of_a_dangling_symlink_is_not_found_but_lstat_works():
    link = {"type": "SYMLINK", "mode": 0o120777, "realpath": "/mnt/tank/gone"}

    def stat_(path, **kw):
        if path == "/mnt/tank/gone":
            raise FileNotFoundError(2, "No such file or directory")
        return link

    client = _client()
    client.api.filesystem.stat.side_effect = stat_
    p = _ws(client, "/mnt/tank/link")
    with pytest.raises(FileNotFoundError):
        p.stat()
    assert not p.exists()
    assert p.is_symlink()


def test_stat_reports_owner_and_times():
    st = _stat_from_info(
        {
            "mode": 0o100640,
            "size": 3,
            "uid": 1000,
            "gid": 100,
            "atime": 11.5,
            "mtime": 12.5,
            "ctime": 13.5,
        }
    )
    assert (st.st_uid, st.st_gid) == (1000, 100)
    assert (st.st_atime, st.st_mtime, st.st_ctime) == (11.5, 12.5, 13.5)


def test_a_symlink_entry_without_mode_is_a_link():
    assert stat.S_ISLNK(_stat_from_info({"type": "SYMLINK"}).st_mode)


# -- fs.path() for a remote host is the host's own composite path -------------


def _ws_only_host(**fs):
    host = TrueNASClient("wss://nas", autologin=False)
    host.__dict__["api"] = MagicMock()
    for name, value in fs.items():
        getattr(host.api.filesystem, name).return_value = value
    return host


def test_fs_path_of_a_remote_host_is_the_host_path_rooted_at_slash():
    host = TrueNASClient("wss://nas", autologin=False)
    p = fs_path(host, "mnt", "tank", "f.txt")
    assert type(p) is type(host.path("/x"))
    assert str(p) == "/mnt/tank/f.txt"
    assert p.provider.name == "tnasws"
    assert str(fs_path(host, "x", backend="truenas")) == "/x"


def test_fs_path_refuses_an_unknown_backend():
    with pytest.raises(ValueError, match="unknown path backend"):
        fs_path(TrueNASClient("wss://nas", autologin=False), "/x", backend="sftp")


def test_the_tnasws_provider_builds_a_plain_websocket_path():
    host = TrueNASClient("wss://nas", autologin=False)
    p = host.path("/mnt/tank/f.txt", backend="tnasws")
    assert type(p._backend_path) is TnasWsPath
    assert p._backend_path.path == "/mnt/tank/f.txt"


def test_a_websocket_only_host_cannot_rename():
    host = TrueNASClient("wss://nas", autologin=False)
    with pytest.raises(NotImplementedError):
        host.path("/f").rename("/g")


# -- mkdir: the mode actually applied, and parents ------------------------------


def _mkdir_client(existing=("/", "/mnt", "/mnt/tank")):
    """A real Namespace over a `filesystem.mkdir` that behaves like 26.0's.

    Measured live: the middleware applies the mode it is sent (no umask), and
    a missing parent fails with `[Errno 2] No such file or directory: '...'`.
    """
    from pytruenas.connection import ClientException
    from pytruenas.namespace import Namespace

    dirs = set(existing)
    sent = []

    def call(method, *args, **kwds):
        assert method == "filesystem.mkdir", method
        spec = args[0]
        path = spec["path"]
        sent.append((path, spec["options"]["mode"]))
        parent = path.rsplit("/", 1)[0] or "/"
        if parent not in dirs:
            raise ClientException(f"[Errno 2] No such file or directory: '{path}'", 2)
        if path in dirs:
            raise ClientException(f"[Errno 17] File exists: '{path}'", 17)
        dirs.add(path)
        return {"path": path}

    client = MagicMock()
    client.config = SimpleNamespace(ssh=None)
    client.conn.call.side_effect = call
    client.api = Namespace(client)
    return client, sent, dirs


def test_mkdir_default_mode_is_not_world_writable():
    """pathlib's default 0o777 relies on a umask; the middleware applies none.

    Measured live: a default `mkdir()` produced a 0o777 directory.
    """
    client, sent, _ = _mkdir_client()
    TnasWsPath("truenas+ws://nas/mnt/tank/d", backend=TnasWsBackend(client)).mkdir()
    assert sent == [("/mnt/tank/d", "0o755")]


def test_mkdir_explicit_mode_is_sent_as_given():
    client, sent, _ = _mkdir_client()
    p = TnasWsPath("truenas+ws://nas/mnt/tank/d", backend=TnasWsBackend(client))
    p.mkdir(mode=0o750)
    assert sent == [("/mnt/tank/d", "0o750")]


def test_mkdir_parents_creates_the_missing_parents():
    """`[Errno 2] ...` from the middleware must read as FileNotFoundError.

    As a ClientException, `mkdir(parents=True)` never creates the parents and
    the call fails with ENOENT (measured live).
    """
    client, sent, dirs = _mkdir_client()
    p = TnasWsPath("truenas+ws://nas/mnt/tank/a/b", backend=TnasWsBackend(client))
    p.mkdir(parents=True)
    assert {"/mnt/tank/a", "/mnt/tank/a/b"} <= dirs
    assert all(mode == "0o755" for _, mode in sent)


def test_bracketed_errno_numbers_map_to_the_matching_oserror():
    from pytruenas.connection import ClientException
    from pytruenas.namespace import ioerror

    err = ioerror(ClientException("[Errno 2] No such file or directory: '/x'", 2))
    assert isinstance(err, FileNotFoundError)
    assert isinstance(ioerror(ClientException("[EEXIST] exists", 17)), FileExistsError)
    unknown = ClientException("[EWHATEVER] odd", None)
    assert ioerror(unknown) is unknown


# -- one host vs two hosts: rename, move and the same-file guard ---------------


def _host_client(name, **fs):
    """A fake host with a real-looking identity (`_config.host`, a URI)."""
    client = _client(**fs)
    client._config = SimpleNamespace(host=name, is_local=False)
    client.connection_uri = f"truenas+wss://{name}"
    return client


def test_paths_built_separately_on_one_host_are_one_filesystem():
    """`fs.path()` gives each path its own backend; the host is what counts.

    With the URI layer's default (compare supplied backend objects) the
    same-file guard never fires, so `move(overwrite=True)` onto a second
    `fs.path()` of the same file deletes it.
    """
    client = _host_client("nasA", stat={"mode": 0o100644}, get=b"data")
    a = fs_path(client, "/mnt/tank/a.txt", backend="ws")
    b = fs_path(client, "/mnt/tank/a.txt", backend="ws")
    assert a._backend is not b._backend
    assert a._same_filesystem(b)
    with pytest.raises(OSError, match="same file"):
        a.copy(b, overwrite=True)
    assert not client.api.filesystem.put.called


def test_paths_on_two_hosts_are_two_filesystems():
    a = fs_path(_host_client("nasA"), "/mnt/tank/a.txt", backend="ws")
    b = fs_path(_host_client("nasB"), "/mnt/tank/a.txt", backend="ws")
    assert not a._same_filesystem(b)


def test_host_paths_built_separately_are_one_filesystem():
    """The host's composite paths share its providers, so the guard fires."""
    host = TrueNASClient("wss://nas", autologin=False)
    assert fs_path(host, "/a")._same_filesystem(host.path("/a"))
    other = TrueNASClient("wss://nas", autologin=False)
    assert not host.path("/a")._same_filesystem(other.path("/a"))


# -- a filename with URI syntax reaches the SFTP leg unchanged ----------------


_SPECIAL_NAMES = [
    "/mnt/tank/cache?v=2",  # truncated at the `?` -- read as a query
    "/mnt/tank/a#b",  # truncated at the `#` -- read as a fragment
    "/mnt/tank/sp ace",
    "/mnt/tank/100%",  # a lone `%` -- must not be re-encoded twice
    "/mnt/tank/report%20final.txt",  # a literal `%20`, NOT a space
    "/mnt/tank/café.txt",
    "/C:/Temp",  # `:` is legal in a segment
]


@pytest.mark.requires("asyncssh")
@pytest.mark.parametrize("remote", _SPECIAL_NAMES)
def test_every_leg_of_a_host_path_names_the_decoded_file(remote):
    """The SFTP leg and the websocket leg address the same name, byte for byte.

    A `?` or `#` read as URI syntax would truncate the name into a query or
    fragment, and a genuine `%xx` decoded once more would name another file --
    either way the operation runs against a different file with no error.
    Building an absolute path connects nothing.
    """
    host = TrueNASClient("wss://nas", autologin=False, ssh=_ssh_config(port=2222))
    sftp = host.path(remote, backend="sftp")
    ws = host.path(remote, backend="tnasws")
    assert str(sftp._backend_path) == remote
    assert ws._backend_path.path == remote
    assert fs_path(host, remote, backend="ws").path == remote


# -- the truenas:// URI is built the same way, one layer up --------------------


def _path_client(ssh=None):
    """A remote fake host shaped for `pytruenas.fs.path(..., backend="ws")`.

    `path()` reads `is_local`/`host` off the host's `_config`.
    """
    return SimpleNamespace(
        _config=SimpleNamespace(is_local=False, host="nas", port=0),
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
    [("ws", TnasWsPath), ("api", TnasWsPath)],
)
def test_path_construction_survives_uri_syntax_in_a_filename(remote, backend, expected):
    """A name holding URI syntax survives construction unchanged.

    A truncated name at construction would send every `filesystem.*` call to
    another file. What is pinned is the round-trip, not the encoded spelling.
    """
    p = fs_path(_path_client(), remote, backend=backend)
    assert isinstance(p, expected)
    assert p.path == remote


def test_path_construction_leaves_uri_legal_characters_readable():
    """Encoding is minimal, as on the SFTP leg: `:` is legal in a segment."""
    p = fs_path(_path_client(), "/C:/Temp", backend="ws")
    assert str(p) == "truenas+ws://nas/C:/Temp"
    assert p.path == "/C:/Temp"


def test_path_construction_brackets_an_ipv6_host():
    """An IPv6 literal is bracketed in the authority, or its colons read as a
    port."""
    client = _path_client()
    client._config.host = "fd00::1"
    p = fs_path(client, "/mnt/x", backend="ws")
    assert str(p) == "truenas+ws://[fd00::1]/mnt/x"
    assert p.path == "/mnt/x"


def test_path_construction_joins_segments_before_encoding():
    """A `/` between segments is a separator, not part of a name."""
    p = fs_path(_path_client(), "/mnt/tank", "a?b", "c#d", backend="ws")
    assert p.path == "/mnt/tank/a?b/c#d"
    assert p.name == "c#d"


def test_an_absolute_later_segment_restarts_the_path_on_every_leg():
    """`client.path("/mnt", "/etc")` named `/etc`, while its websocket leg
    operated on `/mnt//etc` -- `unlink()` removed a different file."""
    assert fs_path(_path_client(), "/mnt", "/etc", backend="ws").path == "/etc"
    from pytruenas.providers import TnasWsPathProvider

    host = TrueNASClient("wss://nas.example", autologin=False)
    assert TnasWsPathProvider(host)._make_path("/mnt", "/etc").path == "/etc"


# -- symlink_to(force=) must not remove before it can create ------------------


class _LinkPath:
    """Just enough path to record what `fs.symlink_to` does to it."""

    def __init__(self, kind=None):
        self.kind = kind  # None: absent; "file", "directory" or "link"
        self.calls = []

    def exists(self):
        return self.kind is not None

    def is_symlink(self):
        return self.kind == "link"

    def is_dir(self):
        return self.kind == "directory"

    def is_file(self):
        return self.kind == "file"

    def unlink(self):
        self.calls.append("unlink")

    def rm(self, recursive=False, missing_ok=False):
        self.calls.append(("rm", recursive))

    def _symlink_to(self, target, target_is_directory=False):
        raise AssertionError("fs.symlink_to calls the public method")

    def symlink_to(self, target, target_is_directory=False):
        self.calls.append(("symlink", target, target_is_directory))


def test_symlink_to_force_does_not_remove_when_nothing_can_create():
    """A websocket-only host cannot make a symlink, so `force=` must not delete.

    Removing first and then failing would be pure loss.
    """
    host = _ws_only_host(stat={"mode": 0o100644})
    with pytest.raises(NotImplementedError):
        fs_symlink_to(host.path("/link"), "/target", force=True)
    assert not host.api.filesystem.stat.called
    assert not host.api.filesystem.put.called


def test_symlink_to_force_removes_then_creates():
    p = _LinkPath("file")
    fs_symlink_to(p, "/target", force=True)
    assert p.calls == ["unlink", ("symlink", "/target", False)]
    d = _LinkPath("directory")
    fs_symlink_to(d, TnasWsPath("truenas+ws://nas/t", backend=None), True, force=True)
    assert d.calls == [("rm", True), ("symlink", "/t", True)]


def test_symlink_to_without_force_leaves_a_conflict_to_the_leg():
    p = _LinkPath("file")
    fs_symlink_to(p, "/target")
    assert p.calls == [("symlink", "/target", False)]


def test_symlink_to_force_honours_onremove_veto():
    p = _LinkPath("link")
    fs_symlink_to(p, "/target", force=True, onremove=lambda _p, _kind: False)
    assert p.calls == [("symlink", "/target", False)]


def test_symlink_to_force_rejects_a_kind_it_was_not_allowed():
    p = _LinkPath("file")
    with pytest.raises(FileExistsError):
        fs_symlink_to(p, "/target", force="link")
    assert p.calls == []
    q = _LinkPath("link")
    fs_symlink_to(q, "/target", force=["link", "file"])
    assert q.calls[0] == "unlink"


@pytest.mark.requires("asyncssh")
def test_a_host_path_with_an_sftp_leg_can_create_a_symlink():
    """Construction only: the composite path claims the operation for SFTP."""
    from pathapi.protocols import Symlink, supports

    host = TrueNASClient("wss://nas", autologin=False, ssh=_ssh_config())
    assert supports(host.path("/link"), Symlink)
