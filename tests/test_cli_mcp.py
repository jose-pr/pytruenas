"""The hosts are part of every command's MCP tool schema, and a tool call reaches them.

Driven through the real stdio server (``PYTRUENAS_MCP=stdio``), as an agent would.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytruenas.main as main

ROOT = Path(__file__).resolve().parents[1]

_INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "1"},
    },
}


def _serve(*requests, path=None):
    """Replies by id from one stdio server session over ``requests``."""
    lines = [_INIT, {"jsonrpc": "2.0", "method": "notifications/initialized"}]
    lines += requests
    env = dict(os.environ, PYTRUENAS_MCP="stdio")
    env.pop("PYTRUENAS_PATH", None)
    if path:
        env["PYTRUENAS_PATH"] = str(path)
    out = subprocess.run(
        [sys.executable, "-m", "pytruenas"],
        input="".join(json.dumps(line) + "\n" for line in lines),
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    ).stdout
    return {reply["id"]: reply for reply in map(json.loads, out.splitlines())}


def test_every_tool_schema_has_targets():
    replies = _serve(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        path=ROOT / "examples" / "runpath",
    )
    tools = {tool["name"]: tool for tool in replies[2]["result"]["tools"]}
    assert "pytruenas.health" in tools  # a RunPath command
    for name, tool in tools.items():
        assert "targets" in tool["inputSchema"]["properties"], name


def test_a_tool_call_runs_on_the_targets_it_names():
    call = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "pytruenas.query",
            "arguments": {"namespace": "user", "targets": ["ws://127.0.0.1:9"]},
        },
    }
    text = _serve(call)[2]["result"]["content"][0]["text"]
    assert "[127.0.0.1:9]" in text
    assert "[localhost]" not in text


def test_hook_added_positionals_come_before_the_targets(tmp_path, monkeypatch):
    (tmp_path / "thing.py").write_text(
        "def register(parser, args):\n"
        "    parser.add_argument('item')\n"
        "def run(client, args, logger):\n"
        "    pass\n"
    )
    monkeypatch.setenv("PYTRUENAS_PATH", str(tmp_path))
    seen = {}

    def dispatch(command, instance):
        seen["item"] = instance.item
        seen["targets"] = instance._expanded_targets_()
        return 0

    with patch.object(main, "_dispatch", dispatch):
        assert main.main("pytruenas", ["thing", "x", "nas1", "nas2"]) == 0
    assert seen == {"item": "x", "targets": ["nas1", "nas2"]}
