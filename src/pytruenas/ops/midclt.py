from pathlib import PurePath
import logging as _logging
import configparser as _confparse
import io as _io

from pytruenas import TrueNASClient

LOGGER = _logging.getLogger()

from .template import FileTarget, TextTemplate


class _SystemdConfigParser(_confparse.ConfigParser):
    def __init__(self):
        super().__init__(
            defaults=None,
            dict_type=dict,
            allow_no_value=False,
            delimiters=("=",),
            comment_prefixes=("#", ";"),
            inline_comment_prefixes=None,
            strict=True,
            empty_lines_in_values=True,
            default_section=None,
            interpolation=None,
        )

    def optionxform(self, optionstr):
        return optionstr


class TruenasSystemFile(FileTarget):
    def __init__(
        self,
        path,
        client: TrueNASClient,
        etc: str = None,
        services: list[str] = None,
        baseline=True,
    ):
        super().__init__(client.path(path), baseline=baseline)
        self.services = services or []
        if isinstance(self.services, str):
            self.services = self.services.split(",")
        self.client = client
        self.etc = etc

    def write(self, content):
        modified = super().write(content)
        if modified:
            if self.etc:
                if isinstance(self.etc, (list,tuple)):
                    etc = self.etc
                else:
                    etc = (self.etc,)
                LOGGER.info(f"Reloading etc group: {etc}")
                self.client.api.etc.generate(*etc)
            for service in self.services:
                LOGGER.info(f"Reloading service: {service}")
                self.client.api.service.reload(service)
        return modified


class SystemdUnit(TruenasSystemFile):
    def __init__(
        self,
        client: TrueNASClient,
        name: str,
        desc="",
        enable=True,
        start=True,
        *,
        after="network.target auditd.service",
        wantedby="multi-user.target",
        conf: "dict[str, dict] | None" = None,
    ) -> None:
        if "." not in name:
            name = name + ".service"
        self.name = name
        desc = desc or self.name.split(".")[0].upper()
        self.enable = enable
        self.start = start
        self.after = after

        self.conf = conf or {}
        unit = self.conf.setdefault("Unit", {})
        install = self.conf.setdefault("Install", {})
        unit.update({"Description": desc})
        if after:
            unit["After"] = after
        if wantedby:
            install.update({"WantedBy": wantedby})
        super().__init__(f"/etc/systemd/system/{self.name}", client, baseline=False)

    def uninstall(self):
        if self.path.exists():
            self.client.run("systemctl", "disable", "--now", f"'{self.name}'")
            self.path.unlink(True)
            self.client.run(["systemctl", "daemon-reload"])

    def _unit(self):
        conf = _SystemdConfigParser()
        conf.read_dict(self.conf)
        stream = _io.StringIO()
        conf.write(stream)
        stream.seek(0)
        return stream.read()

    def template(self):
        return TextTemplate(self._unit())

    def _escape(self, text: str):
        return (
            self.client.run(("systemd-escape", text), capture_output=True)
            .stdout.decode()
            .strip()
        )

    def apply(self):
        return self.template().apply(self)

    def _systemctl(self, cmd: str, *args, unit_action=True, **kwargs):
        raise_ = not cmd.startswith("is-")
        if unit_action:
            args = [f"{self.name}", *args]
        return self.client.run(
            ("systemctl", cmd, *args), check=raise_, capture_output=True, **kwargs
        )

    def configure(self):
        active = self._systemctl("is-active").returncode == 0
        enabled = self._systemctl("is-enabled").returncode == 0
        if self.enable and not enabled:
            self._systemctl("enable")
        elif self.enable is False and enabled:
            self._systemctl("disable")
        if self.start and not active:
            self._systemctl("start")
        elif self.start is False and active:
            self._systemctl("stop")

    def write(self, content) -> bool:
        modified = super().write(content)
        if modified:
            self._systemctl("daemon-reload", unit_action=False)
        self.configure()
        return modified


class SystemdServiceUnit(SystemdUnit):
    def __init__(
        self, client: TrueNASClient, name: str, cmd: str = None, **unitkwargs
    ) -> None:
        super().__init__(client, name + ".service", **unitkwargs)
        cmd = cmd or name
        cmd = cmd.as_posix() if isinstance(cmd, PurePath) else str(cmd)
        service = self.conf.setdefault("Service", {})
        service.update({"ExecStart": cmd})
        service.setdefault("Restart", "always")
        service.setdefault("RestartSec", 10)


class SystemdMountUnit(SystemdUnit):
    def __init__(
        self,
        client: TrueNASClient,
        where: str,
        what: str,
        options: str,
        type: str,
        **unitkwargs,
    ) -> None:
        self.client = client
        if isinstance(where, PurePath):
            where = where.as_posix()
        name = self._escape(where).lstrip("-")
        super().__init__(client, name + ".mount", **unitkwargs)

        mount = self.conf.setdefault("Mount", {})
        mount.update({"What": what, "Where": where, "Options": options, "Type": type})


class SystemdAutoMountUnit(SystemdUnit):
    def __init__(
        self, client: TrueNASClient, where: str, timeout: str, **unitkwargs
    ) -> None:
        self.client = client
        name = self._escape(where).lstrip("-")
        super().__init__(client, name + ".automount", **unitkwargs)

        mount = self.conf.setdefault("Automount", {})
        mount.update({"Where": where, "TimeoutIdleSec": timeout})


class MiddlewareCode:
    def __init__(self, client: TrueNASClient = None, module_path: str = None) -> None:
        if not client:
            self.client = TrueNASClient()
        else:
            self.client = client
        if module_path is None:
            self.module_path = self.client.middlewared_path
        else:
            self.module_path = client.path(module_path)

    def find_template(
        self, template: str, etc: str = None, services=None
    ) -> TruenasSystemFile:
        for path in ["etc_files", "etc_files/local"]:
            path = self.module_path / path / template
            mako = (
                path if path.suffix == ".mako" else path.with_name(path.name + ".mako")
            )
            for path in [path, mako]:
                try:
                    return self.find_module_file(path, etc=etc, services=services)
                except FileNotFoundError:
                    continue
        raise FileNotFoundError(template)

    def find_module_file(
        self, path: str, *args, cls: TruenasSystemFile = None, **kwargs
    ) -> TruenasSystemFile:
        _path = self.module_path / path
        cls = cls or TruenasSystemFile
        if _path.exists() or _path.with_name(_path.name + ".baseline").exists():
            return cls(_path, self.client, *args, **kwargs)
        else:
            raise FileNotFoundError(_path)
