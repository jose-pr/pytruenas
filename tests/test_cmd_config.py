"""The CLI's config file (utils/cmd.py): format, location, and target expansion."""

import pytest
from duho import UsageError

from pytruenas.utils import cmd as _cmd
from pytruenas.utils.cmd import PyTrueNASArgs


@pytest.fixture(autouse=True)
def _no_config_env(monkeypatch, tmp_path):
    monkeypatch.delenv("PYTRUENAS_CONFIG", raising=False)
    # The default location, isolated from the real one.
    monkeypatch.setenv("APPDATA", str(tmp_path / "appdata"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))


@pytest.mark.parametrize(
    "name, text",
    [
        ("pytruenas.cfg", 'credentials = "root:pw"\ncommandspath = ["cmds"]\n'),
        ("settings", 'credentials = "root:pw"\ncommandspath = ["cmds"]\n'),
        ("pytruenas.toml", 'credentials = "root:pw"\ncommandspath = ["cmds"]\n'),
        ("pytruenas.json", '{"credentials": "root:pw", "commandspath": ["cmds"]}'),
        (
            "pytruenas.cfg",
            '#!json\n{"credentials": "root:pw", "commandspath": ["cmds"]}',
        ),
    ],
)
def test_a_cfg_is_toml_unless_its_first_line_or_suffix_says_otherwise(
    tmp_path, name, text
):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    assert _cmd.load_config(path) == {
        "credentials": "root:pw",
        "commandspath": ["cmds"],
    }


@pytest.mark.parametrize("first_line", ["#!yaml", "#!/usr/bin/env yaml"])
def test_a_shebang_names_yaml(tmp_path, first_line):
    pytest.importorskip("yaml")
    path = tmp_path / "pytruenas.cfg"
    path.write_text(f"{first_line}\ncredentials: root:pw\n", encoding="utf-8")
    assert _cmd.load_config(path) == {"credentials": "root:pw"}


def test_a_yaml_suffix_is_yaml(tmp_path):
    pytest.importorskip("yaml")
    path = tmp_path / "pytruenas.yaml"
    path.write_text("credentials: root:pw\n", encoding="utf-8")
    assert _cmd.load_config(path) == {"credentials": "root:pw"}


def test_an_empty_file_has_no_settings(tmp_path):
    path = tmp_path / "pytruenas.cfg"
    path.write_bytes(b"")
    assert _cmd.load_config(path) == {}


@pytest.mark.parametrize(
    "text, message",
    [
        ("credentials = [\n", "line"),  # TOML that does not parse
        ("#!json\n[1, 2]\n", "expected a table"),
        ("#!ini\n[pytruenas]\nx = 1\n", "not supported"),
        ("#!nosuchformat\nx = 1\n", "nosuchformat"),
    ],
)
def test_a_file_that_is_not_settings_is_a_usage_error(tmp_path, text, message):
    path = tmp_path / "pytruenas.cfg"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(UsageError, match=message) as raised:
        _cmd.load_config(path)
    assert str(path) in str(raised.value)


def test_the_default_location_is_the_users_config_directory(monkeypatch, tmp_path):
    expected = _cmd.default_config_path()
    assert expected.parts[-2:] == ("pytruenas", "pytruenas.cfg")
    assert str(tmp_path) in str(expected)


def test_a_missing_default_file_has_no_settings():
    assert PyTrueNASArgs()._config_dict_() == {}


def test_the_default_file_is_read_when_present():
    path = _cmd.default_config_path()
    path.parent.mkdir(parents=True)
    path.write_text('credentials = "root:pw"\n', encoding="utf-8")
    assert PyTrueNASArgs()._config_dict_() == {"credentials": "root:pw"}


def test_the_working_directory_is_never_searched(monkeypatch, tmp_path):
    """`./pytruenas.yaml` was read from wherever the CLI ran."""
    pytest.importorskip("yaml")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pytruenas.yaml").write_text("credentials: stray\n")
    (tmp_path / "pytruenas.cfg").write_text('credentials = "stray"\n')
    assert PyTrueNASArgs()._config_dict_() == {}


def test_the_variable_is_read_when_the_file_is_needed(monkeypatch, tmp_path):
    """It was read when `pytruenas.utils.cmd` was imported."""
    path = tmp_path / "named.cfg"
    path.write_text('credentials = "named"\n', encoding="utf-8")
    monkeypatch.setenv("PYTRUENAS_CONFIG", str(path))
    assert PyTrueNASArgs()._config_dict_() == {"credentials": "named"}


@pytest.mark.parametrize("via", ["option", "variable"])
def test_a_named_file_must_exist(monkeypatch, tmp_path, via):
    args = PyTrueNASArgs()
    if via == "option":
        args.config = tmp_path / "typo.cfg"
    else:
        monkeypatch.setenv("PYTRUENAS_CONFIG", str(tmp_path / "typo.cfg"))
    with pytest.raises(UsageError, match="config file not found"):
        args._config_dict_()


def test_config_dict_from_mapping():
    args = PyTrueNASArgs()
    args.config = {"already": "loaded"}
    assert args._config_dict_() == {"already": "loaded"}


def test_expanded_targets_default_localhost():
    args = PyTrueNASArgs()
    args.targets = []
    assert args._expanded_targets_() == ["localhost"]


def test_expanded_targets_comma_and_range():
    args = PyTrueNASArgs()
    args.targets = ["nas1,nas2", "web[1-2]"]
    assert args._expanded_targets_() == ["nas1", "nas2", "web1", "web2"]
