"""Where rendered content goes, and how "did it change?" is decided.

A target owns two things a template does not: reading whatever is already
there, and writing only when the new content differs. That comparison is the
whole basis of idempotence in :mod:`pytruenas.patch` -- every caller decides
whether to reload a service or regenerate an etc group from the boolean
``write`` returns.
"""

from __future__ import annotations

import logging as _logging
import stat as _stat
import typing as _ty
from pathlib import Path as _LocalPath

from .base import BaseTemplate, TextTemplate

__all__ = ["TemplateTarget", "FileTarget"]

LOGGER = _logging.getLogger(__name__)

#: Mode for directories created on the way to a target. Octal, and stated as
#: such: the previous code passed a bare ``755``, which Python reads as decimal
#: -- ``0o1363``, i.e. setuid plus the wrong permission bits.
DIRECTORY_MODE = 0o755

#: Methods a path-like must provide to be usable as a :class:`FileTarget`.
_REQUIRED_PATH_METHODS = ("exists", "read_bytes", "write_bytes", "with_name")


class TemplateTarget:
    """Something a template can be written to."""

    def read(self) -> bytes:
        """The content to template *from*. May raise ``FileNotFoundError``."""
        raise NotImplementedError

    def write(self, content: "str | bytes") -> bool:
        """Store ``content``; return whether it differed from what was there."""
        raise NotImplementedError

    def apply_template(
        self,
        template: "BaseTemplate | str | type | _LocalPath",
        context: object = None,
        **kwargs,
    ) -> bool:
        """Render ``template`` onto this target; return whether it changed.

        ``template`` may be:

        * a :class:`~pytruenas.patch.templates.base.BaseTemplate` instance -- used
          as-is;
        * a ``BaseTemplate`` *subclass* -- instantiated with this target's
          current content, so the template layers onto what is already there
          (an absent target gives an empty baseline rather than an error);
        * a ``str`` -- the literal template text;
        * anything else path-like -- read from the LOCAL filesystem.

        ``kwargs`` reach the template's constructor, which is why the class and
        the path forms accept them and a ready instance does not.
        """
        if isinstance(template, type) and issubclass(template, BaseTemplate):
            try:
                baseline = self.read()
            except FileNotFoundError:
                baseline = b""
            template = template(baseline, **kwargs)
        elif isinstance(template, BaseTemplate):
            if kwargs:
                # Silently dropping these would leave the caller wondering why
                # their option had no effect on an already-built template.
                raise TypeError(
                    "kwargs are not accepted with an already-constructed "
                    f"template ({type(template).__name__}); pass them where it "
                    "is built"
                )
        elif isinstance(template, str):
            template = TextTemplate(template, **kwargs)
        else:
            template = TextTemplate(
                _LocalPath(template).read_text(encoding="utf-8"), **kwargs
            )

        return template.apply(self, context)


class FileTarget(TemplateTarget):
    """A file, optionally with a baseline snapshot of its original content.

    With ``baseline`` set, the first write copies the existing file aside
    (``<name>.baseline`` by default) and :meth:`read` returns *that* rather
    than the current content. This is what makes repeated application
    idempotent: a template that layers changes onto a stock config always sees
    the stock config, not its own previous output.
    """

    def __init__(
        self,
        path,
        baseline: "bool | str" = False,
        mode: "int | None" = None,
    ) -> None:
        # Duck-typed rather than `isinstance(path, pathlib_next.Path)`: this
        # class only calls the methods below, and demanding one concrete type
        # rejected valid stand-ins (a test double, another backend's path) for
        # no benefit. The error still fires early, and names what is missing.
        missing = [
            attribute
            for attribute in _REQUIRED_PATH_METHODS
            if not callable(getattr(path, attribute, None))
        ]
        if missing:
            raise TypeError(f"{path!r} is not path-like: missing {', '.join(missing)}")
        self.path = path
        if baseline is True:
            baseline = ".baseline"
        self._baseline = str(baseline or "")
        #: Mode for a file this target CREATES. An existing file keeps its own
        #: mode across a rewrite regardless -- see :meth:`write`. ``None``
        #: leaves a new file at whatever the backend/umask produces.
        self.mode = mode

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.path})"

    @property
    def baseline_path(self):
        """Where the baseline snapshot lives, or ``None`` if not using one."""
        if not self._baseline:
            return None
        return self.path.with_name(self.path.name + self._baseline)

    @property
    def _absent_marker(self):
        """Marks that the file did not exist when this target first wrote it.

        Without it, the second write found "an existing file with no baseline"
        -- this target's own output -- and snapshotted it as the original, so
        layering templates duplicated their additions and ``revert()`` restored
        patched content.
        """
        if not self._baseline:
            return None
        return self.path.with_name(self.path.name + self._baseline + ".absent")

    def baseline(self):
        """Return the baseline path, creating the snapshot if it is missing.

        A target that does not exist yet has nothing to snapshot -- that is the
        ordinary "create this file if absent" case, and it must not fail; it is
        recorded with an ``.absent`` marker instead, so later writes and
        ``revert()`` know the original was absent. The snapshot keeps the
        original's permission bits: a copy of ``/etc/shadow`` must not be
        world-readable.
        """
        baseline = self.baseline_path
        if baseline is None:
            return self.path
        if baseline.exists() or self._absent_marker.exists():
            return baseline
        if not self.path.exists():
            self._absent_marker.write_bytes(b"")
            return baseline
        # Guard against an empty suffix, which would make the "baseline" the
        # target itself and truncate the file it exists to preserve. Compared
        # as strings rather than via resolve(): not every path backend has
        # resolve() (hostctl's CompositePosixPath does not), and a suffix that
        # is empty is the only way these can collide anyway.
        if str(baseline) == str(self.path):
            return self.path
        LOGGER.info("Snapshotting %s -> %s", self.path, baseline)
        self._write_with_mode(
            baseline, self.path.read_bytes(), self._mode_of(self.path)
        )
        return baseline

    def read(self) -> bytes:
        """The content to template FROM: the baseline if one exists, else the file.

        **Never creates the snapshot.** Taking it is :meth:`write`'s job, and
        doing it here made reading a mutating operation -- which fails outright
        on a read-only mount (the middlewared package ships on one; see
        :meth:`pytruenas.patch.middleware.MiddlewareFiles.find_template`). That
        turned ``baseline=True`` into "cannot even read this file", which is
        why the middleware helper used to default it off.

        Snapshotting at write time is also the correct moment on its own terms:
        the mount must be writable by then anyway, and a caller who only reads
        has changed nothing that needs undoing.

        With no snapshot yet, the file's CURRENT content is the right answer --
        nothing has displaced it, so it is still its own original.
        """
        if self._baseline:
            baseline = self.baseline_path
            if baseline is not None and baseline.exists():
                return baseline.read_bytes()
            if self._absent_marker.exists():
                # The original was absent: template from nothing, not from
                # this target's own earlier output.
                raise FileNotFoundError(str(self.path))
        if not self.path.exists():
            # No original to template from: distinguishing this from an empty
            # file is the caller's job (`apply_template` treats it as empty).
            raise FileNotFoundError(str(self.path))
        return self.path.read_bytes()

    # -- inspection and undo ----------------------------------------------

    def is_patched(self) -> bool:
        """Whether the file currently differs from its baseline.

        ``False`` when there is no snapshot to compare against -- this target
        keeps no baseline, or the file did not exist when it was first written
        (nothing was displaced). A snapshotted file is patched while its
        content differs, including when it has been deleted.
        """
        baseline = self.baseline_path
        if baseline is None or not baseline.exists():
            return False
        if not self.path.exists():
            return True
        return self.path.read_bytes() != baseline.read_bytes()

    def would_change(self, content: "str | bytes") -> bool:
        """Whether writing ``content`` would modify the file. No side effects.

        The dry-run half of :meth:`write`. Without it the only way to find out
        was to perform the write, which is the wrong tool for "show me what
        this patch would do".
        """
        if isinstance(content, str):
            content = content.encode()
        if not self.path.exists():
            return True
        return self.path.read_bytes() != content

    def revert(self, remove_baseline: bool = True) -> bool:
        """Restore the original content. Returns whether anything changed.

        The counterpart the baseline mechanism exists for. Cases:

        * a snapshot exists -> its content (and permission bits) are written
          back, and (by default) the snapshot is removed, so the target is left
          exactly as found;
        * this target created the file -> the file is left in place (not ours
          to delete) and returns ``False``; by default its ``.absent`` marker
          is removed;
        * baseline configured but never taken, or no baseline -> a no-op.

        ``remove_baseline=False`` keeps the snapshot or marker, for reverting a
        patch you intend to re-apply.
        """
        baseline = self.baseline_path
        if baseline is None:
            return False
        marker = self._absent_marker
        if marker.exists():
            if remove_baseline:
                self._unlink(marker)
            return False
        if not baseline.exists():
            LOGGER.debug("Nothing to revert for %s (no baseline)", self.path)
            return False

        original = baseline.read_bytes()
        changed = not self.path.exists() or self.path.read_bytes() != original
        if changed:
            LOGGER.info("Reverting %s to its baseline", self.path)
            self._write_with_mode(self.path, original, self._mode_of(baseline))
        if remove_baseline:
            self._unlink(baseline)
        return changed

    def _unlink(self, path) -> None:
        unlink = getattr(path, "unlink", None)
        if callable(unlink):
            unlink(missing_ok=True)
        else:
            # Not in _REQUIRED_PATH_METHODS, because only revert() needs it: a
            # backend that cannot delete should still be able to patch and to
            # restore content.
            LOGGER.warning(
                "cannot remove %s (backend has no unlink); it is left in place", path
            )

    def _mode_of(self, path) -> "int | None":
        try:
            return _stat.S_IMODE(path.stat().st_mode)
        except (OSError, AttributeError, NotImplementedError):
            return None

    def _write_with_mode(self, path, data: bytes, mode: "int | None") -> None:
        """Write ``data`` to ``path`` without ever exposing it at a wider mode.

        A new file is created empty and chmod'ed BEFORE the content goes in:
        writing first and chmod'ing after leaves e.g. a copy of ``/etc/shadow``
        readable at the backend's default mode for the length of the call.
        """
        if mode is not None and not path.exists():
            path.write_bytes(b"")
            self._chmod(path, mode)
        path.write_bytes(data)
        if mode is not None and self._mode_of(path) != mode:
            self._chmod(path, mode)

    def _chmod(self, path, mode: int) -> None:
        try:
            path.chmod(mode)
        except (OSError, AttributeError, NotImplementedError):
            LOGGER.warning(
                "could not set mode %s on %s; it keeps whatever the write gave it",
                oct(mode),
                path,
            )

    def write(self, content: "str | bytes") -> bool:
        if content is None:
            raise TypeError(
                f"refusing to write None to {self.path}; the template rendered "
                "nothing (a render() that returns None, or no return at all)"
            )
        if isinstance(content, str):
            content = content.encode()

        parent = self.path.parent
        if not parent.exists():
            parent.mkdir(DIRECTORY_MODE, True, True)
        if self._baseline:
            self.baseline()

        if self.path.exists() and self.path.read_bytes() == content:
            return False

        # An existing file keeps its own mode: rewriting can reset it to the
        # umask default, and silently widening /etc/shadow from 0640 to 0644 is
        # a security regression. A new file gets `self.mode`, applied before
        # the content lands (see _write_with_mode).
        existing = self._mode_of(self.path) if self.path.exists() else None
        self._write_with_mode(
            self.path, content, existing if existing is not None else self.mode
        )
        return True


if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    pass
