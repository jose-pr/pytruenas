"""A derived tool can supply its own shared args root.

``main(args=...)`` / ``PyTrueNAS._ARGS_`` set the class every command inherits.
The point of it being a parameter (rather than something a caller wires up) is
that one value has to reach TWO places: the app root, and ``duho.runpath``'s
``base``. A tool whose global flag works on ``pytruenas call`` but vanishes on a
RunPath directory is the bug this guards.

``duho.runpath.register`` mutates PROCESS-GLOBAL state, so every test here
restores it -- otherwise a custom base leaks into every later test in the
session, and the failure surfaces somewhere unrelated.
"""

import duho.runpath as _runpath
import pytest

from pytruenas.main import PyTrueNAS, main
from pytruenas.utils.cmd import PyTrueNASArgs
from pytruenas.utils.runpath import PyTrueNASRunPathArgs


class MyArgs(PyTrueNASArgs):
    """A derived tool's shared root."""

    region: str = "us-east"
    "Which region to operate on"
    ("--region",)  # type: ignore


@pytest.fixture(autouse=True)
def _restore_runpath_base():
    """Undo any register() a test performs (see the module docstring)."""
    saved = _runpath._BASE
    yield
    _runpath._BASE = saved


def _runpath_base():
    """The base a RunPath command would currently be built from."""
    return _runpath._BASE


# -- the default is unchanged ---------------------------------------------


def test_default_args_is_pytruenasargs():
    assert PyTrueNAS._ARGS_ is PyTrueNASArgs


def test_no_args_leaves_the_registered_base_alone():
    """The import-time registration already set this; don't churn it."""
    before = _runpath_base()
    with pytest.raises(SystemExit):
        main("pytruenas", ["--help"])
    assert _runpath_base() is before


# -- args= reaches both places --------------------------------------------


def test_args_subclass_reaches_the_runpath_base():
    with pytest.raises(SystemExit):
        main("mytool", ["--help"], args=MyArgs)
    assert issubclass(_runpath_base(), MyArgs)


def test_runpath_base_keeps_the_trailing_targets_override():
    """Without this a derived tool's RunPath commands lose TARGET entirely.

    `targets` is SUPPRESS-ed on a plain class command; only
    PyTrueNASRunPathArgs._initparser_ adds the positional back.
    """
    with pytest.raises(SystemExit):
        main("mytool", ["--help"], args=MyArgs)
    assert issubclass(_runpath_base(), PyTrueNASRunPathArgs)


def test_args_subclass_adds_its_flag_to_the_parser(capsys):
    with pytest.raises(SystemExit):
        main("mytool", ["--help"], args=MyArgs)
    assert "--region" in capsys.readouterr().out


def test_default_parser_has_no_derived_flag(capsys):
    with pytest.raises(SystemExit):
        main("pytruenas", ["--help"])
    assert "--region" not in capsys.readouterr().out


# -- _ARGS_ on a subclassed root ------------------------------------------


def test_root_subclass_supplies_args_via_dunder(capsys):
    """Setting _ARGS_ once is enough -- no second argument to main()."""

    class MyApp(PyTrueNAS):
        """My derived tool."""

        _ARGS_ = MyArgs

    with pytest.raises(SystemExit):
        main("mytool", ["--help"], root=MyApp)
    assert "--region" in capsys.readouterr().out
    assert issubclass(_runpath_base(), MyArgs)


def test_explicit_args_overrides_the_roots_dunder(capsys):
    class Other(PyTrueNASArgs):
        flavour: str = "x"
        "A different flag"
        ("--flavour",)  # type: ignore

    class MyApp(PyTrueNAS):
        _ARGS_ = MyArgs

    with pytest.raises(SystemExit):
        main("mytool", ["--help"], root=MyApp, args=Other)
    out = capsys.readouterr().out
    assert "--flavour" in out and "--region" not in out


# -- rejection -------------------------------------------------------------


def test_rejects_a_non_pytruenasargs_class():
    """The fan-out calls _expanded_targets_ on the parsed instance."""

    class Bare:
        pass

    with pytest.raises(TypeError, match="PyTrueNASArgs"):
        main("mytool", ["--help"], args=Bare)  # type: ignore[arg-type]
