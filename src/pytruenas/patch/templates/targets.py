"""Where rendered content goes, and how "did it change?" is decided.

A target owns two things a template does not: reading whatever is already
there, and writing only when the new content differs. That comparison is the
whole basis of idempotence in :mod:`pytruenas.patch` -- every caller decides
whether to reload a service or regenerate an etc group from the boolean
``write`` returns.
"""

from __future__ import annotations

import hashlib as _hashlib
import logging as _logging
import stat as _stat
import typing as _ty
import uuid as _uuid
from pathlib import Path as _LocalPath

from .base import BaseTemplate, TextTemplate

__all__ = ["TemplateTarget", "FileTarget"]

LOGGER = _logging.getLogger(__name__)

#: Mode for directories created on the way to a target. Octal: a bare ``755``
#: is decimal, i.e. ``0o1363`` (setuid plus the wrong permission bits).
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

        ``kwargs`` reach the constructor of a template *class*, and only
        there: with any other form they raise ``TypeError``.
        """
        if isinstance(template, type) and issubclass(template, BaseTemplate):
            try:
                baseline = self.read()
            except FileNotFoundError:
                baseline = b""
            template = template(baseline, **kwargs)
        elif kwargs:
            # Silently dropping these would leave the caller wondering why
            # their option had no effect.
            if isinstance(template, BaseTemplate):
                raise TypeError(
                    "kwargs are not accepted with an already-constructed "
                    f"template ({type(template).__name__}); pass them where it "
                    "is built"
                )
            raise TypeError(
                "kwargs are accepted only with a template class, which they "
                f"are passed to; got {type(template).__name__}"
            )
        elif isinstance(template, str):
            template = TextTemplate(template)
        elif not isinstance(template, BaseTemplate):
            template = TextTemplate(_LocalPath(template).read_text(encoding="utf-8"))

        return template.apply(self, context)


class FileTarget(TemplateTarget):
    """A file, optionally with a baseline snapshot of its original content.

    With ``baseline`` set, the first write that changes the file copies the
    existing file aside (``<name>.baseline`` by default) and :meth:`read`
    returns *that* rather than the current content. This is what makes
    repeated application idempotent: a template that layers changes onto a
    stock config always sees the stock config, not its own previous output.

    Each changing write also records a digest of what it wrote
    (``<name>.baseline.applied``). When the file no longer matches it,
    something else has rewritten it since -- TrueNAS regenerating an ``/etc``
    file, say -- and that content is the original from then on: :meth:`read`
    returns it, the next write snapshots it, and :meth:`revert` leaves it.

    A baseline or marker found beside the target is trusted only when it is a
    regular file with one link, owned by root or by the target's owner; a
    symlink or anything else there raises ``PermissionError`` rather than
    being read or written through. (Checked where the path backend offers
    ``lstat()``.)
    """

    def __init__(
        self,
        path,
        baseline: "bool | str" = False,
        mode: "int | None" = None,
    ) -> None:
        # Duck-typed: only the methods below are called, so a test double or
        # another backend's path works. The error still fires here, naming
        # what is missing.
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
        """Records that the file did not exist when this target first changed it.

        So a later write does not take this target's own output for an
        original, and :meth:`revert` leaves a file it created in place.
        """
        if not self._baseline:
            return None
        return self.path.with_name(self.path.name + self._baseline + ".absent")

    @property
    def _record_path(self):
        """Holds SHA-256 digests (hex, one per line) of what the file may hold
        from this target's last write."""
        if not self._baseline:
            return None
        return self.path.with_name(self.path.name + self._baseline + ".applied")

    def baseline(self):
        """Return the baseline path, creating the snapshot if it is missing.

        A target that does not exist yet has nothing to snapshot -- that is the
        ordinary "create this file if absent" case, and it must not fail; it is
        recorded with an ``.absent`` marker instead, so later writes and
        ``revert()`` know the original was absent. The snapshot keeps the
        original's permission bits: a copy of ``/etc/shadow`` must not be
        world-readable.
        """
        if self.baseline_path is None:
            return self.path
        self._snapshot(self._current())
        return self.baseline_path

    def _snapshot(self, current: "bytes | None") -> None:
        """Take the snapshot (or the absent marker) unless one exists and the
        file is still what this target last wrote."""
        baseline = self.baseline_path
        marker = self._absent_marker
        kept = baseline if self._present(baseline) else None
        if kept is None and self._present(marker):
            kept = marker
        if kept is not None:
            if current is None or not self._displaced(current):
                return
            LOGGER.warning(
                "%s was rewritten since this target last wrote it; "
                "taking its content as the original",
                self.path,
            )
            self._create(baseline, current, self._mode_of(self.path))
            if kept is marker:
                self._unlink(marker)
            return
        if current is None:
            self._create(self._absent_marker, b"", None)
            return
        LOGGER.info("Snapshotting %s -> %s", self.path, baseline)
        self._create(baseline, current, self._mode_of(self.path))

    def read(self) -> bytes:
        """The content to template FROM: the baseline if one exists, else the file.

        **Never creates the snapshot**: that is :meth:`write`'s job. Reading
        must work on a read-only mount (the middlewared package ships on one),
        and a caller who only reads has changed nothing that needs undoing.
        With no snapshot yet, the file's CURRENT content is the original.

        Raises ``FileNotFoundError`` when there is no original: the file is
        missing, or it did not exist when this target first wrote it.
        """
        if self._baseline:
            baseline = self.baseline_path
            has_baseline = self._present(baseline)
            if has_baseline or self._present(self._absent_marker):
                current = self._displaced()
                if current is not None:
                    return current
                if has_baseline:
                    return baseline.read_bytes()
                # The original was absent: template from nothing, not from
                # this target's own earlier output.
                raise FileNotFoundError(str(self.path))
        current = self._current()
        if current is None:
            # Distinguishing this from an empty file is the caller's job
            # (`apply_template` treats it as empty).
            raise FileNotFoundError(str(self.path))
        return current

    # -- inspection and undo ----------------------------------------------

    def is_patched(self) -> bool:
        """Whether the file currently differs from its baseline.

        ``False`` when there is no snapshot to compare against -- this target
        keeps no baseline, or the file did not exist when it was first written
        (nothing was displaced). A snapshotted file is patched while its
        content differs, including when it has been deleted.
        """
        baseline = self.baseline_path
        if baseline is None or not self._present(baseline):
            return False
        if self._displaced() is not None:
            return False  # rewritten by something else: the patch is gone
        return self._current() != baseline.read_bytes()

    def would_change(self, content: "str | bytes") -> bool:
        """Whether writing ``content`` would modify the file. No side effects."""
        if isinstance(content, str):
            content = content.encode()
        return self._current() != content

    def revert(self, remove_baseline: bool = True) -> bool:
        """Restore the original content. Returns whether anything changed.

        The counterpart the baseline mechanism exists for. Cases:

        * a snapshot exists -> its content (and permission bits) are written
          back, and (by default) the snapshot is removed, so the target is left
          exactly as found;
        * this target created the file -> the file is left in place (not ours
          to delete) and returns ``False``; by default its ``.absent`` marker
          is removed;
        * baseline configured but never taken, or no baseline -> a no-op;
        * the file was rewritten by something else since this target wrote it
          -> left as it is (the patch is already gone) and returns ``False``.

        ``remove_baseline=False`` keeps the snapshot or marker, for reverting a
        patch you intend to re-apply.
        """
        baseline = self.baseline_path
        if baseline is None:
            return False
        marker = self._absent_marker
        if self._present(marker):
            if remove_baseline:
                self._discard(marker, self._record_path)
            return False
        if not self._present(baseline):
            LOGGER.debug("Nothing to revert for %s (no baseline)", self.path)
            return False
        if self._displaced() is not None:
            LOGGER.info(
                "Not reverting %s: it was rewritten since this target wrote it",
                self.path,
            )
            if remove_baseline:
                self._discard(baseline, self._record_path)
            return False

        original = baseline.read_bytes()
        current = self._current()
        changed = current != original
        if changed:
            LOGGER.info("Reverting %s to its baseline", self.path)
            self._record(original, current)
            self._write_with_mode(
                self.path,
                original,
                self._mode_of(baseline),
                exists=current is not None,
            )
        if remove_baseline:
            self._discard(baseline, self._record_path)
        return changed

    # -- writing ------------------------------------------------------------

    def write(self, content: "str | bytes") -> bool:
        """Write ``content`` if it differs; return whether it did.

        An existing file keeps its own mode; a new one gets ``mode`` before
        any content lands. With a baseline configured, the snapshot is taken
        only when the file is about to change.
        """
        return self._write(content)[0]

    def _write(self, content: "str | bytes") -> "tuple[bool, bytes | None]":
        """``write()``, also returning the content found (``None``: absent)."""
        if content is None:
            raise TypeError(
                f"refusing to write None to {self.path}; the template rendered "
                "nothing (a render() that returns None, or no return at all)"
            )
        if isinstance(content, str):
            content = content.encode()

        current = self._current()
        if current == content:
            return False, current
        if current is None:
            parent = self.path.parent
            if not parent.exists():
                parent.mkdir(DIRECTORY_MODE, True, True)
        if self._baseline:
            self._snapshot(current)
            # Before the write: should it not complete, the file still
            # matches a recorded digest and is not taken for a rewrite.
            self._record(content, current)

        # An existing file keeps its own mode: rewriting can reset it to the
        # umask default, and widening /etc/shadow from 0640 to 0644 is a
        # security regression. A new file gets `self.mode`.
        mode = self._mode_of(self.path) if current is not None else None
        self._write_with_mode(
            self.path,
            content,
            mode if mode is not None else self.mode,
            exists=current is not None,
        )
        return True, current

    # -- helpers --------------------------------------------------------------

    def _current(self) -> "bytes | None":
        """The file's content, or ``None`` when it does not exist."""
        try:
            return self.path.read_bytes()
        except FileNotFoundError:
            return None

    def _record(self, *contents: "bytes | None") -> None:
        """Note ``contents`` as what the file may hold from this target: what
        it is about to write, and what it found (should the write not land)."""
        record = self._record_path
        self._present(record)  # refuses a planted symlink before writing
        digests = [_digest(content) for content in contents if content is not None]
        self._write_with_mode(record, b"\n".join(digests) + b"\n", None)

    def _displaced(self, current: "bytes | None | object" = ...) -> "bytes | None":
        """The file's content when something else rewrote it since this target
        last wrote it, else ``None``. Without a record, never displaced."""
        record = self._record_path
        if record is None or not self._present(record):
            return None
        if current is ...:
            current = self._current()
        if current is None or _digest(current) in record.read_bytes().split():
            return None
        return _ty.cast(bytes, current)

    def _discard(self, *paths) -> None:
        for path in paths:
            if path is not None and self._present(path):
                self._unlink(path)

    def _present(self, path) -> bool:
        """Whether a baseline or marker exists, raising for one not to trust.

        A non-root user who can write the target's directory could plant a
        symlink or a file there; root would then template from it, write
        through it, or restore it into the target.
        """
        lstat = getattr(path, "lstat", None)
        if not callable(lstat):
            return path.exists()
        try:
            info = lstat()
        except FileNotFoundError:
            return False
        except ConnectionError:
            raise
        except (OSError, NotImplementedError, AttributeError):
            return path.exists()
        mode = getattr(info, "st_mode", None)
        if mode is not None and not _stat.S_ISREG(mode):
            raise PermissionError(
                f"refusing {path}: not a regular file (a symlink or other "
                "entry where this target keeps its baseline)"
            )
        if (getattr(info, "st_nlink", 1) or 1) > 1:
            raise PermissionError(f"refusing {path}: it has other hard links")
        uid = getattr(info, "st_uid", None)
        if uid:
            owner = self._owner_uid()
            if owner is not None and uid != owner:
                raise PermissionError(
                    f"refusing {path}: owned by uid {uid}, which is neither root "
                    f"nor the owner of {self.path}"
                )
        return True

    def _owner_uid(self) -> "int | None":
        """The uid owning the target, or its directory while it is absent."""
        for candidate in (self.path, self.path.parent):
            try:
                return getattr(candidate.stat(), "st_uid", None)
            except FileNotFoundError:
                continue
            except ConnectionError:
                raise
            except (OSError, NotImplementedError, AttributeError):
                return None
        return None

    def _create(self, path, data: bytes, mode: "int | None") -> None:
        """Create ``path`` holding ``data``, complete or not at all.

        Written to a randomly named sibling and renamed into place where the
        backend can replace, so an interrupted transfer leaves no truncated
        snapshot to be trusted as the original, and the rename replaces
        whatever sits at ``path`` instead of writing through it.
        """
        temporary = path.with_name(f".{path.name}.{_uuid.uuid4().hex[:12]}.tmp")
        if not callable(getattr(temporary, "replace", None)):
            self._write_with_mode(path, data, mode)
            return
        try:
            self._write_with_mode(temporary, data, mode, exists=False)
            temporary.replace(path)
        except BaseException:
            try:
                self._unlink(temporary)
            except Exception:
                LOGGER.warning("could not remove %s", temporary)
            raise

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
        except ConnectionError:
            # A lost or never-made connection (hostctl's
            # OperationNotStartedError among them) is not "this backend has
            # no modes"; reading it as one would let the write go ahead.
            raise
        except (OSError, AttributeError, NotImplementedError):
            return None

    def _write_with_mode(
        self, path, data: bytes, mode: "int | None", exists: "bool | None" = None
    ) -> None:
        """Write ``data`` to ``path`` without ever exposing it at a wider mode.

        A new file is created empty and chmod'ed BEFORE the content goes in,
        so a copy of e.g. ``/etc/shadow`` is never readable at the backend's
        default mode, not even for the length of the call. ``exists`` saves
        the check when the caller already knows.
        """
        if exists is None:
            exists = mode is not None and path.exists()
        if mode is not None and not exists:
            path.write_bytes(b"")
            self._chmod(path, mode)
        path.write_bytes(data)
        if mode is not None and self._mode_of(path) != mode:
            self._chmod(path, mode)

    def _chmod(self, path, mode: int) -> None:
        try:
            path.chmod(mode)
        except ConnectionError:
            # The content write that follows may reconnect and succeed, which
            # would leave it at the wider mode this chmod was meant to prevent.
            raise
        except (OSError, AttributeError, NotImplementedError):
            LOGGER.warning(
                "could not set mode %s on %s; it keeps whatever the write gave it",
                oct(mode),
                path,
            )


def _digest(content: bytes) -> bytes:
    return _hashlib.sha256(content).hexdigest().encode("ascii")
