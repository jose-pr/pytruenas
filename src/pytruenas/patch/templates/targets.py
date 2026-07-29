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

    def baseline(self):
        """Return the baseline path, creating the snapshot if it is missing.

        A target that does not exist yet has nothing to snapshot -- that is the
        ordinary "create this file if absent" case, and it must not fail. The
        previous implementation called ``read_bytes()`` on the missing original
        and raised ``FileNotFoundError`` from inside ``write()``.
        """
        baseline = self.baseline_path
        if baseline is None:
            return self.path
        if baseline.exists():
            return baseline
        if not self.path.exists():
            return baseline
        # Guard against an empty suffix, which would make the "baseline" the
        # target itself and truncate the file it exists to preserve. Compared
        # as strings rather than via resolve(): not every path backend has
        # resolve() (hostctl's CompositePosixPath does not), and a suffix that
        # is empty is the only way these can collide anyway.
        if str(baseline) == str(self.path):
            return self.path
        LOGGER.info("Snapshotting %s -> %s", self.path, baseline)
        baseline.write_bytes(self.path.read_bytes())
        return baseline

    def read(self) -> bytes:
        if self._baseline:
            baseline = self.baseline()
            if not baseline.exists():
                # No original to template from: an empty baseline is the
                # correct answer for a file that does not exist yet.
                raise FileNotFoundError(str(self.path))
            return baseline.read_bytes()
        return self.path.read_bytes()

    # -- inspection and undo ----------------------------------------------

    def is_patched(self) -> bool:
        """Whether the file currently differs from its baseline.

        ``False`` when there is no baseline to compare against -- either
        because this target does not use one, or because the file did not exist
        when it was first written (nothing was displaced, so nothing is
        "patched" in the sense of overwriting something).
        """
        baseline = self.baseline_path
        if baseline is None or not baseline.exists() or not self.path.exists():
            return False
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

        The counterpart the baseline mechanism exists for. Three cases:

        * a baseline exists -> its content is written back, and (by default)
          the snapshot is removed, so the target is left exactly as found;
        * no baseline, but this target created the file -> nothing to restore
          and no way to know it was ours, so this is a no-op returning ``False``
          rather than deleting a file that may not be ours to delete;
        * baseline configured but never taken -> also a no-op.

        ``remove_baseline=False`` keeps the snapshot, for reverting a patch you
        intend to re-apply.
        """
        baseline = self.baseline_path
        if baseline is None or not baseline.exists():
            LOGGER.debug("Nothing to revert for %s (no baseline)", self.path)
            return False

        original = baseline.read_bytes()
        changed = not self.path.exists() or self.path.read_bytes() != original
        if changed:
            LOGGER.info("Reverting %s to its baseline", self.path)
            self.path.write_bytes(original)
        if remove_baseline:
            unlink = getattr(baseline, "unlink", None)
            if callable(unlink):
                unlink(missing_ok=True)
            else:
                # Not in _REQUIRED_PATH_METHODS, because only revert() needs
                # it: a backend that cannot delete should still be able to
                # patch and to restore content.
                LOGGER.warning(
                    "cannot remove the baseline at %s (backend has no unlink); "
                    "the snapshot is left in place",
                    baseline,
                )
        return changed

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

        # Capture the mode BEFORE writing. Rewriting a file can reset it to
        # whatever the umask says, and silently widening /etc/shadow from 0640
        # to 0644 is a security regression, not a cosmetic one.
        mode = self._current_mode()
        self.path.write_bytes(content)
        if mode is not None:
            self._restore_mode(mode)
        elif self.mode is not None:
            self._apply_mode(self.mode)
        return True

    def _current_mode(self) -> "int | None":
        """The file's permission bits, or ``None`` if it does not exist yet."""
        try:
            if not self.path.exists():
                return None
            return _stat.S_IMODE(self.path.stat().st_mode)
        except (OSError, AttributeError):  # pragma: no cover - backend gaps
            return None

    def _apply_mode(self, mode: int) -> None:
        try:
            self.path.chmod(mode)
        except (OSError, AttributeError, NotImplementedError):
            # A backend without chmod (the websocket filesystem leg) must not
            # turn a successful write into a failure -- but the caller should
            # know the mode is not what they asked for.
            LOGGER.warning(
                "could not set mode %s on %s; it keeps whatever the write gave it",
                oct(mode),
                self.path,
            )

    def _restore_mode(self, mode: int) -> None:
        if self._current_mode() != mode:
            self._apply_mode(mode)


if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    pass
