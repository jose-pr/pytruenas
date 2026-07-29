"""Render content and apply it to a target, only when it changed.

Two halves, deliberately separate:

* :mod:`.base` -- rendering. A template turns itself plus a context into text
  and knows nothing about where that text goes.
* :mod:`.targets` -- destinations. A target reads what is already there, writes
  only if the new content differs, and reports which happened.

That boolean is the point. Everything in :mod:`pytruenas.patch` keys its
expensive follow-up work (``systemctl daemon-reload``, an ``etc.generate``, a
service reload) off it, so applying the same configuration twice does the work
once.

Was a single ``ops/template.py``; split when the file-target logic grew a
baseline mechanism worth reading on its own.
"""

from .base import (
    BaseTemplate,
    BasicTemplate,
    TextTemplate,
    render_basic_template,
)
from .targets import FileTarget, TemplateTarget

__all__ = [
    "BaseTemplate",
    "BasicTemplate",
    "TextTemplate",
    "render_basic_template",
    "FileTarget",
    "TemplateTarget",
]
