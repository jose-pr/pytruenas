"""patch.systemd.SystemFile and patch.middleware against a recording client.

Files live under a temporary directory (``client.path("/etc/x")`` is
``tmp_path / "etc/x"``); middleware calls and commands are recorded, so what
the patch says to the host is asserted without one.
"""

from __future__ import annotations

import pytest

from pytruenas.patch.systemd import SystemFile


class _Result:
    def __init__(self, returncode=0, stdout=""):
        self.returncode = returncode
        self.stdout = stdout


class _Method:
    def __init__(self, client, name):
        self._client, self._name = client, name

    def __getattr__(self, name):
        return _Method(self._client, f"{self._name}.{name}")

    def __call__(self, *args):
        self._client.api_calls.append((self._name, args))
        failure = self._client.fail_api.get(self._name)
        if failure is not None:
            raise failure


class _Api:
    def __init__(self, client):
        self._client = client

    def __getattr__(self, name):
        return _Method(self._client, name)


class _Client:
    """``path()`` maps into ``root``; ``api.*`` and ``run()`` are recorded.

    ``readonly`` models one ZFS dataset holding every path: ``zfs get``
    answers from it and ``zfs set`` changes it.
    """

    def __init__(self, root, readonly=False):
        self.root = root
        self.api = _Api(self)
        self.api_calls = []
        self.fail_api = {}
        self.runs = []
        self.readonly = readonly

    def path(self, path):
        return self.root / str(path).lstrip("/")

    def run(self, argv, check=True, capture_output=None, encoding=None, **kwargs):
        argv = list(argv)
        self.runs.append(argv)
        if argv[0] == "findmnt":
            return _Result(0, "zfs boot-pool/ROOT/26.0/usr\n")
        if argv[:2] == ["zfs", "get"]:
            value = "on" if self.readonly else "off"
            return _Result(0, f"readonly\t{value}\tlocal\n")
        if argv[:2] == ["zfs", "set"]:
            for pair in argv[2:-1]:
                name, _, value = pair.partition("=")
                if name == "readonly":
                    self.readonly = value == "on"
            return _Result(0)
        return _Result(0)

    def zfs_sets(self):
        return [argv[2:-1] for argv in self.runs if argv[:2] == ["zfs", "set"]]


@pytest.fixture
def client(tmp_path):
    return _Client(tmp_path)


def test_each_etc_group_is_regenerated_by_its_own_call(client):
    target = SystemFile("/etc/app.conf", client, etc="a,b", services="nfs,smb")
    assert target.write("v1\n") is True
    assert client.api_calls == [
        ("etc.generate", ("a",)),
        ("etc.generate", ("b",)),
        ("service.reload", ("nfs",)),
        ("service.reload", ("smb",)),
    ]


def test_an_unchanged_write_notifies_nothing(client):
    target = SystemFile("/etc/app.conf", client, etc="a", services="nfs")
    target.write("v1\n")
    client.api_calls.clear()
    assert target.write("v1\n") is False
    assert client.api_calls == []


def test_revert_notifies_as_a_write_does(client):
    (client.root / "etc").mkdir()
    (client.root / "etc" / "app.conf").write_bytes(b"stock\n")
    target = SystemFile("/etc/app.conf", client, etc="a", services="nfs")
    target.write("patched\n")
    client.api_calls.clear()

    assert target.revert() is True
    assert (client.root / "etc" / "app.conf").read_bytes() == b"stock\n"
    assert client.api_calls == [("etc.generate", ("a",)), ("service.reload", ("nfs",))]

    client.api_calls.clear()
    assert target.revert() is False  # nothing left to undo
    assert client.api_calls == []


# -- the writable window --------------------------------------------------------


def test_writable_opens_the_window_only_for_a_real_change(tmp_path):
    client = _Client(tmp_path, readonly=True)
    target = SystemFile("/usr/lib/x.conf", client, writable=True, baseline=False)

    assert target.write("v1\n") is True
    assert client.zfs_sets()[0][0] == "readonly=off"
    assert client.readonly is True  # restored

    client.runs.clear()
    assert target.write("v1\n") is False
    assert client.zfs_sets() == []
    assert not [argv for argv in client.runs if argv[0] == "findmnt"]


def test_revert_happens_inside_the_window(tmp_path):
    client = _Client(tmp_path, readonly=True)
    (tmp_path / "usr").mkdir()
    (tmp_path / "usr" / "x.conf").write_bytes(b"stock\n")
    target = SystemFile("/usr/x.conf", client, writable=True)
    target.write("patched\n")
    client.runs.clear()

    assert target.revert() is True
    assert (tmp_path / "usr" / "x.conf").read_bytes() == b"stock\n"
    assert client.zfs_sets()[0][0] == "readonly=off"
    assert client.readonly is True


# -- a failed follow-up is retried, not lost ------------------------------------


def test_a_failed_notify_puts_the_previous_content_back(client):
    path = client.root / "etc" / "app.conf"
    path.parent.mkdir()
    path.write_bytes(b"stock\n")
    target = SystemFile("/etc/app.conf", client, services="nfs")

    client.fail_api["service.reload"] = RuntimeError("reload failed")
    with pytest.raises(RuntimeError, match="reload failed"):
        target.write("patched\n")
    assert path.read_bytes() == b"stock\n"

    # The next apply sees the change again and notifies.
    del client.fail_api["service.reload"]
    client.api_calls.clear()
    assert target.write("patched\n") is True
    assert client.api_calls == [("service.reload", ("nfs",))]


def test_a_failed_notify_removes_a_file_the_write_created(client):
    target = SystemFile("/etc/new.conf", client, etc="a")
    client.fail_api["etc.generate"] = RuntimeError("generate failed")
    with pytest.raises(RuntimeError):
        target.write("v1\n")
    assert not (client.root / "etc" / "new.conf").exists()

    del client.fail_api["etc.generate"]
    assert target.write("v1\n") is True


def test_a_failed_notify_on_revert_keeps_the_patch_and_its_baseline(client):
    path = client.root / "etc" / "app.conf"
    path.parent.mkdir()
    path.write_bytes(b"stock\n")
    target = SystemFile("/etc/app.conf", client, services="nfs")
    target.write("patched\n")

    client.fail_api["service.reload"] = RuntimeError("reload failed")
    with pytest.raises(RuntimeError):
        target.revert()
    assert path.read_bytes() == b"patched\n"
    assert (client.root / "etc" / "app.conf.baseline").read_bytes() == b"stock\n"

    del client.fail_api["service.reload"]
    assert target.revert() is True
    assert path.read_bytes() == b"stock\n"
    assert not (client.root / "etc" / "app.conf.baseline").exists()
