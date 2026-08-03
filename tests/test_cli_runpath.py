"""RunPath directories run once per target, each with its own client/context.

A RunPath is a directory of numbered ``NN-name.py`` steps (duho.runpath, adopted
in pytruenas via ``duho.runpath.register(base=PyTrueNASRunPathArgs)`` in
``pytruenas.main``). ``pytruenas`` fans the whole directory out per target, so a
RunPath command's steps run once per target with a per-target client -- restoring
the private predecessor's ``RunPathCmd`` behavior the current duho-based
``pytruenas`` never had.

Capabilities asserted here (per the plan): the per-target client built by
``__main__.py`` ``init(cmd, logger)``; per-target mutable state stashed on ``cmd``
and read by a later step (no cross-target bleed); the whole directory running
once per target; and ``--rcopts`` step selection. The source is injected via a
``tmp_path`` directory + ``PYTRUENAS_PATH`` (never ``-c``), matching this repo's
own testing convention; ``PYTRUENAS_PATH`` splits on ``os.pathsep`` (``;`` on
Windows), so a ``tmp_path`` with a drive letter is safe (unlike ``--cmdspath``'s
``:`` split).

Each step appends a line to a recorder FILE (path passed via an env var) rather
than a shared in-process object: a RunPath step is imported under a synthesized
unique ``sys.modules`` name, so a module-global shared with the step would not be
the same object the test holds. A file sidesteps that entirely.
"""

import json
import os

import pytest

import pytruenas.utils.runpath as _runpath_utils

_RECORD_ENV = "PYTRUENAS_TEST_RECORD"


class _FakeClient:
    """A stand-in TrueNASClient that records its target instead of connecting."""

    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.sslverify = kwargs.get("sslverify", False)


def _write_runpath(directory):
    """Create a RunPath directory with a lifecycle + two numbered steps.

    ``__main__.py`` ``init`` builds the per-target client and stashes per-target
    state on ``cmd`` (``cmd.context``); ``01-first`` (2-arg, takes ctx) and
    ``02-second`` (1-arg) each append what they saw to the recorder file named by
    the ``PYTRUENAS_TEST_RECORD`` env var.
    """
    flow = directory / "myflow"
    flow.mkdir()
    (flow / "__main__.py").write_text(
        "from pytruenas.utils.runpath import default_init\n"
        "def init(cmd, logger):\n"
        "    client = default_init(cmd, logger)\n"
        "    cmd.context = 'ctx-%s' % cmd.target\n"
        "    return client\n"
    )
    _recorder = (
        "import json, os\n"
        "def _record(entry):\n"
        "    with open(os.environ['PYTRUENAS_TEST_RECORD'], 'a') as fh:\n"
        "        fh.write(json.dumps(entry) + '\\n')\n"
    )
    (flow / "01-first.py").write_text(
        _recorder + "def main(cmd, ctx):\n"
        "    _record(['first', cmd.target, ctx.target, cmd.context])\n"
    )
    (flow / "02-second.py").write_text(
        _recorder + "def main(cmd):\n"
        "    _record(['second', cmd.target, None, cmd.context])\n"
    )
    return flow


def _records(record_path):
    """Read the recorder file into a {target: [entries...]} mapping, in order."""
    by_target: "dict" = {}
    if not os.path.exists(record_path):
        return by_target
    with open(record_path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            step, target, ctx_target, context = json.loads(line)
            by_target.setdefault(target, []).append((step, ctx_target, context))
    return by_target


@pytest.fixture()
def record_path(tmp_path, monkeypatch):
    path = tmp_path / "record.jsonl"
    monkeypatch.setenv(_RECORD_ENV, str(path))
    # `runpath` is the module that constructs the client, so patching its name
    # is what matters. (There used to be a second patch of `pytruenas.client`,
    # a re-export shim that no longer exists.)
    monkeypatch.setattr(_runpath_utils, "TrueNASClient", _FakeClient)
    monkeypatch.delenv("PYTRUENAS_PATH", raising=False)
    return path


def _run(tmp_path, monkeypatch, argv):
    """Point PYTRUENAS_PATH at a fresh RunPath dir and run main() with argv."""
    _write_runpath(tmp_path)
    monkeypatch.setenv("PYTRUENAS_PATH", str(tmp_path))
    import pytruenas.main as main

    return main.main("pytruenas", argv)


def test_runpath_runs_once_per_target(tmp_path, monkeypatch, record_path):
    rc = _run(tmp_path, monkeypatch, ["myflow", "nas1", "nas2"])
    assert rc == 0
    records = _records(record_path)
    # Each target ran BOTH steps, exactly once, in order.
    assert set(records) == {"nas1", "nas2"}
    for target in ("nas1", "nas2"):
        step_names = [entry[0] for entry in records[target]]
        assert step_names == ["first", "second"]


def test_runpath_per_target_client_and_context_no_bleed(
    tmp_path, monkeypatch, record_path
):
    _run(tmp_path, monkeypatch, ["myflow", "nasA", "nasB"])
    records = _records(record_path)
    # Each target's step 1 saw ITS OWN client (ctx.target == target) and its own
    # stashed cmd.context -- no cross-target bleed.
    assert records["nasA"][0] == ("first", "nasA", "ctx-nasA")
    assert records["nasB"][0] == ("first", "nasB", "ctx-nasB")
    # The 1-arg later step reads the SAME per-target stashed state.
    assert records["nasA"][1] == ("second", None, "ctx-nasA")
    assert records["nasB"][1] == ("second", None, "ctx-nasB")


def test_runpath_rcopts_disables_a_step(tmp_path, monkeypatch, record_path):
    # `!*,first` disables all then re-enables `first`: only step 1 should run.
    rc = _run(tmp_path, monkeypatch, ["myflow", "--rcopts", "!*,first", "nas1"])
    assert rc == 0
    records = _records(record_path)
    step_names = [entry[0] for entry in records["nas1"]]
    assert step_names == ["first"]


def _write_module_signature_runpath(directory):
    """A RunPath dir whose steps use the MODULE signature via ``@step``.

    Module commands are ``run(client, args, logger)``; duho calls a step
    ``main(cmd, ctx)``. These steps are written the module way and decorated,
    so the same body would work in either command kind.
    """
    flow = directory / "myflow"
    flow.mkdir()
    (flow / "__main__.py").write_text(
        "from pytruenas.utils.runpath import default_init as init\n"
    )
    _recorder = (
        "import json, os\n"
        "def _record(entry):\n"
        "    with open(os.environ['PYTRUENAS_TEST_RECORD'], 'a') as fh:\n"
        "        fh.write(json.dumps(entry) + '\\n')\n"
    )
    # Full module signature: client FIRST, args second, a real logger third.
    (flow / "01-first.py").write_text(
        _recorder + "from pytruenas.utils.runpath import step\n"
        "@step\n"
        "def main(client, args, logger):\n"
        "    _record(['first', args.target, client.target,\n"
        "             logger is not None and hasattr(logger, 'info')])\n"
    )
    # Shorter arity: a step that does not care about the logger.
    (flow / "02-second.py").write_text(
        _recorder + "from pytruenas.utils.runpath import step\n"
        "@step\n"
        "def main(client, args):\n"
        "    _record(['second', args.target, client.target, None])\n"
    )
    return flow


def test_step_decorator_gives_steps_the_module_signature(
    tmp_path, monkeypatch, record_path
):
    # The regression: without @step a module-signature step raises TypeError
    # (duho passes exactly 2 positionals, client second). With it, `client` is
    # the per-target client, `args` the cmd, and `logger` a usable logger.
    _write_module_signature_runpath(tmp_path)
    monkeypatch.setenv("PYTRUENAS_PATH", str(tmp_path))
    import pytruenas.main as main

    rc = main.main("pytruenas", ["myflow", "nas1"])
    assert rc == 0
    records = _records(record_path)
    # client.target is the per-target client -- proving it did NOT bind to cmd.
    assert records["nas1"][0] == ("first", "nas1", True)
    # A 2-arg step still gets (client, args) and is not handed the logger.
    assert records["nas1"][1] == ("second", "nas1", None)


def _write_undecorated_runpath(directory):
    """A RunPath dir whose 3-arg step uses the module signature, NO decorator."""
    flow = directory / "myflow"
    flow.mkdir()
    (flow / "__main__.py").write_text(
        "from pytruenas.utils.runpath import default_init as init\n"
    )
    _recorder = (
        "import json, os\n"
        "def _record(entry):\n"
        "    with open(os.environ['PYTRUENAS_TEST_RECORD'], 'a') as fh:\n"
        "        fh.write(json.dumps(entry) + '\\n')\n"
    )
    (flow / "01-first.py").write_text(
        _recorder + "def main(client, args, logger):\n"
        "    _record(['first', args.target, client.target,\n"
        "             logger is not None and hasattr(logger, 'info')])\n"
    )
    # duho's own shape must keep working alongside it, undecorated too.
    (flow / "02-second.py").write_text(
        _recorder + "def main(cmd, ctx):\n"
        "    _record(['second', cmd.target, ctx.target, None])\n"
    )
    return flow


def test_a_three_arg_step_needs_no_decorator(tmp_path, monkeypatch, record_path):
    # The step_adapter registered in pytruenas.main adapts an unambiguous
    # 3-arg step automatically: duho never calls a step with three positionals,
    # so it can only have meant the module signature.
    _write_undecorated_runpath(tmp_path)
    monkeypatch.setenv("PYTRUENAS_PATH", str(tmp_path))
    import pytruenas.main as main

    rc = main.main("pytruenas", ["myflow", "nas1"])
    assert rc == 0
    records = _records(record_path)
    # client bound FIRST (not to cmd), and a real logger arrived third.
    assert records["nas1"][0] == ("first", "nas1", True)
    # duho's native (cmd, ctx) step is untouched by the adapter.
    assert records["nas1"][1] == ("second", "nas1", None)


def test_step_adapter_leaves_ambiguous_arities_alone():
    # A 2-arg step could be duho's (cmd, ctx) or this app's (client, args), and
    # nothing in the signature says which. Guessing would silently swap them,
    # so shorter signatures still need an explicit @step.
    from pytruenas.utils.runpath import step, step_adapter

    def native(cmd, ctx):
        return cmd

    def one(cmd):
        return cmd

    for entrypoint in (native, one):
        assert step_adapter(entrypoint) is entrypoint

    def three(client, args, logger):
        return client

    assert step_adapter(three) is not three

    # An already-decorated step is not wrapped a second time -- that would feed
    # the wrapper's own (cmd, ctx) signature back in as if it were (client, args).
    decorated = step(three)
    assert step_adapter(decorated) is decorated


def test_step_decorator_preserves_arity_detection():
    # functools.wraps sets __wrapped__, which makes inspect.signature report the
    # DECORATED function. duho decides the call arity from exactly that, so a
    # 1-arg `@step def main(client)` would take duho's 1-arg branch and receive
    # ctx=None -- a silently None client rather than an error.
    from duho.runpath import _step_wants_ctx

    from pytruenas.utils.runpath import step

    @step
    def one(client):
        return client

    @step
    def three(client, args, logger):
        return client

    for entrypoint in (one, three):
        assert _step_wants_ctx(entrypoint) is True

    # The wrapper still reports the original name for tracebacks.
    assert one.__name__ == "one"
    # And a 1-arg step really receives the client, not None.
    assert one(object(), "the-client") == "the-client"


def test_runpath_discovered_as_subcommand(tmp_path, monkeypatch, record_path):
    # The RunPath directory becomes a subcommand named after the directory,
    # discovered via PYTRUENAS_PATH -- listed in --help output.
    _write_runpath(tmp_path)
    monkeypatch.setenv("PYTRUENAS_PATH", str(tmp_path))
    import contextlib
    import io

    import pytruenas.main as main

    out = io.StringIO()
    with contextlib.redirect_stdout(out), pytest.raises(SystemExit):
        main.main("pytruenas", ["--help"])
    assert "myflow" in out.getvalue()
