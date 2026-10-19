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
    monkeypatch.setattr(pytruenas.host, "TrueNASHost", FakeClient)
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
