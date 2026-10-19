# Patching a host

`pytruenas.patch` is a toolkit for changing a TrueNAS host beyond what the
middleware API exposes: a systemd unit for a daemon TrueNAS has no concept of,
a file under `/etc`, a line added to one of the middleware's own templates.
It is a supported part of pytruenas, versioned like the rest of the package.

What TrueNAS does not support is the change itself. The middleware owns the
appliance's configuration, `/usr` is a read-only dataset, and an update boots
a new environment that has none of your changes. So a patch here is written to
be **re-applied**: after an update, after a reboot, or every time a deploy
runs. Applying it to a host that already has it changes nothing and restarts
nothing, and every piece can be undone.

## What the toolkit does for you

- **Change detection.** Every write compares content first and returns
  whether anything changed. The follow-up work -- `systemctl daemon-reload`,
  regenerating an etc group, reloading a service -- runs only when it did.
- **Baselines and undo.** A file target with `baseline=True` copies the
  original aside (`<name>.baseline`) before its first change, templates from
  that copy ever after, and `revert()` puts it back. A file the patch created
  is recorded as such (`<name>.baseline.absent`) and left in place by
  `revert()`.
- **Regenerated files.** Each change also records digests of what it wrote
  (`<name>.baseline.applied`). When the middleware rewrites the file later --
  after a settings change in the UI, say -- that content becomes the original:
  the next apply layers onto it, and `revert()` leaves it alone.
- **Failed follow-ups are retried.** If the reload after a change fails, the
  previous content is put back before the error is raised, so the next apply
  sees the change again instead of finding the file already written.
- **Permissions survive.** A rewritten file keeps its mode; `mode=` sets the
  mode of a file the patch creates, before any content is written.
- **Read-only datasets.** `writable=True` (or `zfs.writable()`) clears
  `readonly` on the dataset holding a path for the duration of the write and
  restores it however the write ends.
- **Declared unit state.** A unit's `enable`/`start` are reconciled against
  what systemd reports; `None` means "leave it alone".

## The pieces

| Piece | Use it for |
| --- | --- |
| `BasicTemplate(text)` | text with `%{NAME}` placeholders filled from a dict or object |
| `TextTemplate(text)` | literal text |
| a `BaseTemplate` subclass | anything else: `render(context)` returns the text; built with the target's original content when passed as a class to `apply_template` |
| `FileTarget(path, baseline=, mode=)` | a file reached through any path object |
| `SystemFile(path, client, etc=, services=, baseline=True, writable=False, mode=)` | a file on the host, plus the etc groups to regenerate and services to reload when it changes |
| `ServiceUnit` / `MountUnit` / `AutomountUnit` | a systemd unit: `apply()` writes it, reloads systemd and reconciles enable/start; `uninstall()` removes it |
| `MiddlewareFiles(client).find_template(name, ...)` | one of the middleware's own `etc_files` templates, as a `SystemFile` |
| `zfs.writable(client, path)` | a context manager making the dataset under `path` writable |

The full signatures and contracts are in the package's API header
(`src/pytruenas/AGENTS.md`, section `patch`).

## A complete patch

The patch below installs an agent: its config file, rendered from a template;
a systemd unit that runs it; and a change layered onto the middleware's own
`sshd_config` template, which the middleware then regenerates
`/etc/ssh/sshd_config` from before the ssh service reloads.

```python
from pytruenas.patch import (
    BaseTemplate,
    BasicTemplate,
    MiddlewareFiles,
    ServiceUnit,
    SystemFile,
)

AGENT = "/mnt/tank/apps/agent/bin/agent"

CONFIG = """\
listen = 0.0.0.0:%{PORT}
data = %{DATA}
"""


class SshdKeepalive(BaseTemplate):
    """Adds two lines to the stock sshd_config template."""

    def __init__(self, stock: bytes):
        self.stock = stock.decode()

    def render(self, context):
        return self.stock + "ClientAliveInterval 300\nClientAliveCountMax 3\n"


def sshd_template(nas):
    # The template lives in the middlewared package on the read-only /usr
    # dataset, so the write needs `writable=True`.
    return MiddlewareFiles(nas).find_template(
        "ssh/sshd_config", etc="ssh", services="ssh", writable=True
    )


def install(nas, port=9100, data="/mnt/tank/apps/agent/data"):
    """Apply the whole patch; return whether anything changed."""
    config = SystemFile("/etc/agent.conf", nas, baseline=False, mode=0o640)
    config_changed = BasicTemplate(CONFIG).apply(config, {"port": port, "data": data})

    unit = ServiceUnit(
        nas,
        "agent",
        cmd=f"{AGENT} --config /etc/agent.conf",
        description="Example agent",
        restart_on_change=True,
    )
    unit_changed = unit.apply()  # write if changed, daemon-reload, enable, start
    if config_changed and not unit_changed:
        unit.restart()  # same unit, new config

    sshd_changed = sshd_template(nas).apply_template(SshdKeepalive)

    return config_changed or unit_changed or sshd_changed


def uninstall(nas):
    """Undo install(): the stock template comes back, the unit goes."""
    sshd_template(nas).revert()
    ServiceUnit(nas, "agent").uninstall()
    nas.path("/etc/agent.conf").unlink(missing_ok=True)
```

`SshdKeepalive` is passed as a class, so `apply_template` builds it from the
template's *original* content: the stock file the first time, its baseline
copy every time after. That is what keeps a second apply from adding the lines
twice.

## Trying it without a NAS

A patch only needs `client.path()`, `client.run()` and `client.api`, so it runs
against a stand-in. This one keeps files under a local directory, answers
`systemctl` and `zfs` from memory, and records every command and middleware
call -- enough to see what the patch would do, or to test your own:

```python
import pathlib
import subprocess


class FakeNAS:
    """A stand-in for TrueNASClient, for running a patch offline."""

    PACKAGE = "/usr/lib/python3/dist-packages/middlewared"

    def __init__(self, root):
        self.root = pathlib.Path(root)
        self.commands = []  # the argv of every run()
        self.calls = []  # every middleware call, as ("etc.generate", ("ssh",))
        self.units = {}  # unit name -> {"enabled", "active"}
        self.zfs = {"readonly": "on"}  # the properties of the /usr dataset

    def path(self, path):
        if str(path).startswith(str(self.root)):
            return pathlib.Path(path)
        return self.root / str(path).lstrip("/")

    @property
    def api(self):
        return _Call(self.calls)

    def run(self, argv, check=False, **kwargs):
        argv = [str(arg) for arg in argv]
        self.commands.append(argv)
        out, status = "", 0
        if argv[0] == "systemctl" and len(argv) > 2:
            state = self.units.setdefault(argv[2], set())
            verb = argv[1]
            if verb in ("is-enabled", "is-active"):
                status = 0 if verb[3:] in state else 1  # the answer is the status
            elif verb == "enable":
                state.add("enabled")
            elif verb == "start":
                state.add("active")
            elif verb == "disable":
                state.discard("enabled")
                if "--now" in argv:
                    state.discard("active")
            elif verb == "stop":
                state.discard("active")
        elif argv[0] == "python3":  # where is the middlewared package?
            out = self.PACKAGE + "\n"
        elif argv[0] == "findmnt":
            out = "zfs boot-pool/ROOT/26.0/usr\n"
        elif argv[:2] == ["zfs", "get"]:
            names = argv[-2].split(",")
            out = "".join(f"{name}\t{self.zfs.get(name, '-')}\tlocal\n" for name in names)
        elif argv[:2] == ["zfs", "set"]:
            self.zfs.update(pair.split("=", 1) for pair in argv[2:-1])
        elif argv[:2] == ["zfs", "inherit"]:
            self.zfs.pop(argv[-2], None)
        return subprocess.CompletedProcess(argv, status, out, "")


class _Call:
    """`nas.api.etc.generate("ssh")` records ("etc.generate", ("ssh",))."""

    def __init__(self, calls, name=""):
        self._calls, self._name = calls, name

    def __getattr__(self, name):
        return _Call(self._calls, f"{self._name}.{name}".lstrip("."))

    def __call__(self, *args):
        self._calls.append((self._name, args))
```

Seed it with the stock template, then apply the patch twice:

```python
import tempfile

nas = FakeNAS(tempfile.mkdtemp())
stock = nas.path(FakeNAS.PACKAGE + "/etc_files/ssh/sshd_config.mako")
stock.parent.mkdir(parents=True)
stock.write_bytes(b"Port 22\n")

assert install(nas) is True
assert nas.calls == [("etc.generate", ("ssh",)), ("service.reload", ("ssh",))]
assert nas.units["agent.service"] == {"enabled", "active"}
assert nas.zfs["readonly"] == "on"  # opened for the write, then restored

nas.calls.clear()
assert install(nas) is False  # already applied: nothing written, nothing reloaded
assert nas.calls == []

assert install(nas, port=9200) is True  # only the config changed
assert ["systemctl", "restart", "agent.service"] in nas.commands

uninstall(nas)
assert stock.read_bytes() == b"Port 22\n"
assert not nas.path("/etc/systemd/system/agent.service").exists()
```

## Running it against a NAS

Hand `install()` a real client. A patch runs commands on the host (`systemctl`,
`zfs`, `findmnt`, `python3`), so the client needs a working `run()`: over SSH
when one is configured, otherwise over the middleware's web shell -- see
[Running commands](commands.md).

```python
# needs a NAS
from pytruenas import TrueNASClient

nas = TrueNASClient("nas.example.com", "1-<64-char-api-key>")
install(nas)
```

Run it again after every TrueNAS update: the update boots a new environment
without the patch, and re-applying puts back exactly what is missing.

## Things to know

- **The files beside a target are part of the patch.** `<name>.baseline`,
  `<name>.baseline.absent` and `<name>.baseline.applied` hold the original and
  what was written; deleting them while the patch is applied loses the undo.
- **Only trusted files are used.** A baseline, marker or record must be a
  regular file with one link, owned by root or by the target's owner;
  anything else (a symlink, say) raises `PermissionError` rather than being
  read or written through. This matters where a non-root user can write the
  target's directory.
- **`zfs.writable()` marks the dataset** with the user property
  `pytruenas:restore-readonly` while it is open, so a window left open by a
  crash is closed by the next one. Two windows on one dataset at the same time
  (two processes) are not coordinated. A path that is not on ZFS is left
  alone.
- **Unit names get their type.** `ServiceUnit(nas, "my.agent")` is
  `my.agent.service`; a name already ending in a unit type keeps it. List
  values in a unit's `conf` render as repeated keys
  (`{"Service": {"ExecStartPre": ["/a", "/b"]}}`).
- **A changed unit is reloaded, not restarted,** unless it was built with
  `restart_on_change=True`: a restart interrupts the service, so it is your
  call.
