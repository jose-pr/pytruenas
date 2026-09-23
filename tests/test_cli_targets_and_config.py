"""Target expansion and config loading: what the CLI reads before it connects.

Both were string handling applied to the wrong span -- expansion over a whole
target including its credentials, and a config file read with whatever encoding
the console happened to have.
"""

import logging

import pytest

import pytruenas.main as main
from pytruenas.utils.cmd import PyTrueNASArgs


def _args(targets=(), **fields):
    args = PyTrueNASArgs()
    args.targets = list(targets)
    for name, value in fields.items():
        setattr(args, name, value)
    return args


@pytest.mark.parametrize(
    "target,expected",
    [
        # What already worked and must keep working.
        ("nas1,nas2", ["nas1", "nas2"]),
        ("web[1-2]", ["web1", "web2"]),
        ("localhost", ["localhost"]),
        # A comma inside the password is part of the password, not a separator:
        # this used to become three targets, two of them nonsense.
        ("wss://root:pw,with,commas@nas", ["wss://root:pw,with,commas@nas"]),
        # Credentials must reach EVERY expanded host; the second target used to
        # lose them entirely and connect unauthenticated.
        ("root:secret@nas1,nas2", ["root:secret@nas1", "root:secret@nas2"]),
        ("wss://root:p1@nas[1-2]", ["wss://root:p1@nas1", "wss://root:p1@nas2"]),
        # A range in the password is not a range either.
        ("wss://root:a[1-2]b@nas", ["wss://root:a[1-2]b@nas"]),
        # An "@" in a path does not make the rest userinfo.
        ("wss://nas/api/v1@x", ["wss://nas/api/v1@x"]),
    ],
)
def test_only_the_host_part_is_expanded(target, expected):
    assert _args([target])._expanded_targets_() == expected


def test_a_config_file_is_read_as_utf8(tmp_path, monkeypatch):
    """`read_text()` used the locale encoding, so a UTF-8 config crashed under
    a cp1252 console."""
    pytest.importorskip("yaml")
    cfg = tmp_path / "pytruenas.yaml"
    cfg.write_bytes("credentials: 'røøt:hünter2'\n".encode("utf-8"))
    args = _args(config=cfg)
    assert args._config_dict_()["credentials"] == "røøt:hünter2"


def test_a_config_that_is_not_a_mapping_is_ignored(tmp_path, caplog):
    pytest.importorskip("yaml")
    cfg = tmp_path / "pytruenas.yaml"
    cfg.write_text("- just\n- a\n- list\n")
    with caplog.at_level(logging.WARNING):
        assert _args(config=cfg)._config_dict_() == {}
    assert "expected a mapping" in caplog.text


def test_a_scalar_commandspath_is_one_source(tmp_path):
    """`list("mycmds")` made it six single-letter sources."""
    (tmp_path / "mycmds").mkdir()
    cfg = tmp_path / "pytruenas.yaml"
    assert main._config_sources("mycmds", cfg) == [str(tmp_path / "mycmds")]
    assert main._config_sources(["a.pkg", "mycmds"], cfg) == [
        "a.pkg",
        str(tmp_path / "mycmds"),
    ]
    assert main._config_sources(None, cfg) == []


def test_a_commandspath_of_the_wrong_type_is_ignored(tmp_path, caplog):
    with caplog.at_level(logging.WARNING):
        assert main._config_sources({"not": "a list"}, tmp_path / "c.yaml") == []
    assert "expected a string or a list" in caplog.text


def test_an_unusable_command_source_is_skipped_not_fatal(caplog):
    """A stray token crashed the whole CLI; duho's own discovery is resilient
    to a bad command, and a bad source should be too."""
    with caplog.at_level(logging.WARNING):
        assert main._commands_from_source("not a module name!") == []
    assert "skipping command source" in caplog.text


def test_an_implicit_config_cannot_inject_command_sources(
    tmp_path, monkeypatch, caplog
):
    """./pytruenas.yaml is whatever directory the CLI runs in; naming command
    sources from there means importing that directory's code."""
    monkeypatch.delenv("PYTRUENAS_CONFIG", raising=False)
    monkeypatch.delenv("PYTRUENAS_CFG", raising=False)
    implicit = _args()
    assert implicit._config_is_implicit_() is True
    explicit = _args(config=tmp_path / "given.yaml")
    assert explicit._config_is_implicit_() is False
    # And naming it through the environment counts as asking for it.
    monkeypatch.setenv("PYTRUENAS_CONFIG", str(tmp_path / "given.yaml"))
    assert _args()._config_is_implicit_() is False
