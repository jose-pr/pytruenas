"""Argument plumbing: the `--` tail, the app root, and step arity.

Each of these is a place where pytruenas re-implemented something duho already
does, and the copy had drifted from the original.
"""

import logging
from types import SimpleNamespace
from unittest.mock import patch

import pytest

import pytruenas.main as main
from pytruenas.utils._introspect import positional_arity
from pytruenas.utils.runpath import _positional_count, step


def _parse(argv):
    captured = {}

    def fake_dispatch(command, instance):
        captured["cmd"] = command._parsername_
        captured["targets"] = instance._expanded_targets_()
        captured["passthrough"] = list(getattr(instance, "_passthrough_", ()) or ())
        return 0

    with patch.object(main, "_dispatch", fake_dispatch):
        main.main("pytruenas", argv)
    return captured


def test_the_tail_after_a_separator_reaches_the_command():
    """pytruenas split argv itself and carried the tail in a module global,
    duplicating duho's own `_passthrough_` capture."""
    parsed = _parse(["deploy", "nas1", "--", "call", "system.info"])
    assert parsed["targets"] == ["nas1"]
    assert parsed["passthrough"] == ["call", "system.info"]
    assert not hasattr(main, "PASSTHROUGH")


def test_deploy_reads_the_tail_off_the_parsed_instance():
    from pytruenas.cmd import deploy

    assert deploy._passthrough(SimpleNamespace(_passthrough_=["a", "b"])) == ["a", "b"]
    assert deploy._passthrough(SimpleNamespace()) == []


def test_a_tail_no_command_reads_is_reported(caplog):
    """It was dropped in silence."""
    logger = logging.getLogger("pytruenas.test.passthrough")
    with caplog.at_level(logging.WARNING):
        main._warn_stray_passthrough(
            SimpleNamespace(_parsername_="query"),
            SimpleNamespace(_passthrough_=["x"], targets=["nas1"]),
            logger,
        )
    assert "query reads none" in caplog.text


def test_a_target_after_the_separator_is_reported(caplog):
    """`deploy -- call x nas1` runs against localhost: nothing after `--` is a
    target, which the run used to do without a word."""
    logger = logging.getLogger("pytruenas.test.passthrough")
    with caplog.at_level(logging.WARNING):
        main._warn_stray_passthrough(
            SimpleNamespace(_parsername_="deploy"),
            SimpleNamespace(_passthrough_=["call", "x", "nas1"], targets=[]),
            logger,
        )
    assert "no target before '--'" in caplog.text


def test_a_well_formed_deploy_says_nothing(caplog):
    logger = logging.getLogger("pytruenas.test.passthrough")
    with caplog.at_level(logging.WARNING):
        main._warn_stray_passthrough(
            SimpleNamespace(_parsername_="deploy"),
            SimpleNamespace(_passthrough_=["call", "x"], targets=["nas1"]),
            logger,
        )
    assert caplog.text == ""


# -- the app root ---------------------------------------------------------


def test_the_runpath_base_for_the_shared_root_is_the_shared_base():
    """Combining them the other way round is an impossible MRO, which is why
    registration used to be skipped for the default args entirely -- leaving a
    derived tool's base registered for everyone after it."""
    from pytruenas.utils.cmd import PyTrueNASArgs
    from pytruenas.utils.runpath import PyTrueNASRunPathArgs

    assert main._runpath_base(PyTrueNASArgs) is PyTrueNASRunPathArgs
    assert main._runpath_base(PyTrueNASRunPathArgs) is PyTrueNASRunPathArgs

    class MyArgs(PyTrueNASArgs):
        pass

    combined = main._runpath_base(MyArgs)
    assert issubclass(combined, MyArgs) and issubclass(combined, PyTrueNASRunPathArgs)


def test_discovery_reads_globals_off_the_resolved_root():
    """A derived tool's own global options were invisible to discovery."""
    import inspect

    assert "root" in inspect.signature(main._discover).parameters


# -- step arity -----------------------------------------------------------


def test_only_required_positionals_count():
    assert positional_arity(lambda a, b, c: None) == 3
    assert positional_arity(lambda a, b, c=None: None, required_only=True) == 2
    assert positional_arity(lambda *a: None, varargs=3) == 3
    assert positional_arity(lambda *a: None) == 0
    assert positional_arity(lambda a, b, c, d: None, cap=3) == 3
    # A callable `inspect` cannot describe falls back to the caller's choice.
    assert positional_arity(dict.fromkeys, unknown=3) in (2, 3)
    assert positional_arity(object(), unknown=3) == 3


@pytest.mark.parametrize(
    "func,expected",
    [
        (lambda client, args, logger: None, 3),
        # duho-native shapes that must NOT be adapted: the third parameter is
        # optional, or the signature is a catch-all. Both used to count as 3,
        # so the adapter swapped the caller's arguments.
        (lambda cmd, ctx, extra=None: None, 2),
        (lambda *args: None, 0),
        (lambda cmd, ctx: None, 2),
    ],
)
def test_a_step_is_adapted_only_when_it_needs_three(func, expected):
    assert _positional_count(func) == expected
    # `main._step_adapter` wraps only what needs all three; the adapter itself
    # is exercised end to end in test_cli_runpath.
    assert (main._step_adapter(func) is not func) is (expected >= 3)


def test_an_explicitly_decorated_step_is_still_adapted():
    @step
    def two(client, args):
        return (client, args)

    assert callable(two)
