"""patch/zfs: making a read-only dataset temporarily writable.

The restore-on-exception path is the one that matters most -- leaving /usr
writable because a patch raised halfway is the failure this module exists to
prevent -- so it is tested explicitly rather than assumed from the `finally`.
"""

import pytest

from pytruenas.patch import zfs


class _Result:
    def __init__(self, stdout="", returncode=0):
        self.stdout = stdout
        self.returncode = returncode


class _FakeClient:
    """Answers findmnt/zfs-get from state; records zfs-set calls."""

    def __init__(self, dataset="boot-pool/ROOT/26.0/usr", readonly=True):
        self.dataset = dataset
        self.readonly = readonly
        self.calls = []
        self.fail_on_restore = False

    def run(self, argv, check=True, capture_output=None, encoding=None, **kwargs):
        self.calls.append(list(argv))
        if argv[0] == "findmnt":
            return _Result(self.dataset + "\n")
        if argv[:2] == ["zfs", "get"]:
            return _Result(("on" if self.readonly else "off") + "\n")
        if argv[:2] == ["zfs", "set"]:
            value = argv[2].split("=", 1)[1]
            if value == "on" and self.fail_on_restore:
                raise RuntimeError("zfs set failed")
            self.readonly = value == "on"
            return _Result()
        return _Result()

    def sets(self):
        return [c[2] for c in self.calls if c[:2] == ["zfs", "set"]]


def test_dataset_for_asks_the_host():
    client = _FakeClient(dataset="boot-pool/ROOT/26.0/usr")
    assert zfs.dataset_for(client, "/usr/lib/x") == "boot-pool/ROOT/26.0/usr"
    assert client.calls[0][:2] == ["findmnt", "--noheadings"]
    assert "--target" in client.calls[0]


def test_dataset_for_raises_on_an_empty_answer():
    client = _FakeClient(dataset="")
    with pytest.raises(RuntimeError, match="could not determine the dataset"):
        zfs.dataset_for(client, "/nowhere")


def test_is_readonly_reads_the_property():
    assert zfs.is_readonly(_FakeClient(readonly=True), "pool/ds") is True
    assert zfs.is_readonly(_FakeClient(readonly=False), "pool/ds") is False


def test_writable_flips_and_restores():
    client = _FakeClient(readonly=True)
    with zfs.writable(client, "/usr") as dataset:
        assert dataset == client.dataset
        assert client.readonly is False  # writable inside
    assert client.readonly is True  # restored after
    assert client.sets() == ["readonly=off", "readonly=on"]


def test_writable_restores_even_when_the_body_raises():
    """The whole reason this is a context manager."""
    client = _FakeClient(readonly=True)
    with pytest.raises(ValueError):
        with zfs.writable(client, "/usr"):
            assert client.readonly is False
            raise ValueError("patch failed")
    assert client.readonly is True
    assert client.sets() == ["readonly=off", "readonly=on"]


def test_writable_is_a_noop_when_already_writable():
    """Nothing is set, so nothing is 'restored' to a value it never had."""
    client = _FakeClient(readonly=False)
    with zfs.writable(client, "/var/db/system"):
        assert client.readonly is False
    assert client.sets() == []


def test_a_failed_restore_is_logged_loudly_and_raised(caplog):
    """A silently-writable root would be worse than a noisy failure."""
    import logging

    client = _FakeClient(readonly=True)
    client.fail_on_restore = True
    with caplog.at_level(logging.ERROR, logger="pytruenas.patch.zfs"):
        with pytest.raises(RuntimeError, match="zfs set failed"):
            with zfs.writable(client, "/usr"):
                pass
    assert any("still WRITABLE" in record.getMessage() for record in caplog.records)


def test_set_readonly_builds_one_argv():
    client = _FakeClient()
    zfs.set_readonly(client, "pool/ds", False)
    assert client.calls[-1] == ["zfs", "set", "readonly=off", "pool/ds"]


# -- host_path ------------------------------------------------------------


def test_host_path_accepts_str_and_pure_paths():
    from pathlib import PurePosixPath

    assert zfs.host_path("/usr/lib/x") == "/usr/lib/x"
    assert zfs.host_path(PurePosixPath("/usr/lib/x")) == "/usr/lib/x"


def test_host_path_unwraps_a_uripath_and_never_leaks_credentials():
    """A UriPath renders three ways, and two of them are wrong for argv.

    `str()` gives a whole URI, `as_posix()` gives scp syntax, `os.fspath()`
    raises. Only `.path` is the host-local filesystem path -- and getting this
    wrong would put a URI (historically, with credentials in it) into a command
    line. Filed upstream as 2026-07-29_uripath_fspath_refuses_remote_schemes.
    """
    sftp = pytest.importorskip("pathlib_next.uri.schemes.sftp")

    path = sftp.SftpPath("sftp://root:hunter2@nas/usr/lib/x.conf")
    assert zfs.host_path(path) == "/usr/lib/x.conf"
    assert "hunter2" not in zfs.host_path(path)
    assert "nas" not in zfs.host_path(path)
    assert "sftp://" not in zfs.host_path(path)


def test_dataset_for_walks_up_to_an_existing_ancestor():
    """`findmnt --target` FAILS on a path that does not exist yet.

    Which is the ordinary "create a new config file here" case, so it must not
    be an error.
    """

    class _Walking(_FakeClient):
        def __init__(self):
            super().__init__()
            self.answers_for = "/usr"
            self.targets = []

        def run(self, argv, check=True, **kwargs):
            if argv[0] == "findmnt":
                target = argv[-1]
                self.targets.append(target)
                if target == self.answers_for:
                    return _Result("boot-pool/ROOT/26.0/usr\n", 0)
                return _Result("", 1)
            return super().run(argv, check=check, **kwargs)

    client = _Walking()
    assert dataset_for_missing(client) == "boot-pool/ROOT/26.0/usr"
    assert client.targets == [
        "/usr/lib/py/new.conf",
        "/usr/lib/py",
        "/usr/lib",
        "/usr",
    ]


def dataset_for_missing(client):
    return zfs.dataset_for(client, "/usr/lib/py/new.conf")


def test_dataset_for_gives_up_at_the_root():
    class _NeverAnswers(_FakeClient):
        def run(self, argv, check=True, **kwargs):
            if argv[0] == "findmnt":
                return _Result("", 1)
            return super().run(argv, check=check, **kwargs)

    with pytest.raises(RuntimeError, match="could not determine the dataset"):
        zfs.dataset_for(_NeverAnswers(), "/a/b/c")
