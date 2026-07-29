"""Manage systemd units on a TrueNAS host, idempotently.

Renamed from ``ops/midclt.py``, which was a misnomer: ``midclt`` is TrueNAS's
own CLI binary, and nothing here invokes it. What this module actually does is
write unit files and drive ``systemctl``.

Everything is built on :mod:`~pytruenas.ops.template`'s
:class:`~pytruenas.ops.template.FileTarget`, so writes are *conditional*: the
content is compared first, and the expensive follow-up (``daemon-reload``, an
``etc.generate``, a service reload) only happens when the file actually
changed. That is what makes these safe to run repeatedly.

Three layers, each adding one thing:

* :class:`SystemFile` -- a file on the host that some subsystem cares about;
  writing it can regenerate an ``etc`` group or reload services.
* :class:`Unit` -- a systemd unit file, plus ``daemon-reload`` and the
  enable/start state you declared.
* :class:`ServiceUnit` / :class:`MountUnit` / :class:`AutomountUnit` -- the
  section boilerplate for the three unit types worth a shortcut.

Typical use::

    unit = ServiceUnit(nas, "my-agent", cmd="/usr/local/bin/my-agent")
    unit.apply()          # write if changed, reload, enable+start
    ...
    unit.uninstall()      # disable, remove, reload
"""

from __future__ import annotations

import configparser as _configparser
import io as _io
import logging as _logging
import typing as _ty
from pathlib import PurePath as _PurePath

from .template import FileTarget, TextTemplate

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from ..host import TrueNASHost as TrueNASClient

__all__ = [
    "SystemFile",
    "Unit",
    "ServiceUnit",
    "MountUnit",
    "AutomountUnit",
    "MiddlewareFiles",
]

LOGGER = _logging.getLogger(__name__)

#: Where systemd looks for locally-administered units.
UNIT_DIR = "/etc/systemd/system"


class _UnitConfigParser(_configparser.ConfigParser):
    """A ``ConfigParser`` that reads and writes systemd unit syntax.

    Unit files are INI-shaped but not INI: keys are **case-sensitive**
    (``ExecStart``, never ``execstart``), ``=`` is the only delimiter, and
    ``%`` specifiers are systemd's, so the parser's own interpolation has to be
    off or a perfectly valid ``%i`` blows up at write time.
    """

    def __init__(self) -> None:
        super().__init__(
            defaults=None,
            dict_type=dict,
            allow_no_value=False,
            delimiters=("=",),
            comment_prefixes=("#", ";"),
            inline_comment_prefixes=None,
            strict=True,
            empty_lines_in_values=True,
            default_section=None,  # type: ignore[arg-type]
            interpolation=None,
        )

    def optionxform(self, optionstr: str) -> str:
        # The base class lowercases; systemd keys are case-sensitive.
        return optionstr


class SystemFile(FileTarget):
    """A file on the host whose change some subsystem needs to be told about.

    ``etc`` names one or more middleware ``etc`` groups to regenerate, and
    ``services`` names services to reload -- but only if the write actually
    changed the file, which is the whole point of routing through
    :class:`~pytruenas.ops.template.FileTarget`.
    """

    def __init__(
        self,
        path: str,
        client: "TrueNASClient",
        etc: "str | _ty.Sequence[str] | None" = None,
        services: "str | _ty.Sequence[str] | None" = None,
        baseline: bool = True,
    ) -> None:
        super().__init__(client.path(path), baseline=baseline)
        self.client = client
        self.etc = _as_sequence(etc)
        self.services = _as_sequence(services)

    def write(self, content) -> bool:
        modified = super().write(content)
        if not modified:
            return False
        if self.etc:
            LOGGER.info("Regenerating etc group(s): %s", ", ".join(self.etc))
            self.client.api.etc.generate(*self.etc)
        for service in self.services:
            LOGGER.info("Reloading service: %s", service)
            self.client.api.service.reload(service)
        return True


def _as_sequence(value: "str | _ty.Sequence[str] | None") -> "tuple[str, ...]":
    """Normalize ``None`` / one name / a comma list / a sequence to a tuple.

    A bare string is one name, not an iterable of characters -- the mistake
    that turns ``services="nfs"`` into four bogus reloads.
    """
    if not value:
        return ()
    if isinstance(value, str):
        return tuple(part.strip() for part in value.split(",") if part.strip())
    return tuple(value)


class Unit(SystemFile):
    """A systemd unit file, with its reload and enable/start state.

    ``enable`` and ``start`` are *declared* state, reconciled on every
    :meth:`apply`: ``True`` means "make it so", ``False`` means "make sure it
    is not", and ``None`` means "leave whatever is there alone" -- which is not
    the same as ``False`` and was not expressible before.
    """

    #: Unit-file suffix for this class; subclasses override.
    SUFFIX = ".service"

    def __init__(
        self,
        client: "TrueNASClient",
        name: str,
        description: str = "",
        enable: "bool | None" = True,
        start: "bool | None" = True,
        *,
        after: str = "network.target auditd.service",
        wantedby: str = "multi-user.target",
        conf: "dict[str, dict] | None" = None,
    ) -> None:
        self.name = name if "." in name else f"{name}{self.SUFFIX}"
        self.enable = enable
        self.start = start

        self.conf: "dict[str, dict]" = conf or {}
        unit = self.conf.setdefault("Unit", {})
        unit["Description"] = description or self.name.rsplit(".", 1)[0].upper()
        if after:
            unit["After"] = after
        if wantedby:
            self.conf.setdefault("Install", {})["WantedBy"] = wantedby

        # baseline=False: a unit file this code owns has no pre-existing
        # version worth preserving, unlike an /etc file shipped by the OS.
        super().__init__(f"{UNIT_DIR}/{self.name}", client, baseline=False)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name})"

    # -- rendering ---------------------------------------------------------

    def render(self) -> str:
        """The unit file's text, from :attr:`conf`."""
        parser = _UnitConfigParser()
        parser.read_dict(self.conf)
        stream = _io.StringIO()
        parser.write(stream)
        return stream.getvalue()

    def template(self) -> TextTemplate:
        return TextTemplate(self.render())

    def apply(self) -> bool:
        """Write the unit if it changed, then reconcile enable/start state."""
        return self.template().apply(self)

    # -- systemctl ---------------------------------------------------------

    def _systemctl(self, command: str, *args: str, unit_action: bool = True):
        """Run one ``systemctl`` invocation as a single argv.

        argv, not a shell string: a unit name can contain characters a shell
        would reinterpret (a mount unit's name is full of ``-`` and ``\\x2d``
        escapes), and hand-quoting them was a latent bug. ``is-*`` queries use
        their exit code as the answer, so they must not raise on non-zero.
        """
        argv = ["systemctl", command]
        if unit_action:
            argv.append(self.name)
        argv.extend(args)
        return self.client.run(argv, check=not command.startswith("is-"))

    def is_active(self) -> bool:
        return self._systemctl("is-active").returncode == 0

    def is_enabled(self) -> bool:
        return self._systemctl("is-enabled").returncode == 0

    def configure(self) -> None:
        """Bring enable/start into the state this unit declares."""
        if self.enable is not None:
            enabled = self.is_enabled()
            if self.enable and not enabled:
                LOGGER.info("Enabling %s", self.name)
                self._systemctl("enable")
            elif not self.enable and enabled:
                LOGGER.info("Disabling %s", self.name)
                self._systemctl("disable")

        if self.start is not None:
            active = self.is_active()
            if self.start and not active:
                LOGGER.info("Starting %s", self.name)
                self._systemctl("start")
            elif not self.start and active:
                LOGGER.info("Stopping %s", self.name)
                self._systemctl("stop")

    def write(self, content) -> bool:
        modified = super().write(content)
        if modified:
            LOGGER.info("Reloading systemd for %s", self.name)
            self._systemctl("daemon-reload", unit_action=False)
        self.configure()
        return modified

    def uninstall(self) -> bool:
        """Disable, stop, remove the unit file, and reload. Returns whether it existed."""
        if not self.path.exists():
            return False
        LOGGER.info("Removing %s", self.name)
        self._systemctl("disable", "--now")
        self.path.unlink(missing_ok=True)
        self._systemctl("daemon-reload", unit_action=False)
        return True

    def escape(self, text: str) -> str:
        """``systemd-escape`` ``text`` on the host (path names -> unit names)."""
        result = self.client.run(
            ["systemd-escape", text], capture_output="stdout", encoding="utf-8"
        )
        return result.stdout.strip()


class ServiceUnit(Unit):
    """A ``.service`` unit running ``cmd``."""

    SUFFIX = ".service"

    def __init__(
        self,
        client: "TrueNASClient",
        name: str,
        cmd: "str | _PurePath | None" = None,
        **kwargs,
    ) -> None:
        super().__init__(client, name, **kwargs)
        command = cmd if cmd is not None else name
        if isinstance(command, _PurePath):
            command = command.as_posix()
        service = self.conf.setdefault("Service", {})
        service["ExecStart"] = str(command)
        service.setdefault("Restart", "always")
        service.setdefault("RestartSec", "10")


class MountUnit(Unit):
    """A ``.mount`` unit. Its name is derived from ``where`` via systemd-escape."""

    SUFFIX = ".mount"

    def __init__(
        self,
        client: "TrueNASClient",
        where: "str | _PurePath",
        what: str,
        options: str = "",
        type: str = "",
        **kwargs,
    ) -> None:
        if isinstance(where, _PurePath):
            where = where.as_posix()
        # The name must be escaped BEFORE super().__init__, which uses it to
        # build the path -- so escaping cannot go through self.escape() (no
        # client yet). Hence the module-level helper taking the client.
        name = _escape_path(client, where)
        super().__init__(client, f"{name}{self.SUFFIX}", **kwargs)
        mount = self.conf.setdefault("Mount", {})
        mount.update({"What": what, "Where": where})
        if options:
            mount["Options"] = options
        if type:
            mount["Type"] = type


class AutomountUnit(Unit):
    """An ``.automount`` unit for ``where``, idle-unmounting after ``timeout``."""

    SUFFIX = ".automount"

    def __init__(
        self,
        client: "TrueNASClient",
        where: "str | _PurePath",
        timeout: str = "60",
        **kwargs,
    ) -> None:
        if isinstance(where, _PurePath):
            where = where.as_posix()
        name = _escape_path(client, where)
        super().__init__(client, f"{name}{self.SUFFIX}", **kwargs)
        self.conf.setdefault("Automount", {}).update(
            {"Where": where, "TimeoutIdleSec": timeout}
        )


def _escape_path(client: "TrueNASClient", path: str) -> str:
    """A filesystem path as a systemd unit name (``/mnt/x`` -> ``mnt-x``).

    Uses the host's own ``systemd-escape`` rather than reimplementing the
    escaping rules, which are fiddly (``-`` becomes ``\\x2d``, and so on).
    """
    result = client.run(
        ["systemd-escape", "--path", path], capture_output="stdout", encoding="utf-8"
    )
    return result.stdout.strip().lstrip("-")


class MiddlewareFiles:
    """Locate files inside the installed ``middlewared`` package on a host.

    Mostly for reaching the stock ``etc_files`` templates so a deployment can
    take one as its baseline and layer changes onto it, instead of writing a
    config from scratch and losing whatever the middleware generates.
    """

    #: Where ``etc_files`` templates live, relative to the middlewared package.
    TEMPLATE_DIRS = ("etc_files", "etc_files/local")

    def __init__(
        self, client: "TrueNASClient | None" = None, module_path: "str | None" = None
    ) -> None:
        from ..host import TrueNASHost

        self.client = client if client is not None else TrueNASHost()
        self.module_path = (
            self.client.path(module_path)
            if module_path is not None
            else self.client.middlewared_path
        )

    def find_template(
        self,
        template: str,
        etc: "str | _ty.Sequence[str] | None" = None,
        services: "str | _ty.Sequence[str] | None" = None,
    ) -> SystemFile:
        """Find an ``etc_files`` template by name, with or without ``.mako``."""
        for directory in self.TEMPLATE_DIRS:
            base = self.module_path / directory / template
            candidates = [base]
            if base.suffix != ".mako":
                candidates.append(base.with_name(base.name + ".mako"))
            for candidate in candidates:
                try:
                    return self.find_file(candidate, etc=etc, services=services)
                except FileNotFoundError:
                    continue
        raise FileNotFoundError(
            f"no template {template!r} under "
            f"{'/'.join(str(self.module_path / d) for d in self.TEMPLATE_DIRS)}"
        )

    def find_file(
        self, path, *args, cls: "type[SystemFile] | None" = None, **kwargs
    ) -> SystemFile:
        """Wrap an existing file under the middlewared package as a target."""
        resolved = self.module_path / path
        baseline = resolved.with_name(resolved.name + ".baseline")
        if not resolved.exists() and not baseline.exists():
            raise FileNotFoundError(str(resolved))
        return (cls or SystemFile)(str(resolved), self.client, *args, **kwargs)
