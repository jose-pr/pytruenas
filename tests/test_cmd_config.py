"""PyTrueNASArgs config loading + target expansion (utils/cmd.py)."""

from pathlib import Path

import pytest

from pytruenas.utils import cmd as _cmd
from pytruenas.utils.cmd import PyTrueNASArgs


def test_load_config_missing_file_returns_empty(tmp_path):
    assert _cmd._load_config(tmp_path / "nope.yaml") == {}


def test_load_config_reads_yaml(tmp_path):
    pytest.importorskip("yaml")
    p = tmp_path / "cfg.yaml"
    p.write_text("targets: [nas1, nas2]\nparallel: 3\n")
    loaded = _cmd._load_config(p)
    assert loaded == {"targets": ["nas1", "nas2"], "parallel": 3}


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
