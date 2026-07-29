"""Systemd units and system files, applied idempotently.

* :mod:`.unitfile` -- unit-file syntax. Pure text: parse and render systemd's
  INI-shaped format, with the three deviations from real INI handled.
* :mod:`.files` -- :class:`~.files.SystemFile`, a file plus the etc groups and
  services to notify when it changes.
* :mod:`.units` -- :class:`~.units.Unit` and the service/mount/automount
  shortcuts: write the file, ``daemon-reload``, reconcile enable/start.

Typical use::

    unit = ServiceUnit(nas, "my-agent", cmd="/usr/local/bin/my-agent")
    unit.apply()          # write if changed, reload, enable + start
    ...
    unit.uninstall()      # disable, remove, reload

Was ``ops/midclt.py`` -- a misnomer, since ``midclt`` is TrueNAS's own CLI
binary and nothing here invokes it.
"""

from .files import SystemFile, as_names
from .unitfile import UnitConfigParser, parse_unit, render_unit
from .units import (
    UNIT_DIR,
    AutomountUnit,
    MountUnit,
    ServiceUnit,
    Unit,
    escape_path,
)

__all__ = [
    "SystemFile",
    "as_names",
    "UnitConfigParser",
    "render_unit",
    "parse_unit",
    "Unit",
    "ServiceUnit",
    "MountUnit",
    "AutomountUnit",
    "escape_path",
    "UNIT_DIR",
]
