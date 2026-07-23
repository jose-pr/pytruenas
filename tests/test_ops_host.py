"""ops.host network helpers, now backed by netimps (not ifaddr).

The adapter-enumeration paths are mocked at the netimps boundary so the tests
are deterministic regardless of the host's real interfaces.
"""

import ipaddress
from types import SimpleNamespace

from pytruenas.ops import host


def test_is_localhost():
    assert host.is_localhost("127.0.0.1") is True
    assert host.is_localhost("::1") is True
    assert host.is_localhost("8.8.8.8") is False


def test_is_local_ip_loopback_shortcuts_without_enumeration(monkeypatch):
    # loopback must answer True without calling netimps at all
    def _boom(*a, **k):
        raise AssertionError("interface_for should not be called for loopback")

    monkeypatch.setattr(host._netimps, "interface_for", _boom)
    assert host.is_local_ip("127.0.0.1") is True


def test_is_local_ip_delegates_to_interface_for(monkeypatch):
    calls = {}

    def fake_interface_for(address, strict=True):
        calls["address"] = address
        calls["strict"] = strict
        # pretend this address is bound locally
        return SimpleNamespace(name="eth0")

    monkeypatch.setattr(host._netimps, "interface_for", fake_interface_for)
    assert host.is_local_ip("10.0.0.5") is True
    assert calls["address"] == ipaddress.ip_address("10.0.0.5")
    assert calls["strict"] is True


def test_is_local_ip_returns_false_when_no_interface(monkeypatch):
    monkeypatch.setattr(host._netimps, "interface_for", lambda a, strict=True: None)
    assert host.is_local_ip("203.0.113.9") is False


def _iface(name, *cidrs):
    return SimpleNamespace(
        name=name, ips=[ipaddress.ip_interface(c) for c in cidrs]
    )


def test_find_adapter_in_network_matches(monkeypatch):
    ifaces = [_iface("lo", "127.0.0.1/8"), _iface("eth0", "10.0.0.5/24")]
    monkeypatch.setattr(host._netimps, "get_interfaces", lambda: ifaces)
    found = host.find_adapter_in_network("10.0.0.0/24")
    assert found is not None and found.name == "eth0"


def test_find_adapter_in_network_no_match_returns_none(monkeypatch):
    ifaces = [_iface("eth0", "10.0.0.5/24")]
    monkeypatch.setattr(host._netimps, "get_interfaces", lambda: ifaces)
    assert host.find_adapter_in_network("192.168.1.0/24") is None
