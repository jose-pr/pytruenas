"""Pure-logic coverage for ops/midclt's systemd config parser.

Only the client-free parser is exercised here; the unit install/systemctl paths
are live-host glue and are not unit-tested.
"""

import io

from pytruenas.ops.midclt import _SystemdConfigParser


def test_systemd_parser_preserves_option_case():
    # Systemd keys are case-sensitive (ExecStart, not execstart); the default
    # ConfigParser lowercases them, so optionxform is overridden.
    p = _SystemdConfigParser()
    p.read_dict({"Service": {"ExecStart": "/bin/true", "Restart": "always"}})
    out = io.StringIO()
    p.write(out)
    text = out.getvalue()
    assert "ExecStart = /bin/true" in text
    assert "execstart" not in text


def test_systemd_parser_roundtrips_equals_delimiter():
    p = _SystemdConfigParser()
    p.read_string("[Unit]\nDescription = demo\n")
    assert p["Unit"]["Description"] == "demo"
