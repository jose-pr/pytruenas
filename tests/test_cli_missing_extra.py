"""A command that needs a missing optional extra fails its target in one line.

hostctl raises ``MissingExtraError`` (an ``ImportError``) wherever it names an
extra that is not installed, and its own command line exits 125 with the
message. A pytruenas target does the same; any other exception keeps its
traceback.
"""

import logging
from types import SimpleNamespace

import pytest
from hostctl.exceptions import MissingExtraError

import pytruenas.main as main


class _Client:
    closed = False

    def close(self):
        self.closed = True


def _command(error):
    def run(client, args, logger):
        raise error

    module = SimpleNamespace(run=run, init=lambda args, logger: _Client())
    return SimpleNamespace(module=module)


def test_a_missing_extra_is_one_error_line_and_status_125(caplog):
    error = MissingExtraError("deploy", "deploy()")
    with caplog.at_level(logging.ERROR, logger="test-extra"):
        status = main._run_module_on_target(
            _command(error),
            SimpleNamespace(logto=None),
            "nas",
            logging.getLogger("test-extra"),
        )
    assert status == 125
    [record] = [r for r in caplog.records if r.levelno == logging.ERROR]
    assert record.getMessage() == str(error)
    assert 'pip install "hostctl[deploy]"' in record.getMessage()
    assert record.exc_info is None


def test_a_plain_import_error_is_not_mapped():
    with pytest.raises(ImportError, match="inside a dependency"):
        main._run_module_on_target(
            _command(ImportError("inside a dependency")),
            SimpleNamespace(logto=None),
            "nas",
            logging.getLogger("test-extra"),
        )


# -- pytruenas's own extras --------------------------------------------------


def test_a_config_file_without_pyyaml_names_pytruenas_config(tmp_path, monkeypatch):
    import sys

    from pytruenas.utils import cmd

    monkeypatch.setitem(sys.modules, "yaml", None)
    cfg = tmp_path / "pytruenas.yaml"
    cfg.write_bytes(b"credentials: x\n")
    with pytest.raises(MissingExtraError) as caught:
        cmd._load_config(cfg)
    assert caught.value.distribution == "pytruenas"
    assert 'pip install "pytruenas[config]"' in str(caught.value)
    assert str(cfg) in str(caught.value)


def test_the_cli_reports_a_missing_config_extra_in_one_line(
    tmp_path, monkeypatch, capsys
):
    """The config file is read before any target runs, so `main()` itself
    maps the error: one line on stderr and the status a target gets."""
    import sys

    monkeypatch.setitem(sys.modules, "yaml", None)
    cfg = tmp_path / "pytruenas.yaml"
    cfg.write_bytes(b"credentials: x\n")
    status = main.main(argv=["--config", str(cfg), "call", "system.info", "nas"])
    assert status == 125
    err = capsys.readouterr().err
    assert err.splitlines() == [
        f"pytruenas: reading the config file {cfg} needs the 'config' extra: "
        'pip install "pytruenas[config]"'
    ]


def test_deriving_a_public_key_without_asyncssh_names_pytruenas_ssh(monkeypatch):
    import sys

    from pytruenas import host

    monkeypatch.setitem(sys.modules, "asyncssh", None)
    with pytest.raises(MissingExtraError) as caught:
        host._asyncssh()
    assert caught.value.extra == "ssh"
    assert 'pip install "pytruenas[ssh]"' in str(caught.value)
