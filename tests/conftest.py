"""Shared test configuration.

``@pytest.mark.requires("asyncssh")`` skips a test when an OPTIONAL extra's
module is not installed, naming it in the skip reason -- so running the suite
without an extra reports skips instead of failures, and a test that needs no
extra is never skipped along with its neighbours (a module-level
``importorskip`` in the middle of a file skips everything after it).
"""

import importlib.util

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "requires(*modules): skip unless every named (optional-extra) module "
        "is importable",
    )


def pytest_collection_modifyitems(config, items):
    for item in items:
        for marker in item.iter_markers("requires"):
            missing = [m for m in marker.args if importlib.util.find_spec(m) is None]
            if missing:
                item.add_marker(
                    pytest.mark.skip(
                        reason=f"needs {', '.join(missing)} (an optional extra)"
                    )
                )
