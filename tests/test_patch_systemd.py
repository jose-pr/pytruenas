"""patch/systemd: unit rendering and the systemctl calls it makes.

The client is a stand-in that records invocations, so argv shaping and the
idempotence logic are covered without a host. What is deliberately NOT covered
is whether systemd accepts the result -- that needs a real machine.
"""

import io

from pytruenas.patch.systemd import (
    AutomountUnit,
    MountUnit,
    ServiceUnit,
    Unit,
    as_names,
    UnitConfigParser,
)


class _Result:
    def __init__(self, returncode=0, stdout=""):
        self.returncode = returncode
        self.stdout = stdout


class _FakePath:
    def __init__(self, store, path):
        self._store = store
        self._path = path

    def exists(self):
        return self._path in self._store

    def read_bytes(self):
        return self._store[self._path]

    def write_bytes(self, data):
        self._store[self._path] = data

    def unlink(self, missing_ok=False):
        self._store.pop(self._path, None)

    @property
    def parent(self):
        return _FakePath(self._store, self._path.rsplit("/", 1)[0])

    def mkdir(self, *args, **kwargs):
        pass

    def with_name(self, name):
        return _FakePath(self._store, self._path.rsplit("/", 1)[0] + "/" + name)

    @property
    def name(self):
        return self._path.rsplit("/", 1)[-1]

    def resolve(self):
        return self


class _FakeClient:
    """Records every run() argv; answers is-* queries from its state."""

    def __init__(self, enabled=False, active=False, escape="mnt-data"):
        self.calls = []
        self.files = {}
        self.enabled = enabled
        self.active = active
        self._escape = escape

    def path(self, path):
        return _FakePath(self.files, str(path))

    def run(self, argv, check=True, capture_output=None, encoding=None, **kwargs):
        self.calls.append(list(argv))
        if argv[:2] == ["systemctl", "is-enabled"]:
            return _Result(0 if self.enabled else 1)
        if argv[:2] == ["systemctl", "is-active"]:
            return _Result(0 if self.active else 1)
        if argv[0] == "systemd-escape":
            return _Result(0, self._escape + "\n")
        return _Result(0)

    def systemctl_calls(self):
        return [call[1:] for call in self.calls if call and call[0] == "systemctl"]


# -- the parser -----------------------------------------------------------


def test_parser_preserves_option_case():
    # Systemd keys are case-sensitive (ExecStart, not execstart); the default
    # ConfigParser lowercases them, so optionxform is overridden.
    parser = UnitConfigParser()
    parser.read_dict({"Service": {"ExecStart": "/bin/true", "Restart": "always"}})
    out = io.StringIO()
    parser.write(out)
    text = out.getvalue()
    assert "ExecStart = /bin/true" in text
    assert "execstart" not in text


def test_parser_roundtrips_equals_delimiter():
    parser = UnitConfigParser()
    parser.read_string("[Unit]\nDescription = demo\n")
    assert parser["Unit"]["Description"] == "demo"


def test_parser_does_not_interpolate_systemd_specifiers():
    """`%i` is systemd's, not ConfigParser's -- interpolation must be off."""
    parser = UnitConfigParser()
    parser.read_dict({"Service": {"ExecStart": "/bin/echo %i"}})
    out = io.StringIO()
    parser.write(out)
    assert "%i" in out.getvalue()


# -- name / sequence normalization ----------------------------------------


def testas_names_treats_a_bare_string_as_one_name():
    """`services="nfs"` must not iterate into three characters."""
    assert as_names("nfs") == ("nfs",)
    assert as_names("nfs,smb") == ("nfs", "smb")
    assert as_names(["nfs", "smb"]) == ("nfs", "smb")
    assert as_names(None) == ()
    assert as_names("") == ()


def test_unit_name_gets_its_suffix_only_when_missing():
    client = _FakeClient()
    assert Unit(client, "agent").name == "agent.service"
    assert Unit(client, "agent.service").name == "agent.service"
    assert Unit(client, "agent.timer").name == "agent.timer"


# -- rendering ------------------------------------------------------------


def test_service_unit_renders_expected_sections():
    unit = ServiceUnit(_FakeClient(), "agent", cmd="/usr/bin/agent --flag")
    text = unit.render()
    assert "[Unit]" in text and "[Service]" in text and "[Install]" in text
    assert "ExecStart = /usr/bin/agent --flag" in text
    assert "Restart = always" in text
    assert "WantedBy = multi-user.target" in text
    assert "Description = AGENT" in text  # derived from the name


def test_service_unit_accepts_a_path_as_cmd():
    from pathlib import PurePosixPath

    unit = ServiceUnit(_FakeClient(), "agent", cmd=PurePosixPath("/opt/a/run"))
    assert "ExecStart = /opt/a/run" in unit.render()


def test_explicit_conf_survives_the_defaults():
    unit = ServiceUnit(
        _FakeClient(), "agent", cmd="/bin/true", conf={"Service": {"Restart": "no"}}
    )
    assert "Restart = no" in unit.render()


# -- systemctl argv -------------------------------------------------------


def test_systemctl_is_invoked_as_one_argv_not_several_commands():
    """`run()` takes *cmds -- each positional is a SEPARATE command.

    The old code called run("systemctl", "disable", "--now", name), which ran
    four commands rather than one, and hand-quoted the unit name on top.
    """
    client = _FakeClient()
    Unit(client, "agent")._systemctl("disable", "--now")
    assert client.calls == [["systemctl", "disable", "agent.service", "--now"]]


def test_is_queries_do_not_raise_on_nonzero():
    """Their exit code IS the answer, so check must be False for them."""
    seen = {}

    class _Recorder(_FakeClient):
        def run(self, argv, check=True, **kwargs):
            seen[tuple(argv[:2])] = check
            return super().run(argv, check=check, **kwargs)

    unit = Unit(_Recorder(), "agent")
    unit.is_active()
    unit.is_enabled()
    unit._systemctl("start")
    assert seen[("systemctl", "is-active")] is False
    assert seen[("systemctl", "is-enabled")] is False
    assert seen[("systemctl", "start")] is True


# -- declared state reconciliation ----------------------------------------


def test_configure_enables_and_starts_when_absent():
    client = _FakeClient(enabled=False, active=False)
    ServiceUnit(client, "agent", cmd="/bin/true").configure()
    actions = [call[0] for call in client.systemctl_calls()]
    assert "enable" in actions and "start" in actions


def test_configure_is_a_noop_when_already_in_the_desired_state():
    client = _FakeClient(enabled=True, active=True)
    ServiceUnit(client, "agent", cmd="/bin/true").configure()
    actions = [call[0] for call in client.systemctl_calls()]
    assert actions == ["is-enabled", "is-active"]  # queries only


def test_configure_disables_and_stops_when_declared_false():
    client = _FakeClient(enabled=True, active=True)
    ServiceUnit(client, "agent", cmd="/bin/true", enable=False, start=False).configure()
    actions = [call[0] for call in client.systemctl_calls()]
    assert "disable" in actions and "stop" in actions


def test_none_means_leave_alone_which_is_not_false():
    """A distinction the old bool-only API could not express."""
    client = _FakeClient(enabled=True, active=False)
    ServiceUnit(client, "agent", cmd="/bin/true", enable=None, start=None).configure()
    assert client.systemctl_calls() == []


# -- write / uninstall ----------------------------------------------------


def test_write_reloads_only_when_the_file_changed():
    client = _FakeClient()
    unit = ServiceUnit(client, "agent", cmd="/bin/true")

    assert unit.apply() is True
    assert "daemon-reload" in [call[0] for call in client.systemctl_calls()]

    client.calls.clear()
    assert unit.apply() is False  # identical content
    assert "daemon-reload" not in [call[0] for call in client.systemctl_calls()]


def test_uninstall_reports_whether_it_existed():
    client = _FakeClient()
    unit = ServiceUnit(client, "agent", cmd="/bin/true")
    assert unit.uninstall() is False  # nothing written yet

    unit.apply()
    client.calls.clear()
    assert unit.uninstall() is True
    actions = [call[0] for call in client.systemctl_calls()]
    assert "disable" in actions and "daemon-reload" in actions


# -- mount units ----------------------------------------------------------


def test_mount_unit_name_comes_from_systemd_escape():
    client = _FakeClient(escape="mnt-data")
    unit = MountUnit(client, "/mnt/data", what="//srv/share", type="cifs")
    assert unit.name == "mnt-data.mount"
    assert ["systemd-escape", "--path", "/mnt/data"] in client.calls
    text = unit.render()
    assert "Where = /mnt/data" in text and "What = //srv/share" in text


def test_automount_unit_carries_its_timeout():
    unit = AutomountUnit(_FakeClient(escape="mnt-data"), "/mnt/data", timeout="30")
    assert unit.name == "mnt-data.automount"
    assert "TimeoutIdleSec = 30" in unit.render()


def test_optional_mount_fields_are_omitted_when_empty():
    """An empty `Options =` is not the same as no Options at all."""
    text = MountUnit(_FakeClient(), "/mnt/d", what="/dev/sda1").render()
    assert "Options" not in text and "Type" not in text
