"""Host-side helpers: local network adapter discovery and directory packaging.

These run *on* a machine (not against the middleware API) and need the optional
``host`` extra (``pip install pytruenas[host]`` -> ``ifaddr``). Import lazily so
the rest of ``pytruenas.ops`` works without it.
"""

from __future__ import annotations

import fnmatch as _fnmatch
import hashlib as _hashlib
import ipaddress as _ip
import os as _os
import typing as _ty
from pathlib import Path as _Path

if _ty.TYPE_CHECKING:
    import ifaddr as _if


def _require_ifaddr():
    try:
        import ifaddr  # noqa: F401
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        raise ImportError(
            "network adapter helpers require the 'host' extra: "
            "pip install pytruenas[host]"
        ) from exc
    return ifaddr


class PathPatterns:
    """A small ``fnmatch`` allow/deny list loaded from ignore-style files."""

    def __init__(self, path: "str | _Path | None" = None, patterns: "_ty.Iterable[str] | None" = None) -> None:
        self.patterns = [*(patterns or [])]
        if path:
            self.load(path)

    def load(self, path: "str | _Path") -> None:
        path = _Path(path)
        if path.exists():
            self.patterns.extend(
                r.strip()
                for r in filter(None, path.read_text(encoding="utf-8").splitlines())
                if r
            )

    def is_match(self, path: "str") -> bool:
        path = str(path)
        return any(_fnmatch.fnmatch(path, pattern) for pattern in self.patterns)


def package(
    path: "str | _Path",
    symlink: "bool | _ty.Callable[[str, _Path], bool]" = True,
) -> bytes:
    """Build an in-memory tar of ``path`` with normalized ownership/modes.

    Files matching a ``.gitignore``/``.ignore`` in the top directory (plus a
    few built-in patterns) are skipped. ``symlink`` controls whether symlinks
    are stored as links (``True``) or dereferenced: pass a callable
    ``(tarname, realpath) -> bool`` for per-link control.
    """
    import io as _io
    import tarfile as _tarfile

    topdir = _Path(path)
    fileobj = _io.BytesIO()
    gitignore = PathPatterns(patterns=["/.*", "/**/*-stub", "/**/*.pyi"])
    for child in topdir.iterdir():
        if child.is_file() and (child.name.endswith(".gitignore") or child.name.endswith(".ignore")):
            gitignore.load(child)

    if not callable(symlink):
        _store_as_link = bool(symlink)

        def symlink(_name: str, _realpath: _Path, _flag=_store_as_link) -> bool:
            return _flag

    def _filter(tarinfo: "_tarfile.TarInfo"):
        name = tarinfo.name.removeprefix(topdir.name)
        if gitignore.is_match(name):
            return None
        relpath = _Path(name)

        if tarinfo.issym():
            realpath = (topdir / name.removeprefix("/")).resolve()
            if not symlink(tarinfo.name, realpath):
                tarinfo = tar.gettarinfo(_os.fspath(realpath), tarinfo.name)

        tarinfo.uid = 0
        tarinfo.gid = 0
        if tarinfo.isdir():
            tarinfo.mode = 0o755
        elif relpath.as_posix().startswith("/bin"):
            tarinfo.mode = 0o755
        else:
            tarinfo.mode = 0o644
        return tarinfo

    with _tarfile.open(fileobj=fileobj, mode="w") as tar:
        tar.add(topdir.as_posix(), topdir.name, filter=_filter)
    fileobj.seek(0)
    return fileobj.read()


def package_digest(path: "str | _Path", **kwargs) -> "tuple[bytes, bytes]":
    """Return ``(sha1_hex_digest, tar_bytes)`` for :func:`package`."""
    content = package(path, **kwargs)
    digest = _hashlib.sha1(content, usedforsecurity=False).hexdigest().encode()
    return digest, content


def is_localhost(ip: str) -> bool:
    return _ip.ip_address(ip).is_loopback


def is_local_ip(ip: str) -> bool:
    """True if ``ip`` is loopback or bound to a local network adapter."""
    address = _ip.ip_address(ip)
    if address.is_loopback:
        return True
    ifaddr = _require_ifaddr()
    for adapter in ifaddr.get_adapters():
        for entry in adapter.ips:
            try:
                if address == _ip.ip_address(entry.ip):
                    return True
            except ValueError:
                pass
    return False


def find_adapter_in_network(network: "str | _ip.IPv4Network | _ip.IPv6Network"):
    """Return the first local adapter whose IP falls inside ``network``."""
    net = _ip.ip_network(network)
    ifaddr = _require_ifaddr()
    for adapter in ifaddr.get_adapters():
        for entry in adapter.ips:
            ip = entry.ip
            if entry.is_IPv6:
                ip = f"{ip[0]}%{ip[2]}"
            try:
                interface = _ip.ip_interface((ip, entry.network_prefix))
            except ValueError:
                continue
            if interface in net:
                return adapter
    return None
