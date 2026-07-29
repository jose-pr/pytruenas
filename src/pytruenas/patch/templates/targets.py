"""Where rendered content goes, and how "did it change?" is decided.

A target owns two things a template does not: reading whatever is already
there, and writing only when the new content differs. That comparison is the
whole basis of idempotence in :mod:`pytruenas.patch` -- every caller decides
whether to reload a service or regenerate an etc group from the boolean
``write`` returns.
"""

from __future__ import annotations

import logging as _logging
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

    def __init__(self, path, baseline: "bool | str" = False) -> None:
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
        self.path.write_bytes(content)
        return True


if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    pass
