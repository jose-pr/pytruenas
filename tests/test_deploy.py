"""``deploy``: CLI wiring and the policy around ``hostctl.deploy``.

The bundler and installer are hostctl's and tested there; these tests pin
what pytruenas decides: what is deployed, where, under which name, and what
runs afterwards.
"""

import logging
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from hostctl.exceptions import BundleError

import pytruenas.cli.commands.deploy as deploy_cmd
import pytruenas.cli._app as main


def _logger():
    logger = logging.getLogger("test-deploy")
    logger.addHandler(logging.NullHandler())
    return logger


def _parse(argv):
    captured = {}

    def fake_dispatch(command, instance):
        captured["args"] = instance
        captured["targets"] = instance._expanded_targets_()
        return 0

    with patch.object(main, "_dispatch", fake_dispatch):
        main.main(argv)
    return captured


# -- CLI parsing --------------------------------------------------------


def test_source_defaults_to_installed():
    c = _parse(["deploy", "nas1"])
    assert c["args"].source == "installed"


def test_source_repo_is_accepted():
    c = _parse(["deploy", "--source", "repo", "nas1"])
    assert c["args"].source == "repo"


def test_repo_root_defaults_to_current_directory():
    c = _parse(["deploy", "nas1"])
    assert c["args"].repo_root == "."


def test_include_exclude_ignore_flags_are_repeatable():
    c = _parse(
        [
            "deploy",
            "--include",
            "requests",
            "--include",
            "[ssh]",
            "--exclude",
            "click",
            "--ignore-file",
            ".gitignore",
            "--ignore-pattern",
            "*.log",
            "--pythonpath",
            "src",
            "nas1",
        ]
    )
    args = c["args"]
    assert args.include == ["requests", "[ssh]"]
    assert args.exclude == ["click"]
    assert args.ignore_files == [".gitignore"]
    assert args.ignore_pattern == ["*.log"]
    assert args.pythonpath == ["src"]


def test_targets_still_trail_after_the_new_flags():
    """The new flags must not swallow the trailing TARGET positional --
    see AGENTS.md's note on greedy list options and register_targets."""
    c = _parse(["deploy", "--source", "repo", "nas1", "nas2"])
    assert c["targets"] == ["nas1", "nas2"]


def test_mode_choices_are_unchanged():
    """--mode still only accepts pyz/dir -- 'repo' belongs to --source, not
    --mode; see the CLI-wiring design note in the module docstring."""
    with pytest.raises(SystemExit):
        _parse(["deploy", "--mode", "repo", "nas1"])


# -- the policy around hostctl.deploy --------------------------------------
#
# Bundling, probing, the digest marker, the atomic swap and the refusal of a
# foreign path are hostctl's (`hostctl.deploy`, tested there). What pytruenas
# decides is what to deploy, where, under which name, and what runs after.


class _Recorder:
    """Stands in for `hostctl.deploy.deploy` and records the call."""

    def __init__(self, written=True):
        self.calls = []
        self.written = written

    def __call__(self, host, source, path, **options):
        from hostctl.deploy import Deployment

        self.calls.append((host, source, path, options))
        mode = options["mode"]
        command = (
            (options["python"], path)
            if mode == "pyz"
            else (f"{path}/bin/{options['package']}",)
        )
        return Deployment(path, "0" * 64, self.written, command)


class _Client:
    def __init__(self, returncode=0):
        self.ran = []
        self.returncode = returncode

    def run(self, command, **options):
        self.ran.append((command, options))
        return SimpleNamespace(returncode=self.returncode)


@pytest.fixture
def recorder(monkeypatch):
    import hostctl.deploy

    recorded = _Recorder()
    monkeypatch.setattr(hostctl.deploy, "deploy", recorded)
    monkeypatch.delenv("PYTRUENAS_PKG_ROOT", raising=False)
    monkeypatch.delenv("PYTRUENAS_PKG_NAME", raising=False)
    return recorded


def _args(**overrides):
    args = deploy_cmd.Args()
    for name, value in overrides.items():
        setattr(args, name, value)
    return args


def test_the_call_binds_to_hostctl_s_deploy_signature():
    import inspect

    from hostctl.deploy import deploy

    inspect.signature(deploy).bind(
        object(),
        "pytruenas",
        "/x.pyz",
        mode="pyz",
        package="pytruenas",
        extras=(),
        skip=(),
        force=False,
        python="python3",
    )


def test_installed_pyz_deploys_pytruenas_to_the_persistent_dataset(recorder):
    client = _Client()
    assert deploy_cmd.run(client, _args(), _logger()) == 0
    [(host, source, path, options)] = recorder.calls
    assert host is client and source == "pytruenas"
    assert path == "/var/db/system/pytruenas.pyz"
    assert options == {
        "mode": "pyz",
        "package": "pytruenas",
        "extras": (),
        "skip": (),
        "force": False,
        "python": "python3",
    }
    assert client.ran == []  # nothing runs without `--`


@pytest.mark.parametrize(
    "given, mode, expected",
    [
        ("/opt/tool", "pyz", "/opt/tool.pyz"),
        ("/opt/tool.pyz", "pyz", "/opt/tool.pyz"),
        ("/opt/tool/", "pyz", "/opt/tool.pyz"),
        ("/opt/tool/", "dir", "/opt/tool"),
        ("/opt/tool.pyz", "dir", "/opt/tool.pyz"),
    ],
)
def test_a_zipapp_is_named_as_a_pyz_file(recorder, given, mode, expected):
    deploy_cmd.run(_Client(), _args(path=given, mode=mode), _logger())
    assert recorder.calls[0][2] == expected


def test_the_root_and_package_come_from_the_arguments_then_the_environment(
    recorder, monkeypatch
):
    monkeypatch.setenv("PYTRUENAS_PKG_ROOT", "tnas-config")
    deploy_cmd.run(_Client(), _args(extras=["ssh"], skip=["jinja2"]), _logger())
    _, source, _, options = recorder.calls[-1]
    assert (source, options["package"]) == ("tnas-config", "tnas_config")
    assert (options["extras"], options["skip"]) == (("ssh",), ("jinja2",))

    monkeypatch.setenv("PYTRUENAS_PKG_NAME", "tnasconfig")
    deploy_cmd.run(_Client(), _args(), _logger())
    assert recorder.calls[-1][3]["package"] == "tnasconfig"

    deploy_cmd.run(_Client(), _args(pkg_root="mine", pkg_name="mine_pkg"), _logger())
    assert recorder.calls[-1][1] == "mine"
    assert recorder.calls[-1][3]["package"] == "mine_pkg"


def test_force_reaches_hostctl(recorder):
    deploy_cmd.run(_Client(), _args(force=True), _logger())
    assert recorder.calls[0][3]["force"] is True


def test_arguments_after_the_separator_run_the_deployed_program(recorder):
    from hostctl import Exec

    client = _Client(returncode=3)
    args = _args(mode="dir")
    args._passthrough_ = ["call", "system.info"]
    assert deploy_cmd.run(client, args, _logger()) == 3
    [(command, options)] = client.ran
    assert isinstance(command, Exec)
    assert options == {"check": False}
    assert (command.program, command.args) == (
        "/var/db/system/pytruenas/bin/pytruenas",
        ("call", "system.info"),
    )


def test_the_logged_command_carries_no_password(recorder, caplog):
    client = _Client()
    args = _args(mode="dir")
    args._passthrough_ = ["query", "user", "wss://root:hunter2@other", "root:pw2@nas"]
    with caplog.at_level(logging.INFO, logger="test-deploy"):
        deploy_cmd.run(client, args, _logger())
    assert "Running:" in caplog.text
    assert "hunter2" not in caplog.text and "pw2" not in caplog.text
    assert "wss://root@other" in caplog.text
    # What runs is still the command as given.
    [(command, _)] = client.ran
    assert command.args[-2:] == ("wss://root:hunter2@other", "root:pw2@nas")


@pytest.mark.requires("pathspec")
def test_source_repo_ships_a_source_tree_with_its_filters(recorder, tmp_path, caplog):
    from hostctl.deploy import SourceTree

    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "pkg"\ndependencies = ["requests", "click"]\n'
    )
    args = _args(
        source="repo",
        mode="dir",
        repo_root=str(tmp_path),
        pkg_root="pkg",
        ignore_files=[".gitignore"],
        ignore_pattern=["*.log"],
        pythonpath=["src"],
        exclude=["click"],
    )
    with caplog.at_level(logging.INFO, logger="test-deploy"):
        deploy_cmd.run(_Client(), args, _logger())
    _, source, path, options = recorder.calls[0]
    assert isinstance(source, SourceTree)
    assert source.root == type(source.root)(str(tmp_path))
    assert source.ignore_files == (".gitignore",)
    assert source.ignore_patterns == ("*.log",)
    assert source.pythonpath == ("src",)
    assert (path, options["mode"], options["package"]) == (
        "/var/db/system/pytruenas",
        "dir",
        "pkg",
    )
    declared = [r.getMessage() for r in caplog.records if "declares" in r.getMessage()]
    assert declared and "requests" in declared[0] and "click" not in declared[0]


def test_source_repo_rejects_mode_pyz():
    args = _args(source="repo", mode="pyz")
    with pytest.raises(BundleError, match="does not support --mode pyz"):
        deploy_cmd.run(None, args, _logger())


def test_source_repo_mode_pyz_never_touches_the_client():
    """The rejection must happen before any client interaction -- a caller
    should not need a reachable target to find out the combination is invalid."""
    args = _args(source="repo", mode="pyz")
    sentinel = object()  # anything -- if this is touched, it will AttributeError
    with pytest.raises(BundleError):
        deploy_cmd.run(sentinel, args, _logger())


@pytest.mark.requires("pathspec")
def test_a_real_bundle_of_a_source_tree_has_a_working_launcher(tmp_path):
    """End to end through hostctl's bundler: the launcher reaches `src/`."""
    from hostctl.deploy import SourceTree, bundle

    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "__init__.py").write_text("X = 1\n")
    out = bundle(SourceTree(tmp_path), tmp_path / "out", mode="dir", package="pkg")
    launcher = (out / "bin" / "pkg").read_text()
    assert f"lib/{tmp_path.name}/src" in launcher


@pytest.mark.parametrize(
    "argv, message",
    [
        (["--source", "repo", "--mode", "pyz"], "does not support --mode pyz"),
        (["--path", "relative/dir"], "--path must be absolute"),
    ],
)
def test_arguments_that_cannot_work_are_refused_once_before_any_target(
    argv, message, monkeypatch, capsys
):
    """Both were found inside the fan-out: exit 1, the same error once per
    target, and a client built for each."""
    import pytruenas.host

    built = []
    monkeypatch.setattr(
        pytruenas.host, "TrueNASClient", lambda *a, **k: built.append(a) or object()
    )
    rc = main.main(["deploy", *argv, "nas1", "nas2"])
    assert rc == 2
    assert built == []
    err = capsys.readouterr().err
    assert err.count(message) == 1
