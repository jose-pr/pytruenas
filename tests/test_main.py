"""CLI driver: the fan-out dispatch runs the command once per target."""

import logging
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytruenas.main as main
from duho.discovery import ModuleCommand


def _cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "pytruenas", *args],
        capture_output=True, text=True,
    )


def test_cli_version_prints_metadata_version():
    # __main__ + main() + duho parser build, end to end; _version_ = AUTO
    # resolves the installed 0.1.0 from importlib.metadata.
    r = _cli("--version")
    assert r.returncode == 0
    assert "0.1.0" in r.stdout


def test_cli_help_lists_subcommands():
    r = _cli("--help")
    assert r.returncode == 0
    for sub in ("dump-api", "generate-typings", "query"):
        assert sub in r.stdout


def test_main_version_in_process(monkeypatch, capsys):
    # In-process so main.py's entry path is measured for coverage. --version
    # exits via SystemExit(0) after argparse prints the metadata version.
    import pytest

    monkeypatch.setattr(sys, "argv", ["pytruenas", "--version"])
    with pytest.raises(SystemExit) as ei:
        main.main("pytruenas")
    assert ei.value.code in (0, None)
    assert "0.1.0" in capsys.readouterr().out


def test_main_help_in_process(monkeypatch, capsys):
    import pytest

    monkeypatch.setattr(sys, "argv", ["pytruenas", "--help"])
    with pytest.raises(SystemExit) as ei:
        main.main("pytruenas")
    assert ei.value.code in (0, None)
    assert "usage:" in capsys.readouterr().out


def _module_command(run):
    mod = SimpleNamespace(__doc__="fake", run=run, init=None, success=None, finally_=None)
    return ModuleCommand(mod, name="fake", entrypoint=run)


def _instance(targets, parallel=2):
    return SimpleNamespace(
        _logger_=logging.getLogger("pytruenas.test"),
        parallel=parallel,
        sslverify=False,
        logto="-",
        _expanded_targets_=lambda: targets,
    )


def test_dispatch_runs_command_per_target(monkeypatch):
    seen = []
    monkeypatch.setattr(main, "TrueNASClient", lambda *a, **k: MagicMock())
    command = _module_command(lambda client, args, logger: seen.append(1) or 0)

    rc = main._dispatch(command, _instance(["h1", "h2", "h3"]))

    assert rc == 0
    assert len(seen) == 3  # one run per target


def test_dispatch_aggregates_worst_exit_code(monkeypatch):
    monkeypatch.setattr(main, "TrueNASClient", lambda *a, **k: MagicMock())
    # A target returning a nonzero code surfaces in the aggregate (max policy).
    command = _module_command(lambda client, args, logger: 2)
    rc = main._dispatch(command, _instance(["h1", "h2", "h3"]))
    assert rc == 2


def test_dispatch_isolates_target_failure(monkeypatch):
    monkeypatch.setattr(main, "TrueNASClient", lambda *a, **k: MagicMock())
    ran = []

    def run(client, args, logger):
        ran.append(1)
        raise RuntimeError("boom")

    command = _module_command(run)
    rc = main._dispatch(command, _instance(["h1", "h2"]))

    # both targets attempted despite the exception; nonzero aggregate.
    assert len(ran) == 2
    assert rc != 0
