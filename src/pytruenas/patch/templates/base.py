"""Rendering: turn a template plus a context into text.

Deliberately knows nothing about *where* the result goes -- that is a
:mod:`~pytruenas.patch.templates.targets` concern. The split is what lets the
same template be applied to a remote file, a systemd unit, or a test double.
"""

from __future__ import annotations

import logging as _logging
import re as _re
import typing as _ty

__all__ = [
    "BaseTemplate",
    "TextTemplate",
    "BasicTemplate",
    "render_basic_template",
]

LOGGER = _logging.getLogger(__name__)


class BaseTemplate:
    """Something that renders to text.

    Subclasses implement :meth:`render`. :meth:`apply` then writes the result
    to a target and reports whether that changed anything -- the return value
    every caller keys their follow-up work off (reload a service, regenerate an
    etc group) so nothing expensive runs on an unchanged file.
    """

    @property
    def source(self) -> str:
        """Where this template came from, for logs. Overridden by subclasses."""
        return "mem"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.source})"

    def render(self, context: object) -> str:
        """Return the rendered text.

        Abstract: a subclass that does not override it raises here, rather
        than handing ``None`` to ``write()`` as the file's new content.
        """
        raise NotImplementedError(f"{type(self).__name__} must implement render()")

    def apply(self, target: "TemplateTarget", context: object = None) -> bool:
        """Render and write to ``target``; return whether it changed."""
        LOGGER.info("Applying %r to %r", self, target)
        rendered = self.render(context if context is not None else {})
        modified = target.write(rendered)
        if modified:
            LOGGER.info("%r modified", target)
        return modified


class TextTemplate(BaseTemplate):
    """A literal string, rendered unchanged."""

    def __init__(self, text: "str | bytes") -> None:
        self.text = text.decode() if isinstance(text, bytes) else text

    def render(self, context: object) -> str:
        return self.text


class BasicTemplate(TextTemplate):
    """A string with ``%{NAME}`` placeholders substituted from the context."""

    def render(self, context: object) -> str:
        return render_basic_template(self.text, context)


def render_basic_template(template: str, context: "object | dict | None") -> str:
    """Substitute ``%{name}`` / ``%{NAME}`` placeholders from ``context``.

    ``context`` may be a mapping or any object with a ``__dict__``. A
    placeholder matches a name as given or its upper-cased form, so a template
    can use ``%{PORT}`` against a ``port`` attribute without the caller
    restating it; an exact match wins. Substitution is one pass: a value that
    itself contains ``%{...}`` is inserted as is, and a placeholder naming
    nothing in ``context`` is left untouched.

    A ``None`` context, or an object without attributes, leaves the template
    untouched rather than raising -- rendering a template with nothing to
    substitute is a no-op, not an error.
    """
    if context is None:
        return template
    if not isinstance(context, dict):
        try:
            context = vars(context)
        except TypeError:
            return template
    values: "dict[str, str]" = {}
    for name, value in context.items():
        values.setdefault(str(name).upper(), str(value))
    for name, value in context.items():
        values[str(name)] = str(value)

    def lookup(match: "_re.Match[str]") -> str:
        return values.get(match.group(1), match.group(0))

    return _PLACEHOLDER.sub(lookup, template)


#: ``%{name}``: any run of characters other than braces.
_PLACEHOLDER = _re.compile(r"%\{([^{}]+)\}")


if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from .targets import TemplateTarget
