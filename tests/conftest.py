"""Shared test configuration.

``@pytest.mark.requires("asyncssh")`` skips a test when an OPTIONAL extra's
module is not installed, naming it in the skip reason -- so running the suite
without an extra reports skips instead of failures, and a test that needs no
extra is never skipped along with its neighbours (a module-level
``importorskip`` in the middle of a file skips everything after it).

No test reads the developer's own ``~/.ssh``: an SSH leg reads the user's
``~/.ssh/config`` (and ``known_hosts``) by default, so every test runs with
``HOME`` and ``USERPROFILE`` pointing at an empty directory. ``fake_home``
returns that directory for a test that writes a config there.
"""

import importlib.util

import pytest


@pytest.fixture(autouse=True)
def fake_home(tmp_path_factory, monkeypatch):
    """An empty home directory, with ``.ssh/``, where ``~`` resolves.

    The CLI's config file lives under it too, and ``$PYTRUENAS_CONFIG``,
    ``$PYTRUENAS_CREDENTIALS`` and ``$PYTRUENAS_CALL_TIMEOUT`` are unset
    (set-then-deleted, so a test that sets one is undone as well): the
    developer's own configuration must not reach a test.
    """
    home = tmp_path_factory.mktemp("home")
    (home / ".ssh").mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.setenv("APPDATA", str(home / "AppData"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home / ".config"))
    for name in ("CONFIG", "CREDENTIALS", "CALL_TIMEOUT"):
        monkeypatch.setenv(f"PYTRUENAS_{name}", "")
        monkeypatch.delenv(f"PYTRUENAS_{name}")
    return home


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
