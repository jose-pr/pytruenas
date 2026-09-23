"""Per-target isolation in the fan-out: state, clients, logs and output.

The CLI's whole purpose is running one command against many targets, and most of
these defects only appear there -- shared args, leaked clients, log files that
miss the records they exist for, interleaved JSON.
"""

import datetime
import json
import logging
import threading
from pathlib import Path
from types import SimpleNamespace

import pytest

import pytruenas.host
import pytruenas.main as main
from pytruenas.utils.cmd import PyTrueNASArgs, emit, emit_json, json_default


class _Args(PyTrueNASArgs):
    def __init__(self, targets=("nas1", "nas2"), logto="-"):
        self._targets = list(targets)
        self.parallel = 2
        self.logto = logto
        self.sslverify = None
        self.insecure = True

    @property
    def _logger_(self):
        logger = logging.getLogger("pytruenas.test.fanout")
        # The real CLI sets levels from --loglevel; without this the INFO
        # records these tests look for never reach a handler at all.
        logger.setLevel(logging.DEBUG)
        return logger

    def _expanded_targets_(self):
        return self._targets


class _Client:
    """Records whether it was closed."""

    def __init__(self, *a, **k):
        self.closed = False
        self.built.append(self)

    built: "list[_Client]" = []

    def close(self):
        self.closed = True


@pytest.fixture(autouse=True)
def _fake_clients(monkeypatch):
    _Client.built = []
    monkeypatch.setattr(pytruenas.host, "TrueNASHost", _Client)


def _command(run, **hooks):
    module = SimpleNamespace(
        __doc__="fake", run=run, init=None, success=None, finally_=None
    )
    for name, hook in hooks.items():
        setattr(module, name, hook)
    return SimpleNamespace(module=module)


def test_concurrent_targets_do_not_share_their_args():
    """`args` was one object for every target, so per-target state written on it
    (and `.target` itself) belonged to whichever target ran last. Run them
    overlapping, which is what --parallel does."""
    started = threading.Barrier(2)
    seen = []

    def run(client, args, logger):
        args.scratch = args.target  # a command recording per-target state
        started.wait(5)  # hold both inside run() at once
        seen.append((args.target, args.scratch))
        return 0

    shared = _Args()
    threads = [
        threading.Thread(
            target=main._run_module_on_target,
            args=(_command(run), shared, target, shared._logger_),
        )
        for target in ("nas1", "nas2")
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(5)
    assert sorted(seen) == [("nas1", "nas1"), ("nas2", "nas2")]
    assert not hasattr(shared, "scratch")  # the shared object is untouched


def test_an_init_hook_can_see_the_target():
    targets = []
    command = _command(
        lambda client, args, logger: 0,
        init=lambda args, logger: targets.append(args.target) or _Client(),
    )
    args = _Args()
    main._run_module_on_target(command, args, "nas1", args._logger_)
    assert targets == ["nas1"]


def test_a_client_the_cli_built_is_closed():
    """Every target leaked its websocket and reader thread for the life of the
    process -- under --parallel, all of them at once."""
    args = _Args()
    main._run_module_on_target(
        _command(lambda client, args, logger: 0), args, "nas1", args._logger_
    )
    assert len(_Client.built) == 1 and _Client.built[0].closed is True


def test_a_client_from_an_init_hook_is_left_alone():
    """It belongs to the hook, which may be caching it."""
    mine = _Client()
    command = _command(lambda client, args, logger: 0, init=lambda args, logger: mine)
    args = _Args()
    main._run_module_on_target(command, args, "nas1", args._logger_)
    assert mine.closed is False


def test_a_client_is_closed_even_when_the_command_raises():
    args = _Args()
    with pytest.raises(RuntimeError):
        main._run_module_on_target(
            _command(lambda *a: (_ for _ in ()).throw(RuntimeError("boom"))),
            args,
            "nas1",
            args._logger_,
        )
    assert _Client.built[0].closed is True


def test_logto_captures_library_records_too(tmp_path):
    """The handler was attached to the command's logger only, so the records a
    per-target file exists for -- a transport fallback warning, a connection
    error from the library -- never reached it."""
    args = _Args(logto=str(tmp_path / "{target}.log"))

    def run(client, args, logger):
        logging.getLogger("pytruenas").warning("fell back to the web shell")
        logger.info("from the command")
        return 0

    main._run_module_on_target(_command(run), args, "nas1", args._logger_)
    written = (tmp_path / "nas1.log").read_text(encoding="utf-8")
    assert "fell back to the web shell" in written
    assert "from the command" in written
    # And the handler is gone afterwards, from both loggers.
    assert not any(
        isinstance(h, logging.FileHandler)
        for h in logging.getLogger("pytruenas").handlers
    )


def test_two_targets_write_to_their_own_files(tmp_path):
    args = _Args(logto=str(tmp_path / "{target}.log"))

    def run(client, args, logger):
        logger.info("hello from %s", args.target)
        return 0

    for target in ("nas1", "nas2"):
        main._run_module_on_target(_command(run), args, target, args._logger_)
    assert "hello from nas1" in (tmp_path / "nas1.log").read_text(encoding="utf-8")
    assert "hello from nas1" not in (tmp_path / "nas2.log").read_text(encoding="utf-8")


# -- output ---------------------------------------------------------------


def test_result_lines_are_written_whole(capsys):
    """`print()` is two writes, so concurrent targets interleaved mid-line and
    neither line parsed as JSON."""
    payload = {"x": "y" * 500}
    threads = [threading.Thread(target=emit_json, args=(payload,)) for _ in range(12)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    lines = [line for line in capsys.readouterr().out.splitlines() if line]
    assert len(lines) == 12
    assert all(json.loads(line) == payload for line in lines)


def test_multi_target_output_says_which_target(capsys):
    args = _Args(targets=("nas1", "nas2"))
    args.target = "root:secret@nas1"
    emit_json({"ok": True}, args)
    line = json.loads(capsys.readouterr().out)
    assert line["result"] == {"ok": True}
    assert line["target"] == "root@nas1"  # the password is not in the output


def test_single_target_output_is_the_bare_result(capsys):
    args = _Args(targets=("nas1",))
    args.target = "nas1"
    emit_json({"ok": True}, args)
    assert json.loads(capsys.readouterr().out) == {"ok": True}


def test_sets_and_datetimes_serialize_as_json():
    """`default=str` emitted a Python repr (`"{1, 2}"`) that nothing can read."""
    assert json.loads(json.dumps({"s": {2, 1}}, default=json_default)) == {"s": [1, 2]}
    when = datetime.datetime(2026, 7, 19, 3, 42, tzinfo=datetime.timezone.utc)
    assert json.loads(json.dumps(when, default=json_default)) == when.isoformat()
    assert json.loads(json.dumps(b"bytes", default=json_default)) == "bytes"


# -- worker discipline ----------------------------------------------------


def test_an_unknown_typings_version_fails_one_target_not_the_run(tmp_path):
    """It raised SystemExit inside a fan-out worker, which aborted the whole run
    and discarded the other targets' exit codes."""
    from pytruenas.cmd import generate_typings

    args = SimpleNamespace(
        api_cache=tmp_path / "dump.json",
        api_version="v99.0.0",
        path=tmp_path / "out",
    )
    args.api_cache.write_text(
        json.dumps({"versions": [{"version": "v26.0.0", "methods": []}]}),
        encoding="utf-8",
    )
    logger = logging.getLogger("pytruenas.test.typings")
    assert generate_typings.run(object(), args, logger) == 2


def test_a_command_without_run_is_not_offered(caplog):
    """It appeared in --help and then failed on every target."""
    command = SimpleNamespace(module=SimpleNamespace(__name__="broken", main=lambda: 0))
    with caplog.at_level(logging.WARNING):
        assert main._is_runnable(command, "broken") is False
    assert "defines no run(" in caplog.text
    ok = SimpleNamespace(module=SimpleNamespace(__name__="fine", run=lambda *a: 0))
    assert main._is_runnable(ok, "fine") is True
    # A class/RunPath command has no `module` and is never filtered.
    assert main._is_runnable(SimpleNamespace(), "runpath-dir") is True
