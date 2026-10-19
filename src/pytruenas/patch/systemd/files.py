"""System files whose change some subsystem has to be told about.

The base for units, and useful alone for any file where writing it is only half
the job -- an ``/etc`` file the middleware regenerates, a config a service must
reload to see.
"""

from __future__ import annotations

import contextlib as _contextlib
import logging as _logging
import typing as _ty

from ..templates import FileTarget

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from ...host import TrueNASHost as TrueNASClient

__all__ = ["SystemFile", "as_names"]

LOGGER = _logging.getLogger(__name__)


def as_names(value: "str | _ty.Sequence[str] | None") -> "tuple[str, ...]":
    """Normalize ``None`` / one name / ``"a,b"`` / a sequence to a tuple.

    A bare string is one name (or a comma-separated list), never an iterable
    of characters: ``services="nfs"`` is one service.
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
        """Write ``content`` if it differs, then notify; return whether it did.

        With ``writable``, an unchanged file is detected before the dataset is
        touched, so re-applying a patch toggles nothing. If notifying fails,
        the previous content is put back before the error is raised: the next
        apply then sees a change and notifies again, instead of finding the
        file already written and doing nothing.
        """
        if self.writable and not self.would_change(content):
            return False
        with self._window():
            changed, previous = self._write(content)
        if changed:
            self._follow_up(previous)
        return changed

    def revert(self, remove_baseline: bool = True) -> bool:
        """Restore the original content, then notify as a write would.

        Reverting is a change like any other: a service still holding the
        patched config has to be told, or the file on disk and the running
        state disagree. Done in the same ``writable`` window as a write, since
        the file being restored is usually on a read-only mount. The snapshot
        is removed only once notifying succeeded, so a failed revert can be
        retried.
        """
        with self._window():
            previous = self._current()
            reverted = super().revert(remove_baseline=False)
            if not reverted and remove_baseline:
                super().revert(remove_baseline=True)
        if reverted:
            self._follow_up(previous)
            if remove_baseline:
                with self._window():
                    super().revert(remove_baseline=True)
        return reverted

    def _window(self):
        """The ``zfs.writable`` window when ``writable`` is set, else nothing."""
        if not self.writable:
            return _contextlib.nullcontext()
        from ..zfs import writable as _writable

        return _writable(self.client, self.path)

    def _follow_up(self, previous: "bytes | None") -> None:
        """Notify after a change; on failure, put ``previous`` back and raise."""
        try:
            self._notify()
        except Exception:
            LOGGER.error(
                "%s changed but notifying failed; putting the previous content "
                "back so the next apply retries",
                self.path,
            )
            try:
                with self._window():
                    if previous is None:
                        self._unlink(self.path)
                    else:
                        self._write_with_mode(
                            self.path, previous, self._mode_of(self.path), exists=True
                        )
            except Exception:
                LOGGER.exception("could not put back the content of %s", self.path)
            raise

    def _notify(self) -> None:
        """Regenerate etc groups and reload services after a real change."""
        # One call per group: `etc.generate(name, checkpoint=None)` reads a
        # second positional as its checkpoint, not as another group.
        for group in self.etc:
            LOGGER.info("Regenerating etc group: %s", group)
            self.client.api.etc.generate(group)
        for service in self.services:
            LOGGER.info("Reloading service: %s", service)
            self.client.api.service.reload(service)
