"""`help` and `call` driven through `main()`, against a recording fake client.

Argument vector in, middleware calls and output out: the parse, the `--`
tail, the schema lookup and where the payload lands are exercised together,
which is where a defect between them shows.
"""

from __future__ import annotations

import collections
import json
import logging

import pytest

import pytruenas.host
import pytruenas.main as main

USER_METHODS = {
    "user.create": {
        "description": "Create a new user.",
        "accepts": [
            {
                "title": "user_create",
                "type": "object",
                "additionalProperties": False,
                "required": ["username"],
                "properties": {
                    "username": {"type": "string"},
                    "shell": {
                        "type": "string",
                        "enum": ["/usr/bin/zsh", "/usr/bin/bash"],
                    },
                    "smb": {"type": "boolean"},
                },
            }
        ],
        "returns": [{"type": "integer"}],
    },
    "user.update": {
        "description": "Update an existing user.",
        "accepts": [
            {"title": "id", "type": "integer"},
            {
                "title": "user_update",
                "type": "object",
                "additionalProperties": False,
                "properties": {"full_name": {"type": "string"}},
            },
        ],
        "returns": [{"type": "object"}],
    },
}


class _Api:
    """``client.api``: attribute chains and ``[name]`` both name a method."""

    def __init__(self, client, name=""):
        self._client = client
        self._name = name

    def __getattr__(self, part):
        return _Api(self._client, f"{self._name}.{part}" if self._name else part)

    def __getitem__(self, name):
        return _Api(self._client, name)

    def __call__(self, *params, **kwargs):
        return self._client.answer(self._name, params)


class FakeClient:
    """What `args._client_` builds: records every middleware call it gets."""

    calls: "collections.Counter[str]" = collections.Counter()
    sent: "list[tuple[str, tuple]]" = []
    get_methods_error: "Exception | None" = None

    def __init__(self, target, *args, **kwargs):
        self.name = target
        self.logger = logging.getLogger("pytruenas.test.fakeclient")
        self.api = _Api(self)

    def answer(self, method, params):
        FakeClient.calls[method] += 1
        if method == "system.info":
            return {"version": "26.0.0"}
        if method == "core.get_services":
            return {"user": {"type": "crud"}, "system": {"type": "config"}}
        if method == "core.get_methods":
            if FakeClient.get_methods_error is not None:
                raise FakeClient.get_methods_error
            service = params[0]
            return {
                n: m for n, m in USER_METHODS.items() if n.startswith(service + ".")
            }
        FakeClient.sent.append((method, params))
        return {"ok": True}

    def close(self):
        pass


@pytest.fixture(autouse=True)
def _fake(monkeypatch, tmp_path):
    FakeClient.calls = collections.Counter()
    FakeClient.sent = []
    FakeClient.get_methods_error = None
    monkeypatch.setattr(pytruenas.host, "TrueNASClient", FakeClient)
    monkeypatch.setenv("PYTRUENAS_CACHE", str(tmp_path / "cache"))
    monkeypatch.delenv("TN_CREDS", raising=False)
    monkeypatch.delenv("PYTRUENAS_CONFIG", raising=False)
    monkeypatch.delenv("PYTRUENAS_CFG", raising=False)
    monkeypatch.chdir(tmp_path)  # no ./pytruenas.yaml


def _main(*argv):
    return main.main("pytruenas", list(argv))


# -- help ------------------------------------------------------------------


def test_help_lists_the_services(capsys):
    assert _main("help", "all", "nas1") == 0
    out = capsys.readouterr().out
    assert "2 services" in out and "user" in out and "system" in out


def test_help_describes_a_namespace_and_a_method(capsys):
    assert _main("help", "user", "nas1") == 0
    out = capsys.readouterr().out
    assert "create" in out and "update" in out

    assert _main("help", "user.create", "nas1") == 0
    out = capsys.readouterr().out
    assert "username" in out and "/usr/bin/bash" in out


def test_help_json_is_the_definition_slice(capsys):
    assert _main("help", "--json", "user", "nas1") == 0
    assert sorted(json.loads(capsys.readouterr().out)) == ["user.create", "user.update"]


@pytest.mark.parametrize(
    "name, message",
    [("user.creat", "did you mean: user.create"), ("usr", "no service named 'usr'")],
)
def test_help_for_an_unknown_name_exits_2_with_suggestions(name, message, caplog):
    with caplog.at_level(logging.ERROR):
        assert _main("help", name, "nas1") == 2
    assert message in caplog.text


@pytest.mark.parametrize("name", ["all", "user", "user.create"])
def test_help_reads_the_version_once(name):
    """Each cache lookup read the version again: three `system.info` round
    trips per invocation, even with everything cached."""
    for _ in ("cold", "warm"):
        FakeClient.calls.clear()
        assert _main("help", name, "nas1") == 0
        assert FakeClient.calls["system.info"] == 1


# -- call ------------------------------------------------------------------


def test_call_sends_its_params(capsys):
    assert _main("call", "system.version", "-p", '{"a": 1}', "-p", "5", "nas1") == 0
    assert FakeClient.sent == [("system.version", ({"a": 1}, 5))]
    assert json.loads(capsys.readouterr().out) == {"ok": True}


def test_call_fields_after_the_separator_are_typed_from_the_schema():
    argv = ["call", "user.create", "nas1", "--"]
    argv += ["--username=svc", "shell=/usr/bin/bash", "--smb=false"]
    assert _main(*argv) == 0
    payload = {"username": "svc", "shell": "/usr/bin/bash", "smb": False}
    assert FakeClient.sent == [("user.create", (payload,))]


def test_call_fields_fill_the_payload_after_the_id():
    argv = ["call", "user.update", "-p", "7", "nas1", "--", "--full_name=New"]
    assert _main(*argv) == 0
    assert FakeClient.sent == [("user.update", (7, {"full_name": "New"}))]


def test_call_pads_missing_params_before_the_payload_with_null():
    """With no `-p`, the payload still goes where the method wants it, and
    the id ahead of it is sent as null for the appliance to refuse."""
    assert _main("call", "user.update", "nas1", "--", "--full_name=New") == 0
    assert FakeClient.sent == [("user.update", (None, {"full_name": "New"}))]


@pytest.mark.parametrize(
    "tail, message",
    [
        (["--usernme=svc"], "usernme"),
        (["--username=svc", "--shell=/bin/sh"], "/usr/bin/zsh"),
    ],
)
def test_call_refuses_a_bad_field_before_calling_anything(tail, message, caplog):
    with caplog.at_level(logging.ERROR):
        assert _main("call", "user.create", "nas1", "--", *tail) == 2
    assert message in caplog.text
    assert FakeClient.sent == []


def test_call_an_unknown_method_exits_2_with_suggestions(caplog):
    with caplog.at_level(logging.ERROR):
        assert _main("call", "user.creat", "nas1", "--", "--username=x") == 2
    assert "did you mean: user.create" in caplog.text
    assert FakeClient.sent == []


@pytest.mark.parametrize("error", [RuntimeError("closed"), KeyError("version")])
def test_call_without_a_schema_sends_the_fields_untyped(error, caplog):
    """A schema that cannot be read is a warning: the untyped call still goes
    out, with the payload last. A KeyError raised while reading it was taken
    for "no such method" and failed on an unbound name."""
    FakeClient.get_methods_error = error
    with caplog.at_level(logging.WARNING):
        assert _main("call", "user.create", "nas1", "--", "--smb=false") == 0
    assert "typing fields as plain JSON" in caplog.text
    assert FakeClient.sent == [("user.create", ({"smb": False},))]


def test_call_no_schema_never_reads_one():
    assert _main("call", "--no-schema", "user.create", "nas1", "--", "uid=5") == 0
    assert FakeClient.calls["core.get_methods"] == 0
    assert FakeClient.sent == [("user.create", ({"uid": 5},))]


def test_a_tail_the_command_does_not_read_is_reported(caplog):
    with caplog.at_level(logging.WARNING):
        assert _main("help", "user", "nas1", "--", "--username=x") == 0
    assert "ignoring the 1 argument(s) after '--': help reads none" in caplog.text


# -- help --dump -------------------------------------------------------------


@pytest.fixture
def _cached_dump():
    """A whole definition in the cache, so `--dump` reads it with no shell."""
    from test_cli_help import USER_CREATE, USER_UPDATE

    from pytruenas.utils import apicache

    older = {"version": "v25.10.0", "methods": [USER_CREATE], "events": []}
    newest = {"version": "v26.0.0", "methods": [USER_CREATE, USER_UPDATE]}
    api = {"versions": [{**newest, "events": []}, older]}
    apicache.store(api, apicache.path_for("nas1", "26.0.0"))


@pytest.mark.parametrize(
    "argv, expected",
    [
        (["all"], "user"),
        (["user.update"], "full_name"),
        (["user"], "update"),
        (["--api-version", "v25.10.0", "user"], "create"),
    ],
)
def test_help_dump_reads_the_cached_definition(argv, expected, _cached_dump, capsys):
    assert _main("help", "--dump", *argv, "nas1") == 0
    assert expected in capsys.readouterr().out
    assert FakeClient.calls["core.get_methods"] == 0


def test_help_dump_json(_cached_dump, capsys):
    assert _main("help", "--dump", "--json", "user", "nas1") == 0
    assert sorted(json.loads(capsys.readouterr().out)) == ["user.create", "user.update"]


@pytest.mark.parametrize(
    "argv, message",
    [
        (["--api-version", "v1.0", "user"], "version 'v1.0' not found"),
        (["user.creat"], "user.create"),
    ],
)
def test_help_dump_unknown_names_exit_2(argv, message, _cached_dump, caplog):
    with caplog.at_level(logging.ERROR):
        assert _main("help", "--dump", *argv, "nas1") == 2
    assert message in caplog.text
