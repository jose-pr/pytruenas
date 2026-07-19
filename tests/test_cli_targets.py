"""Targets are the trailing positional arguments of a command (no -t/--target).

`pytruenas <command> [command-positionals...] [TARGET ...]` — a command's own
positionals come first, targets fill the rest; empty defaults to localhost.
"""

from unittest.mock import patch

import pytruenas.main as main


def _parse(argv):
    """Run main() up to dispatch; return the parsed instance's captured state."""
    captured = {}

    def fake_dispatch(command, instance):
        captured["cmd"] = command._parsername_
        captured["targets"] = instance._expanded_targets_()
        captured["namespace"] = getattr(instance, "namespace", None)
        return 0

    with patch.object(main, "_dispatch", fake_dispatch):
        rc = main.main("pytruenas", argv)
    captured["rc"] = rc
    return captured


def test_query_namespace_then_targets():
    c = _parse(["query", "user", "nas1", "nas2"])
    assert c["cmd"] == "query"
    assert c["namespace"] == "user"
    assert c["targets"] == ["nas1", "nas2"]


def test_query_without_targets_defaults_localhost():
    c = _parse(["query", "user"])
    assert c["namespace"] == "user"
    assert c["targets"] == ["localhost"]


def test_dump_api_targets_are_only_positionals():
    c = _parse(["dump-api", "nas1", "nas2"])
    assert c["cmd"] == "dump-api"
    assert c["targets"] == ["nas1", "nas2"]


def test_targets_comma_and_range_expansion():
    c = _parse(["dump-api", "nas1,nas2", "web[1-2]"])
    assert c["targets"] == ["nas1", "nas2", "web1", "web2"]


def test_no_dash_t_flag():
    # -t must no longer be accepted (targets are positional now).
    import contextlib
    import io

    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            _parse(["query", "user", "-t", "nas1"])
        except SystemExit:
            pass
    # argparse rejects the unknown -t optional
    assert "-t" in err.getvalue() or "unrecognized" in err.getvalue().lower()
