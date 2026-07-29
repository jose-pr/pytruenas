"""Modify a TrueNAS host beyond what the middleware API exposes.

**This is unsupported territory, by definition.** TrueNAS is an appliance: its
configuration is owned by the middleware, ``/`` is read-only, and a boot
environment swap on update discards anything written outside the persistent
datasets. Everything here writes files and drives services the appliance
believes it owns. Sometimes that is the only way to get a thing done -- a
systemd unit for a daemon TrueNAS has no concept of, an ``/etc`` file carrying
a setting the UI does not expose -- and that is what this package is for. It is
still not a supported configuration, and an update can undo any of it.

Given that, the design goal is to be *undoable and repeatable*:

* **Baselines.** A :class:`~pytruenas.patch.templates.FileTarget` snapshots the
  original before its first change and templates from that snapshot ever after.
  So a patch layers onto what TrueNAS generates rather than onto its own
  previous output, and the original is still on disk to restore.
* **Undo.** ``revert()`` puts the original back and clears the snapshot;
  ``Unit.uninstall()`` does the same for a unit (disable, remove, reload). A
  file this code *created* is deliberately left alone -- there is no baseline
  to prove it was ours to delete.
* **Change detection.** Writes compare content first and report whether
  anything changed; the expensive follow-up (``daemon-reload``,
  ``etc.generate``, a service reload) runs only when it did. Applying the same
  patch twice does the work once. ``would_change()`` answers the same question
  without writing, and ``is_patched()`` reports whether a file currently
  differs from its baseline.
* **Permissions survive.** A rewrite preserves the file's existing mode --
  silently widening ``/etc/shadow`` from ``0640`` to whatever the umask gives
  is a security regression, not a cosmetic one. ``mode=`` sets the mode for a
  file the patch *creates*.
* **Declared state.** A unit's enable/start is reconciled against what the host
  reports, and is three-valued -- ``None`` means "not mine to manage".

Contents:

* :mod:`.templates` -- render content, apply it to a target, only when changed.
* :mod:`.systemd` -- unit files and ``systemctl``.
* :mod:`.middleware` -- locate files inside the host's ``middlewared`` package,
  chiefly to take a stock ``etc_files`` template as a baseline.
* :mod:`.zfs` -- :func:`~.zfs.writable`, which clears ``readonly`` on the
  dataset holding a path and restores it afterwards. Needed for anything under
  ``/usr``, and the reason a patch there is possible at all.

Renamed from ``pytruenas.ops``, which said nothing about what the code does or
what it costs you.
"""

from .middleware import MiddlewareFiles, middlewared_path
from .systemd import AutomountUnit, MountUnit, ServiceUnit, SystemFile, Unit
from .templates import (
    BaseTemplate,
    BasicTemplate,
    FileTarget,
    TemplateTarget,
    TextTemplate,
    render_basic_template,
)
from .zfs import dataset_for, writable

__all__ = [
    # templates
    "BaseTemplate",
    "BasicTemplate",
    "TextTemplate",
    "render_basic_template",
    "FileTarget",
    "TemplateTarget",
    # systemd
    "SystemFile",
    "Unit",
    "ServiceUnit",
    "MountUnit",
    "AutomountUnit",
    # middleware
    "MiddlewareFiles",
    "middlewared_path",
    # zfs
    "writable",
    "dataset_for",
]
