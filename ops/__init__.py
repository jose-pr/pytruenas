import hashlib
from pathlib import Path
import ipaddress as _ip
import ifaddr as _if
import fnmatch
import netutils
import typing as _ty
from typing import Any
from coquilib import logging as _logging
import os as _os

from .. import config as _config

LOGGER = _logging.getLogger()
_PACKAGE = None


class PathPatterns:
    def __init__(self, path=None, patterns=None) -> None:
        self.patterns = [*(patterns or [])]
        if path:
            self.load(path)

    def load(self, path: Path):
        path = Path(path)
        if path.exists():
            self.patterns.extend(
                [r.strip() for r in filter(None, path.read_text().splitlines()) if r]
            )

    def is_match(self, path: str):
        path = str(path)
        for pattern in self.patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
        return False


def packageself(reload=False):
    global _PACKAGE
    topdir = _config.PACKAGE_RUN_PATH
    if reload or not _PACKAGE:

        def allowsymlinks(name: str, realpath: Path):
            if '.py' in name:
                pass
            return not (
                not realpath.is_relative_to(topdir)
                and name.removeprefix(topdir.name).startswith("/lib/")
            )

        content = package(topdir, symlink=allowsymlinks)
        _PACKAGE = (
            hashlib.sha1(content, usedforsecurity=False).hexdigest().encode(),
            content,
        )
    return _PACKAGE


def package(path: str | Path, symlink: bool | _ty.Callable[[str, Path], bool] = True):
    import tarfile, io

    topdir = Path(path)
    fileobj = io.BytesIO()
    gitignore: PathPatterns = PathPatterns(patterns=["/.*", "/**/*-stub", "/**/*.pyi"])
    for path in topdir.iterdir():
        if (
            path.is_file()
            and path.name.endswith(".gitignore")
            or path.name.endswith(".ignore")
        ):
            gitignore.load(path)

    if not callable(symlink):

        def symlink(path: str):
            return symlink

    def _filter(tarinfo: tarfile.TarInfo):
        name = tarinfo.name.removeprefix(topdir.name)
        if gitignore.is_match(name):
            return
        path = Path(name)

        if tarinfo.issym():
            realpath = (topdir / name.removeprefix("/")).resolve()
            if not symlink(tarinfo.name, realpath):
                tarinfo = tar.gettarinfo(_os.fspath(realpath), tarinfo.name)

        tarinfo.uid = 0
        tarinfo.gid = 0

        if tarinfo.isdir():
            tarinfo.mode = 0o0755
        else:
            if path.as_posix().startswith("/bin"):
                tarinfo.mode = 0o0755
            else:
                tarinfo.mode = 0o644

        return tarinfo

    with tarfile.open(
        fileobj=fileobj,
        mode="w",
    ) as tar:
        tar.add(topdir.as_posix(), topdir.name, filter=_filter)
    fileobj.seek(0)
    return fileobj.read()


_HIGHBAR_IPS = _ip.ip_network("7.0.0.0/8")


def is_localhost(ip: str):
    return _ip.ip_address(ip).is_loopback


def get_uitc_adapter():
    for adapter in _if.get_adapters():
        for ip_ in adapter.ips:
            ip = ip_.ip
            if ip_.is_IPv6:
                ip = f"{ip[0]}%{ip[2]}"
            interface = _ip.ip_interface((ip, ip_.network_prefix))
            if interface in _HIGHBAR_IPS:
                return adapter


def is_local_ip(ip: str):
    ip = _ip.ip_address(ip)
    if ip.is_loopback:
        return True
    for adapter in _if.get_adapters():
        for ip_ in adapter.ips:
            try:
                if ip == _ip.ip_address(ip_.ip):
                    return True
            except ValueError:
                pass


def get_uitc_ip_interface():
    for adapter in _if.get_adapters():
        for ip_ in adapter.ips:
            ip = ip_.ip
            if ip_.is_IPv6:
                ip = f"{ip[0]}%{ip[2]}"
            interface = _ip.ip_interface((ip, ip_.network_prefix))
            if interface in _HIGHBAR_IPS:
                return interface.ip.exploded




def remote_pytruenas(
    client: "pytruenas.TrueNASClient",
    args: Any,
    logger: _logging.Logger,
    cmd: str,
    *cmd_args: str,
):
    ctx = args.context
    loglevels = args._dump_loglevels()
    logger.info(f"Running {cmd} with options: {cmd_args} on {ctx.fqdn}")
    client.run(
        (
            ctx.exec_path,
            "--loglevel",
            loglevels,
            f"-{(args.verbose or 3)*'v'}",
            cmd,
            *cmd_args,
            "localhost",
        ),
        capture_output=False,
    )
