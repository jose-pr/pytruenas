"""CLI paths that were broken for every invocation, not just edge cases."""

import logging
import subprocess
import sys
from pathlib import Path

import pytest

import pytruenas.main as main
from pytruenas.utils.cmd import PyTrueNASArgs, json_value


def _cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "pytruenas", *args], capture_output=True, text=True
    )


def test_the_config_option_parses(tmp_path):
    """`--config` was typed `dict`, so duho gave it its KEY=VALUE action and
    argparse died on every use ("'WindowsPath' object is not iterable")."""
    cfg = tmp_path / "pytruenas.yaml"
    cfg.write_text("commandspath: []\n")
    r = _cli("-c", str(cfg), "call", "core.ping", "127.0.0.1")
    assert "not iterable" not in r.stderr
    # It got as far as connecting (there is no middleware here to answer).
    assert "usage:" not in r.stderr
    assert PyTrueNASArgs.config.__class__ is not dict


def test_a_failed_command_exits_non_zero():
    """`python -m pytruenas` discarded main()'s return value, so every failure
    exited 0 and no shell or CI step could see it."""
    r = _cli("call", "nope", "127.0.0.1")
    assert r.returncode != 0


def test_importing_main_does_not_configure_logging(monkeypatch):
    """init_stderr_logging() ran at import; importing the module (a test, a
    wrapper) must not reconfigure the importer's logging."""
    called = []
    monkeypatch.setattr(
        "duho.logging.init_stderr_logging", lambda *a, **k: called.append(1)
    )
    import importlib

    import pytruenas.__main__ as entry

    importlib.reload(entry)
    assert called == []


@pytest.mark.parametrize(
    "raw,expected",
    [("0", 0), ("true", True), ("null", None), ("root", "root"), ("1.5", 1.5)],
)
def test_filter_values_are_typed(raw, expected):
    """`query -f uid=0` compared the string "0" against 0 and matched nothing."""
    assert json_value(raw) == expected


def test_query_builds_typed_filters(capsys):
    from pytruenas.cmd import query as query_cmd

    class _Api(dict):
        def __getitem__(self, name):
            return self

        def _query(self, **filters):
            captured.update(filters)
            return []

    captured = {}
    client = type("C", (), {"api": _Api()})()
    args = query_cmd.Args()
    args.namespace = "user"
    args.query = ["uid=0", "locked=false", "username=root"]
    assert query_cmd.run(client, args, logging.getLogger("t")) in (None, 0)
    assert captured == {"uid": 0, "locked": False, "username": "root"}


def test_a_malformed_filter_is_an_error(capsys):
    from pytruenas.cmd import query as query_cmd

    args = query_cmd.Args()
    args.namespace = "user"
    args.query = ["username"]  # no "="
    assert query_cmd.run(None, args, logging.getLogger("t")) == 2


def test_logto_names_are_legal_filenames(tmp_path):
    """{target} for a non-default port and {isodate} both carry colons, which
    Windows refuses -- so --logto failed there for exactly those targets."""
    rendered = main._logto_path(str(tmp_path / "{target}-{isodate}.log"), "nas:8443")
    name = Path(rendered).name
    assert ":" not in name and "nas_8443" in name
    # It must be creatable, which is the whole point.
    Path(rendered).write_text("x")
    # The template's own separators are the caller's and must survive.
    assert str(tmp_path) in rendered


def test_the_success_hook_is_skipped_for_a_failed_run():
    """It ran regardless of the exit code, so a "succeeded" notification fired
    for a command that had just failed."""
    from types import SimpleNamespace

    calls = []
    module = SimpleNamespace(
        __doc__="fake",
        run=lambda client, args, logger: 2,
        init=lambda args, logger: object(),
        success=lambda client, args, logger: calls.append("success"),
        finally_=lambda client, args, logger: calls.append("finally"),
    )
    args = PyTrueNASArgs()
    args.logto = "-"
    rc = main._run_module_on_target(
        SimpleNamespace(module=module), args, "nas", logging.getLogger("t")
    )
    assert rc == 2 and calls == ["finally"]
