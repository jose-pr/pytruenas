"""patch.systemd.SystemFile and patch.middleware against a recording client.

Files live under a temporary directory (``client.path("/etc/x")`` is
``tmp_path / "etc/x"``); middleware calls and commands are recorded, so what
the patch says to the host is asserted without one.
"""

from __future__ import annotations

import pytest

from pytruenas.patch.middleware import MiddlewareFiles, middlewared_path
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
        self.python_answer = ""

    def path(self, path):
        text = str(path)
        if text.startswith(str(self.root)):  # already a path on this host
            return type(self.root)(text)
        return self.root / text.lstrip("/")

    def run(self, argv, check=True, capture_output=None, encoding=None, **kwargs):
        argv = list(argv)
        self.runs.append(argv)
        if argv[0] == "python3":
            return _Result(0, self.python_answer)
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


# -- MiddlewareFiles ------------------------------------------------------------

_PACKAGE = "/usr/lib/python3/dist-packages/middlewared"


def _package(client, files):
    """Create ``files`` (relative to the package) under the fake host."""
    for name, data in files.items():
        path = client.path(f"{_PACKAGE}/{name}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return MiddlewareFiles(client, module_path=_PACKAGE)


def test_middlewared_path_asks_the_hosts_interpreter(client):
    client.python_answer = f"{_PACKAGE}\n"
    assert middlewared_path(client) == client.path(_PACKAGE)
    assert client.runs[-1][:2] == ["python3", "-c"]


def test_middlewared_path_raises_on_an_empty_answer(client):
    client.python_answer = "\n"
    with pytest.raises(RuntimeError, match="could not locate"):
        middlewared_path(client)


def test_repr_does_not_locate_the_package(client):
    assert repr(MiddlewareFiles(client)) == "MiddlewareFiles(<unresolved>)"
    assert client.runs == []


def test_find_template_adds_mako_and_passes_its_options(client):
    files = _package(client, {"etc_files/nginx.conf.mako": b"stock\n"})
    target = files.find_template("nginx.conf", etc="nginx", writable=True)
    assert target.path == client.path(f"{_PACKAGE}/etc_files/nginx.conf.mako")
    assert target.etc == ("nginx",)
    assert target.writable is True
    assert target.baseline_path is not None  # baseline=True by default


def test_find_template_takes_the_first_directory_that_has_it(client):
    files = _package(
        client,
        {"etc_files/x.conf": b"stock\n", "etc_files/local/x.conf": b"local\n"},
    )
    assert files.find_template("x.conf").read() == b"stock\n"


def test_find_template_names_every_location_it_tried(client):
    files = _package(client, {"etc_files/other": b""})
    with pytest.raises(FileNotFoundError) as caught:
        files.find_template("missing.conf")
    message = str(caught.value)
    assert message.count("missing.conf") == 5  # the name, then four locations
    assert "local" in message and ".mako" in message


def test_a_template_with_only_its_baseline_left_is_found(client):
    files = _package(client, {"etc_files/x.conf.baseline": b"stock\n"})
    target = files.find_template("x.conf")
    assert target.read() == b"stock\n"


def test_find_file_honours_the_targets_own_baseline_suffix(client):
    files = _package(client, {"etc_files/x.conf.orig": b"stock\n"})
    target = files.find_file("etc_files/x.conf", baseline=".orig")
    assert target.read() == b"stock\n"
    with pytest.raises(FileNotFoundError):
        files.find_file("etc_files/x.conf")  # default suffix: nothing there
