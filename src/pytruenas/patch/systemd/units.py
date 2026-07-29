"""Systemd units: write the file, reload, and reconcile enable/start state.

Applying a unit is idempotent by construction. The file is written through a
:class:`~pytruenas.patch.templates.FileTarget`, so ``daemon-reload`` runs only
when the content actually changed, and enable/start are *declared* state
reconciled against what the host reports rather than commands fired blindly.
"""

from __future__ import annotations

import logging as _logging
import typing as _ty
from pathlib import PurePath as _PurePath

from ..templates import TextTemplate
from .files import SystemFile
from .unitfile import render_unit

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from ...host import TrueNASHost as TrueNASClient

__all__ = ["Unit", "ServiceUnit", "MountUnit", "AutomountUnit", "escape_path"]

LOGGER = _logging.getLogger(__name__)

#: Where locally-administered units live. ``/lib`` and ``/usr/lib`` are the
#: distribution's; anything written by this code belongs here, where it also
#: takes precedence.
UNIT_DIR = "/etc/systemd/system"


def escape_path(client: "TrueNASClient", path: str) -> str:
    """A filesystem path as a systemd unit name (``/mnt/x`` -> ``mnt-x``).

    Delegated to the host's own ``systemd-escape`` rather than reimplemented:
    the rules are fiddly (``-`` becomes ``\\x2d``, non-ASCII is hex-escaped)
    and getting them subtly wrong produces a unit systemd will not match to the
    mount point it names.
    """
    result = client.run(
        ["systemd-escape", "--path", path], capture_output="stdout", encoding="utf-8"
    )
    return result.stdout.strip().lstrip("-")


class Unit(SystemFile):
    """A systemd unit file plus the state it should be in.

    ``enable`` and ``start`` are three-valued: ``True`` means "make it so",
    ``False`` means "make sure it is not", and ``None`` means "leave whatever
    is there alone" -- a distinction a plain bool could not express, and the
    one you want when a unit's running state is managed elsewhere.
    """

    #: Suffix appended when ``name`` carries none. Overridden per unit type.
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

        self.conf: "dict[str, dict]" = conf if conf is not None else {}
        unit = self.conf.setdefault("Unit", {})
        unit.setdefault(
            "Description", description or self.name.rsplit(".", 1)[0].upper()
        )
        if after:
            unit.setdefault("After", after)
        if wantedby:
            self.conf.setdefault("Install", {}).setdefault("WantedBy", wantedby)

        # baseline=False: a unit this code owns has no prior version worth
        # preserving, unlike a distribution-shipped /etc file.
        super().__init__(f"{UNIT_DIR}/{self.name}", client, baseline=False)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name})"

    # -- rendering ---------------------------------------------------------

    def render(self) -> str:
        """The unit file's text."""
        return render_unit(self.conf)

    def template(self) -> TextTemplate:
        return TextTemplate(self.render())

    def apply(self) -> bool:
        """Write the unit if it changed, reload, and reconcile enable/start."""
        return self.template().apply(self)

    # -- systemctl ---------------------------------------------------------

    def _systemctl(self, command: str, *args: str, unit_action: bool = True):
        """Run one ``systemctl`` invocation as a single argv.

        A list, not a shell string: ``run()`` takes ``*cmds`` where each
        positional is a *separate command*, so passing the words individually
        ran four commands instead of one. Unit names also contain characters a
        shell would reinterpret -- a mount unit's name is full of ``\\x2d``
        escapes -- which hand-quoting got wrong.

        ``is-*`` queries answer through their exit code, so they must not raise
        on non-zero; that is the normal "no" case.
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

    def daemon_reload(self) -> None:
        self._systemctl("daemon-reload", unit_action=False)

    def configure(self) -> None:
        """Bring enable/start into the declared state, querying first."""
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

    def restart(self) -> None:
        self._systemctl("restart")

    def write(self, content) -> bool:
        modified = super().write(content)
        if modified:
            LOGGER.info("Reloading systemd for %s", self.name)
            self.daemon_reload()
        self.configure()
        return modified

    def uninstall(self) -> bool:
        """Disable, stop, remove, reload. Returns whether the unit existed."""
        if not self.path.exists():
            return False
        LOGGER.info("Removing %s", self.name)
        self._systemctl("disable", "--now")
        self.path.unlink(missing_ok=True)
        self.daemon_reload()
        return True

    def escape(self, text: str) -> str:
        """``systemd-escape`` ``text`` on the host."""
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
        service.setdefault("ExecStart", str(command))
        service.setdefault("Restart", "always")
        service.setdefault("RestartSec", "10")


class MountUnit(Unit):
    """A ``.mount`` unit; its name is derived from ``where``."""

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
        # Escaping must happen before super().__init__, which builds the path
        # from the name -- so it takes the client rather than using self.escape.
        name = escape_path(client, where)
        super().__init__(client, f"{name}{self.SUFFIX}", **kwargs)
        mount = self.conf.setdefault("Mount", {})
        mount.update({"What": what, "Where": where})
        # Omitted rather than emitted empty: `Options=` with no value is not
        # the same as no Options line, and systemd treats it as such.
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
        name = escape_path(client, where)
        super().__init__(client, f"{name}{self.SUFFIX}", **kwargs)
        self.conf.setdefault("Automount", {}).update(
            {"Where": where, "TimeoutIdleSec": timeout}
        )
