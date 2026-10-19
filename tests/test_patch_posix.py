"""pytruenas.patch through a real host: hostctl's local paths and executor.

Everything else in the patch suite uses hand-rolled path and client doubles;
this module checks the same behaviour through ``client.path()`` and
``client.run()`` as a caller gets them, on a real POSIX filesystem under
``tmp_path``. ``systemctl``, ``zfs`` and ``findmnt`` are recording stand-ins
put first on ``PATH``, so no real unit or dataset is touched.
"""

from __future__ import annotations

import os
import shutil
import stat
import sys
import textwrap

import pytest

from pytruenas import TrueNASClient
from pytruenas.patch import zfs
from pytruenas.patch.systemd import ServiceUnit, SystemFile, units
from pytruenas.patch.templates import FileTarget

pytestmark = pytest.mark.skipif(
    os.name != "posix" or not os.path.exists("/bin/sh"),
    reason="needs a POSIX host: real modes, symlinks and a local shell",
)

_SYSTEMCTL = """\
#!/bin/sh
{ printf 'systemctl'; for arg in "$@"; do printf '\\t%s' "$arg"; done; echo; } >> "$PATCH_LOG"
case "$1" in
  is-enabled) [ -e "$PATCH_STATE/$2.enabled" ]; exit $? ;;
  is-active) [ -e "$PATCH_STATE/$2.active" ]; exit $? ;;
  enable) : > "$PATCH_STATE/$2.enabled" ;;
  start) : > "$PATCH_STATE/$2.active" ;;
  stop) rm -f "$PATCH_STATE/$2.active" ;;
  disable) rm -f "$PATCH_STATE/$2.enabled"
           if [ "$3" = "--now" ]; then rm -f "$PATCH_STATE/$2.active"; fi ;;
esac
exit 0
"""

_ZFS = """\
#!{python}
import json, os, sys
state = os.path.join(os.environ["PATCH_STATE"], "zfs.json")
props = json.load(open(state)) if os.path.exists(state) else {{"readonly": "on"}}
args = sys.argv[1:]
with open(os.environ["PATCH_LOG"], "a") as log:
    log.write("\\t".join(["zfs"] + args) + "\\n")
if args[0] == "get":
    fields = args[args.index("-o") + 1].split(",")
    for name in args[-2].split(","):
        row = {{"property": name, "value": props.get(name, "-"), "source": "local"}}
        print("\\t".join(row[field] for field in fields))
elif args[0] == "set":
    props.update(pair.split("=", 1) for pair in args[1:-1])
elif args[0] == "inherit":
    props.pop(args[-2], None)
json.dump(props, open(state, "w"))
"""

_FINDMNT = """\
#!/bin/sh
echo "zfs boot-pool/ROOT/fake/usr"
"""


@pytest.fixture
def host(tmp_path, monkeypatch):
    """A local host whose systemctl/zfs/findmnt are the stand-ins above."""
    bin_dir, state = tmp_path / "bin", tmp_path / "state"
    bin_dir.mkdir()
    state.mkdir()
    shims = {
        "systemctl": _SYSTEMCTL,
        "zfs": _ZFS.format(python=sys.executable),
        "findmnt": _FINDMNT,
    }
    for name, text in shims.items():
        (bin_dir / name).write_bytes(text.encode())
        (bin_dir / name).chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("PATCH_LOG", str(tmp_path / "commands.log"))
    monkeypatch.setenv("PATCH_STATE", str(state))
    monkeypatch.setattr(units, "UNIT_DIR", str(tmp_path / "units"))
    return TrueNASClient(None, autologin=False)


def _commands(tmp_path):
    log = tmp_path / "commands.log"
    lines = log.read_text().splitlines() if log.exists() else []
    log.write_text("")
    return [line.split("\t") for line in lines]


def _mode(path):
    return stat.S_IMODE(os.lstat(path).st_mode)


@pytest.fixture(autouse=True)
def _umask():
    previous = os.umask(0o022)
    yield
    os.umask(previous)


def test_modes_survive_a_patch_and_its_revert(host, tmp_path):
    secret = tmp_path / "shadow"
    secret.write_bytes(b"root:HASH:1\n")
    secret.chmod(0o640)
    target = FileTarget(host.path(str(secret)), baseline=True)

    assert target.write("root:NEW:1\n") is True
    assert _mode(secret) == 0o640
    assert _mode(str(secret) + ".baseline") == 0o640
    assert target.write("root:NEW:1\n") is False
    assert target.revert() is True
    assert secret.read_bytes() == b"root:HASH:1\n"
    assert _mode(secret) == 0o640
    assert sorted(p.name for p in tmp_path.iterdir() if "shadow" in p.name) == [
        "shadow"
    ]


def test_a_created_file_gets_its_mode_and_parents(host, tmp_path):
    created = tmp_path / "sub" / "dir" / "new.conf"
    target = FileTarget(host.path(str(created)), baseline=True, mode=0o600)
    assert target.write("token=abc\n") is True
    assert _mode(created) == 0o600
    assert _mode(created.parent) == 0o755
    assert target.revert() is False  # created by the patch: left in place
    assert created.exists()


def test_a_symlinked_baseline_is_refused_and_its_target_untouched(host, tmp_path):
    victim = tmp_path / "victim.txt"
    victim.write_bytes(b"do not overwrite\n")
    config = tmp_path / "app.conf"
    config.write_bytes(b"orig\n")
    os.symlink(victim, str(config) + ".baseline")

    target = FileTarget(host.path(str(config)), baseline=True)
    with pytest.raises(PermissionError):
        target.write("patched\n")
    with pytest.raises(PermissionError):
        target.revert()
    assert victim.read_bytes() == b"do not overwrite\n"
    assert config.read_bytes() == b"orig\n"


def test_a_unit_is_written_reloaded_and_started_through_run(host, tmp_path):
    unit = ServiceUnit(
        host, "my-agent", cmd="/opt/my agent/run --flag='x y'", restart_on_change=True
    )
    assert unit.apply() is True
    text = (tmp_path / "units" / "my-agent.service").read_text()
    assert "ExecStart = /opt/my agent/run --flag='x y'" in text
    assert _commands(tmp_path) == [
        ["systemctl", "daemon-reload"],
        ["systemctl", "try-restart", "my-agent.service"],
        ["systemctl", "is-enabled", "my-agent.service"],
        ["systemctl", "enable", "my-agent.service"],
        ["systemctl", "is-active", "my-agent.service"],
        ["systemctl", "start", "my-agent.service"],
    ]

    assert unit.apply() is False
    assert [argv[1] for argv in _commands(tmp_path)] == ["is-enabled", "is-active"]

    assert unit.uninstall() is True
    assert not (tmp_path / "units" / "my-agent.service").exists()
    assert ["systemctl", "disable", "my-agent.service", "--now"] in _commands(tmp_path)


@pytest.mark.skipif(not shutil.which("systemd-escape"), reason="needs systemd-escape")
def test_mount_unit_names_come_from_the_real_systemd_escape(host):
    assert units.MountUnit(host, "/", what="x").name == "-.mount"
    assert (
        units.MountUnit(host, "/mnt/tank/my-share", what="x").name
        == "mnt-tank-my\\x2dshare.mount"
    )


def test_writable_window_through_run(host, tmp_path):
    target = SystemFile(
        str(tmp_path / "usr" / "x.conf"), host, writable=True, baseline=False
    )
    assert target.write("v1\n") is True
    calls = [argv for argv in _commands(tmp_path) if argv[0] == "zfs"]
    assert calls[1] == [
        "zfs",
        "set",
        "readonly=off",
        "pytruenas:restore-readonly=on",
        "boot-pool/ROOT/fake/usr",
    ]
    assert ["zfs", "set", "readonly=on", "boot-pool/ROOT/fake/usr"] in calls
    assert target.write("v1\n") is False
    assert _commands(tmp_path) == []  # unchanged: no window at all


def test_a_failed_restore_keeps_the_bodys_error(host, tmp_path, monkeypatch):
    zfs_shim = tmp_path / "bin" / "zfs"
    zfs_shim.write_text(
        zfs_shim.read_text().replace(
            'elif args[0] == "set":',
            textwrap.dedent("""\
                elif args[0] == "set" and "readonly=on" in args:
                    sys.exit("cannot set property")
                elif args[0] == "set":"""),
        )
    )
    with pytest.raises(ValueError, match="the body failed"):
        with zfs.writable(host, host.path(str(tmp_path / "usr" / "x"))):
            raise ValueError("the body failed")


@pytest.mark.skipif(not shutil.which("findmnt"), reason="needs findmnt")
def test_a_path_not_on_zfs_is_left_alone_with_the_real_findmnt(host, tmp_path):
    (tmp_path / "bin" / "findmnt").unlink()  # the host's own findmnt answers
    with zfs.writable(host, host.path(str(tmp_path))) as source:
        assert source
    assert not [argv for argv in _commands(tmp_path) if argv[0] == "zfs"]
    with pytest.raises(ValueError, match="not a ZFS dataset"):
        zfs.dataset_for(host, str(tmp_path))
