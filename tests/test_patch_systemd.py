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
        if self._path not in self._store:
            raise FileNotFoundError(self._path)
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


def test_as_names_treats_a_bare_string_as_one_name():
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
    assert ["systemd-escape", "--path", "--", "/mnt/data"] in client.calls
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


def test_units_built_from_one_conf_do_not_share_settings():
    """Each unit gets its own ExecStart and Description; the caller's dict is
    left as it was passed."""
    base = {"Service": {"Environment": "A=1"}}
    client = _FakeClient()
    alpha = ServiceUnit(client, "alpha", cmd="/usr/bin/alpha", conf=base)
    beta = ServiceUnit(client, "beta", cmd="/usr/bin/beta", conf=base)

    assert base == {"Service": {"Environment": "A=1"}}
    assert alpha.conf["Service"]["ExecStart"] == "/usr/bin/alpha"
    assert beta.conf["Service"]["ExecStart"] == "/usr/bin/beta"
    assert beta.conf["Unit"]["Description"] == "BETA"
    assert beta.conf["Service"]["Environment"] == "A=1"


def test_a_failed_daemon_reload_leaves_the_unit_to_be_written_again():
    """Otherwise the next apply finds the file written and never reloads."""
    import pytest

    class _ReloadFails(_FakeClient):
        fail = True

        def run(self, argv, check=True, **kwargs):
            if argv[:2] == ["systemctl", "daemon-reload"] and self.fail:
                self.calls.append(list(argv))
                raise RuntimeError("daemon-reload failed")
            return super().run(argv, check=check, **kwargs)

    client = _ReloadFails()
    unit = ServiceUnit(client, "agent", cmd="/bin/true")
    with pytest.raises(RuntimeError):
        unit.apply()
    assert not unit.path.exists()

    client.fail = False
    client.calls.clear()
    assert unit.apply() is True
    assert ["daemon-reload"] in client.systemctl_calls()


# -- names systemd reads as intended -------------------------------------------


def test_a_dotted_name_still_gets_the_type_suffix():
    """systemd ignores a unit file whose name ends in no unit type."""
    client = _FakeClient()
    assert ServiceUnit(client, "my.agent").name == "my.agent.service"
    assert Unit(client, "agent.v2.timer").name == "agent.v2.timer"


def test_the_root_mount_unit_is_dash_mount():
    """`systemd-escape --path /` prints `-`, and `-.mount` is the unit for /."""
    client = _FakeClient(escape="-")
    assert MountUnit(client, "/", what="tank/root").name == "-.mount"
    assert ["systemd-escape", "--path", "--", "/"] in client.calls


def test_escape_ends_option_parsing_before_the_text():
    client = _FakeClient()
    Unit(client, "agent").escape("-x")
    assert client.calls[-1] == ["systemd-escape", "--", "-x"]


# -- unit-file text --------------------------------------------------------


def test_a_list_value_renders_as_repeated_keys():
    from pytruenas.patch.systemd import render_unit

    text = render_unit({"Service": {"ExecStartPre": ["/a", "/b"], "Type": "simple"}})
    assert text == "[Service]\nExecStartPre = /a\nExecStartPre = /b\nType = simple\n\n"


def test_a_value_spanning_lines_is_refused():
    import pytest

    from pytruenas.patch.systemd import render_unit

    with pytest.raises(ValueError, match="span lines"):
        render_unit({"Service": {"ExecStart": "/bin/a\n/bin/b"}})


def test_render_matches_configparser_for_single_values():
    """Byte-identical output keeps an existing unit unchanged on re-apply."""
    from pytruenas.patch.systemd import render_unit

    conf = {
        "Unit": {"Description": "Agent %i", "After": "network.target"},
        "Service": {"ExecStart": "/bin/a --x=1", "RestartSec": 10, "Empty": ""},
        "Install": {"WantedBy": "multi-user.target"},
    }
    parser = UnitConfigParser()
    parser.read_dict(conf)
    expected = io.StringIO()
    parser.write(expected)
    assert render_unit(conf) == expected.getvalue()


def test_parse_reads_repeated_keys_sections_and_continuations():
    from pytruenas.patch.systemd import parse_unit

    text = (
        "# a comment\n"
        "[Service]\n"
        "ExecStartPre=/a\n"
        "ExecStartPre = /b\n"
        "ExecStart=/bin/agent \\\n"
        "  # skipped inside a continuation\n"
        "  --flag\n"
        "[Unit]\n"
        "Description=x\n"
        "[Service]\n"
        "Restart=always\n"
    )
    assert parse_unit(text) == {
        "Service": {
            "ExecStartPre": ["/a", "/b"],
            "ExecStart": "/bin/agent  --flag",
            "Restart": "always",
        },
        "Unit": {"Description": "x"},
    }


def test_parse_round_trips_render():
    from pytruenas.patch.systemd import parse_unit, render_unit

    conf = {"Service": {"Environment": ["A=1", "B=2"], "ExecStart": "/bin/a"}}
    assert parse_unit(render_unit(conf)) == conf


# -- a changed unit reaching a running service ------------------------------


def test_restart_on_change_restarts_a_changed_unit_after_reloading():
    client = _FakeClient(enabled=True, active=True)
    unit = ServiceUnit(client, "agent", cmd="/bin/v1", restart_on_change=True)
    unit.apply()
    assert [call[0] for call in client.systemctl_calls()][:2] == [
        "daemon-reload",
        "try-restart",
    ]

    client.calls.clear()
    unit.apply()  # unchanged: nothing to restart for
    assert "try-restart" not in [call[0] for call in client.systemctl_calls()]


def test_a_changed_unit_is_not_restarted_by_default():
    client = _FakeClient(enabled=True, active=True)
    ServiceUnit(client, "agent", cmd="/bin/v1").apply()
    assert "try-restart" not in [call[0] for call in client.systemctl_calls()]
