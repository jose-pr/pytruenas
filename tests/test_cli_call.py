"""The `call` command: invoke any middleware method, targets trailing."""

import json
from unittest.mock import MagicMock, patch

import pytruenas.main as main
from pytruenas.cmd import call as call_cmd
from pytruenas.utils.cmd import json_value


def _parse(argv):
    captured = {}

    def fake_dispatch(command, instance):
        captured["cmd"] = command._parsername_
        captured["method"] = getattr(instance, "method", None)
        captured["params"] = getattr(instance, "params", None)
        captured["targets"] = instance._expanded_targets_()
        return 0

    with patch.object(main, "_dispatch", fake_dispatch):
        main.main("pytruenas", argv)
    return captured


def test_method_then_targets():
    c = _parse(["call", "system.info", "nas1", "nas2"])
    assert c["cmd"] == "call"
    assert c["method"] == "system.info"
    assert c["targets"] == ["nas1", "nas2"]


def test_params_are_options_not_positionals():
    # -p before the trailing targets (or after them) keeps params and targets
    # distinct. argparse cannot split a `-p VALUE` sandwiched *between* the
    # method and the target positionals, so put -p first or last.
    c = _parse(["call", "-p", '{"username": "svc"}', "user.create", "nas1"])
    assert c["method"] == "user.create"
    assert c["params"] == ['{"username": "svc"}']
    assert c["targets"] == ["nas1"]  # -p value did not become a target

    c2 = _parse(["call", "user.create", "nas1", "-p", '{"username": "svc"}'])
    assert c2["targets"] == ["nas1"]
    assert c2["params"] == ['{"username": "svc"}']


def test_param_json_parsing():
    assert json_value('{"a": 1}') == {"a": 1}
    assert json_value("5") == 5
    assert json_value("true") is True
    # non-JSON falls back to the raw string
    assert json_value("plain-string") == "plain-string"


def test_run_invokes_method_and_prints(capsys):
    """Parameters reach the method, decoded, in order.

    `args` is a plain namespace, not a MagicMock: a misspelled attribute on a
    MagicMock auto-vivifies to an empty iterable, which let a `run()` that
    dropped every `-p` pass.
    """
    from types import SimpleNamespace

    seen = []
    method = MagicMock(side_effect=lambda *p: seen.append(p) or {"version": "26.0"})
    client = MagicMock()
    client.api.__getitem__.return_value = method
    args = SimpleNamespace(method="system.info", params=['{"a": 1}', "5"])
    call_cmd.run(client, args, MagicMock())
    client.api.__getitem__.assert_called_once_with("system.info")
    assert seen == [({"a": 1}, 5)]
    assert json.loads(capsys.readouterr().out) == {"version": "26.0"}
