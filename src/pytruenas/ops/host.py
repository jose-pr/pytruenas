"""Local network adapter discovery.

These run *on* a machine, not against the middleware API. Discovery is
delegated to :mod:`netimps` (already a runtime dependency), whose
``get_interfaces``/``interface_for`` need no third-party package -- so there is
no longer a ``host`` extra to install.

NOTE: the directory-packaging helpers (``package``/``package_digest``/
``PathPatterns``) that used to live here have moved to
:mod:`pytruenas.utils.bundle` as ``tar_tree``/``tar_digest``, next to the code
that builds the trees they archive. They were unrelated to adapter discovery
and were only ever used for deployment.
"""

from __future__ import annotations

import ipaddress as _ip

import netimps as _netimps


def is_localhost(ip: str) -> bool:
    return _ip.ip_address(ip).is_loopback


def is_local_ip(ip: str) -> bool:
    """True if ``ip`` is loopback or bound to a local network adapter.

    Loopback is answered without enumeration; otherwise ``netimps.interface_for``
    does the reverse lookup (returns the owning interface, or ``None``).
    """
    address = _ip.ip_address(ip)
    if address.is_loopback:
        return True
    return _netimps.interface_for(address, strict=True) is not None


def find_adapter_in_network(network: "str | _ip.IPv4Network | _ip.IPv6Network"):
    """Return the first local interface with an IP inside ``network``.

    Returns a :class:`netimps.Interface` (``.name``/``.ips``/…), or ``None``.
    """
    net = _ip.ip_network(network)
    for interface in _netimps.get_interfaces():
        for addr in interface.ips:
            # ``addr`` is an IPv4/IPv6Interface (address + prefix); test the
            # bare address for membership in the target network.
            if addr.ip in net:
                return interface
    return None
