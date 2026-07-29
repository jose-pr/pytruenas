"""System files whose change some subsystem has to be told about.

The base for units, and useful alone for any file where writing it is only half
the job -- an ``/etc`` file the middleware regenerates, a config a service must
reload to see.
"""

from __future__ import annotations

import logging as _logging
import typing as _ty

from ..templates import FileTarget

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from ...host import TrueNASHost as TrueNASClient

__all__ = ["SystemFile", "as_names"]

LOGGER = _logging.getLogger(__name__)


def as_names(value: "str | _ty.Sequence[str] | None") -> "tuple[str, ...]":
    """Normalize ``None`` / one name / ``"a,b"`` / a sequence to a tuple.

    A bare string is one name, not an iterable of characters -- the mistake
    that turned ``services="nfs"`` into three bogus per-character reloads.
    """
    if not value:
        return ()
    if isinstance(value, str):
        return tuple(part.strip() for part in value.split(",") if part.strip())
    return tuple(value)


class SystemFile(FileTarget):
    """A file on the host, plus what to notify when it changes.

    ``etc`` names middleware ``etc`` groups to regenerate; ``services`` names
    services to reload. Both fire *only* when the write actually changed the
    file, which is what makes applying the same config repeatedly cheap.
    """

    def __init__(
        self,
        path: str,
        client: "TrueNASClient",
        etc: "str | _ty.Sequence[str] | None" = None,
        services: "str | _ty.Sequence[str] | None" = None,
        baseline: bool = True,
        writable: bool = False,
        mode: "int | None" = None,
    ) -> None:
        super().__init__(client.path(path), baseline=baseline, mode=mode)
        self.client = client
        self.etc = as_names(etc)
        self.services = as_names(services)
        #: Clear ``readonly`` on the backing ZFS dataset for the duration of a
        #: write. Off by default: most targets are already writable, and
        #: flipping a dataset is not something to do implicitly. Set it for
        #: anything under ``/usr``, ``/opt`` or another read-only mount --
        #: without it the write fails with a bare ``OSError: Failure``.
        self.writable = writable

    def write(self, content) -> bool:
        if self.writable:
            from ..zfs import writable as _writable

            with _writable(self.client, self.path):
                return self._write_and_notify(content)
        return self._write_and_notify(content)

    def revert(self, remove_baseline: bool = True) -> bool:
        """Restore the original content, then notify as a write would.

        Reverting is a change like any other: a service still holding the
        patched config has to be told, or the file on disk and the running
        state disagree. Wrapped in the same ``writable`` window as a write,
        since the file being restored is usually on a read-only mount.
        """
        if self.writable:
            from ..zfs import writable as _writable

            with _writable(self.client, self.path):
                reverted = super().revert(remove_baseline)
        else:
            reverted = super().revert(remove_baseline)
        if reverted:
            self._notify()
        return reverted

    def _write_and_notify(self, content) -> bool:
        modified = super().write(content)
        if not modified:
            return False
        self._notify()
        return True

    def _notify(self) -> None:
        """Regenerate etc groups and reload services after a real change."""
        if self.etc:
            LOGGER.info("Regenerating etc group(s): %s", ", ".join(self.etc))
            self.client.api.etc.generate(*self.etc)
        for service in self.services:
            LOGGER.info("Reloading service: %s", service)
            self.client.api.service.reload(service)
