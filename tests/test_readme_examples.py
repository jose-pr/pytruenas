"""The README's and the examples' code runs as written.

Only the websocket is fake: ``TrueNASWSConnection._connect`` returns an
in-process peer that answers the JSON-RPC frames the real transport sends, so
the client, the namespace helpers, the CLI and the RunPath flows are the
shipped code. Each documented ``pytruenas`` command line is taken from the
Markdown itself, so a command edited in the docs is the command tested.
"""

import json
import logging
import re
import shlex
import threading
from pathlib import Path

import pytest

from pytruenas import connection
from pytruenas.main import main

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
EXAMPLES = ROOT / "examples"

# The sdist ships tests/ and README.md; examples/ is in it too, but a
# repackaged tree may drop it.
pytestmark = pytest.mark.skipif(
    not README.is_file(), reason="README.md is not in this tree"
)


class _Middleware:
    """The few middleware methods the documented code calls, over in-memory
    tables. Anything else is an error, so an undocumented call shows up."""

    def __init__(self):
        self.calls = []
        self.lock = threading.Lock()
        self.network = {"hostname": "fake-nas", "nameserver1": "192.0.2.1"}
        self.tables = {
            "user": [{"id": 1, "username": "root", "uid": 0, "full_name": "root"}],
            "pool": [{"id": 1, "name": "data", "healthy": False, "status": "DEGRADED"}],
            "service": [
                {"id": 1, "service": "cifs", "enable": False, "state": "STOPPED"},
                {"id": 2, "service": "nfs", "enable": True, "state": "RUNNING"},
            ],
        }

    def methods(self):
        with self.lock:
            return [method for method, _ in self.calls]

    def answer(self, method, params):
        with self.lock:
            self.calls.append((method, params))
            return self._answer(method, params)

    def _answer(self, method, params):
        namespace, _, leaf = method.rpartition(".")
        if method.startswith("auth.login") or method == "service.start":
            return True
        if method == "system.info":
            return {
                "hostname": "fake-nas",
                "version": "26.0.0",
                "uptime": "1 day",
                "cores": 4,
            }
        if method == "network.configuration.config":
            return dict(self.network)
        if method == "network.configuration.update":
            self.network.update(params[0])
            return dict(self.network)
        table = self.tables.setdefault(namespace, [])
        if leaf == "query":
            filters = params[0] if params else []
            options = params[1] if len(params) > 1 else {}
            rows = [
                row
                for row in table
                if all(row.get(key) == value for key, _op, value in filters)
            ]
            return rows[: options["limit"]] if options.get("limit") else rows
        if leaf == "create":
            data = params[0]
            # Datasets and snapshots are keyed by name; everything else by number.
            if namespace == "pool.dataset":
                key = data["name"]
            elif namespace == "pool.snapshot":
                key = f"{data['dataset']}@{data['name']}"
            else:
                key = len(table) + 1
            row = {"id": key, **data}
            table.append(row)
            return row
        if leaf in ("get_instance", "update"):
            for row in table:
                if params[0] in (row.get("id"), row.get("service")):
                    if leaf == "update":
                        row.update(params[1])
                    return row
            raise _Error(f"[ENOENT] {params[0]!r} does not exist", 2)
        raise _Error(f"[EINVAL] the fake has no answer for {method}", 22)


class _Error(Exception):
    def __init__(self, reason, errno):
        super().__init__(reason)
        self.reason, self.errno = reason, errno


class _FakeWebSocket:
    """The peer end of one connection: answers each request frame as it is
    sent, and hands the answer to the transport's reader thread."""

    def __init__(self, middleware):
        self.middleware = middleware
        self.inbox = []
        self.cond = threading.Condition()
        self.closed = False

    def send(self, data):
        request = json.loads(data)
        if "id" not in request:
            return
        response = {"jsonrpc": "2.0", "id": request["id"]}
        try:
            response["result"] = self.middleware.answer(
                request["method"], request.get("params") or []
            )
        except _Error as exc:
            response["error"] = {
                "code": -32001,
                "data": {"reason": exc.reason, "error": exc.errno},
            }
        with self.cond:
            self.inbox.append(json.dumps(response))
            self.cond.notify_all()

    def recv(self):
        with self.cond:
            while not self.inbox and not self.closed:
                self.cond.wait(timeout=1)
            if not self.inbox:
                raise OSError("closed")
            return self.inbox.pop(0)

    def close(self):
        with self.cond:
            self.closed = True
            self.cond.notify_all()

    def shutdown(self):
        self.close()


@pytest.fixture
def middleware(monkeypatch):
    peer = _Middleware()
    monkeypatch.setattr(
        connection.TrueNASWSConnection,
        "_connect",
        lambda self: _FakeWebSocket(peer),
    )
    return peer


def _fenced(path, language):
    """``(heading, code)`` for each fenced block of ``language`` in ``path``."""
    heading, blocks = "", []
    lines = iter(path.read_text(encoding="utf-8").splitlines())
    for line in lines:
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
        elif line.strip() == f"```{language}":
            body = []
            for inner in lines:
                if inner.strip() == "```":
                    break
                body.append(inner)
            blocks.append((heading, "\n".join(body) + "\n"))
    return blocks


def _commands(path):
    """Each ``pytruenas ...`` line of the shell blocks in ``path``, as argv."""
    commands = []
    for _, code in _fenced(path, "sh"):
        for line in code.splitlines():
            if line.startswith("pytruenas "):
                commands.append(shlex.split(line, comments=True)[1:])
    return commands


def _run(argv):
    try:
        return main(argv=argv)
    except SystemExit as exc:
        return exc.code


def _complaints(caplog):
    return [r.getMessage() for r in caplog.records if r.levelno >= logging.WARNING]


def test_every_python_block_in_the_readme_compiles():
    blocks = _fenced(README, "python")
    assert blocks
    for heading, code in blocks:
        compile(code, f"README.md ({heading})", "exec")


def test_the_readme_quick_start_runs(middleware, capsys):
    """The first Quick start block, as written: a query, an `_upsert` that
    creates, and the local-socket client."""
    (code,) = [code for heading, code in _fenced(README, "python")][:1]
    exec(compile(code, "README.md", "exec"), {"__name__": "readme"})  # noqa: S102

    calls = middleware.methods()
    assert "user.query" in calls
    assert "user.create" in calls
    assert calls[-1] == "system.info"
    created = [params for method, params in middleware.calls if method == "user.create"]
    assert created == [
        [{"username": "svc", "full_name": "Service", "group_create": True}]
    ]
    out = capsys.readouterr().out
    assert "root\n" in out and "fake-nas" in out


# The documented commands that need nothing beyond what `_Middleware` answers.
# The rest need a live host: `deploy` copies files to it, `dump-api`,
# `generate-typings`, `help` and `call` with fields read its method schema.
_OFFLINE = re.compile(r"^(query|call [a-z.]+ [^-]+$)")


def _offline(argv):
    words = [word for word in argv if not word.startswith("-")]
    return bool(_OFFLINE.match(" ".join(words))) and "--" not in argv


@pytest.mark.parametrize(
    "argv",
    [argv for argv in _commands(README) if _offline(argv)],
    ids=shlex.join,
)
def test_a_readme_command_runs(argv, middleware, caplog):
    assert _run(argv) == 0
    assert _complaints(caplog) == []
    assert middleware.methods()[-1] == argv[1] + (
        ".query" if argv[0] == "query" else ""
    )


def test_the_readme_documents_runnable_commands():
    """The filter above must not quietly select nothing."""
    assert {argv[0] for argv in _commands(README) if _offline(argv)} == {
        "query",
        "call",
    }


def _flow_commands(path, flow):
    return [argv for argv in _commands(path) if flow in argv and "help" not in argv]


@pytest.mark.parametrize(
    "argv",
    _flow_commands(EXAMPLES / "runpath" / "README.md", "health"),
    ids=shlex.join,
)
def test_the_health_flow_runs_as_documented(argv, middleware, caplog, monkeypatch):
    monkeypatch.chdir(ROOT)
    assert _run(argv) == 0
    assert _complaints(caplog) == []
    assert "system.info" in middleware.methods()
    if "--rcopts" not in argv:
        assert "pool: data is DEGRADED" in caplog.text


@pytest.mark.parametrize(
    "argv",
    [argv for argv in _flow_commands(EXAMPLES / "README.md", "provision")],
    ids=shlex.join,
)
def test_the_provision_flow_runs_as_documented(argv, middleware, caplog, monkeypatch):
    """Dry-run by default, as the README says: nothing is written without
    `--apply`, and with it every step's change reaches the middleware."""
    monkeypatch.chdir(ROOT)
    assert _run(argv) == 0
    assert _complaints(caplog) == []
    writes = {
        method
        for method in middleware.methods()
        if method.rpartition(".")[2] in ("create", "update", "start")
    }
    if "--apply" not in argv:
        assert writes == set()
        assert "change(s) planned" in caplog.text
    else:
        assert {
            "group.create",
            "user.create",
            "network.configuration.update",
            "pool.dataset.create",
            "pool.snapshot.create",
            "sharing.smb.create",
            "sharing.nfs.create",
            "service.update",
            "service.start",
        } <= writes


@pytest.mark.requires("yaml")
def test_the_yaml_script_example_runs(middleware, tmp_path, capsys, monkeypatch):
    config = tmp_path / "pytruenas.yaml"
    config.write_bytes(b"host: nas1\nusername: root\npassword: secret\n")
    namespace = {"__name__": "example"}
    script = EXAMPLES / "scripts" / "simple_client_from_yaml.py"
    exec(compile(script.read_bytes(), str(script), "exec"), namespace)  # noqa: S102
    assert namespace["main"]([str(config)]) == 0
    assert "fake-nas -- TrueNAS 26.0.0, 4 cores" in capsys.readouterr().out
    assert middleware.methods()[-1] == "system.info"


@pytest.mark.requires("yaml")
@pytest.mark.parametrize("given, verify", [({}, True), ({"sslverify": False}, False)])
def test_the_yaml_script_verifies_certificates_unless_told_not_to(given, verify):
    namespace = {"__name__": "example"}
    script = EXAMPLES / "scripts" / "simple_client_from_yaml.py"
    exec(compile(script.read_bytes(), str(script), "exec"), namespace)  # noqa: S102
    client = namespace["client_from_config"]({"host": "nas1", **given})
    assert client.config.sslverify is verify
