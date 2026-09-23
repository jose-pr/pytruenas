"""Jinja environment for the stub templates.

The template is read through ``importlib.resources``, not a
``FileSystemLoader``: a zipapp (what ``deploy --mode pyz`` installs, and the
default) has no filesystem path for it, so loading by directory failed with
``TemplateNotFound`` there while working in a checkout.
"""

from pathlib import Path as _P

from jinja2 import DictLoader, Environment

from . import Renderer as _NSCodegen
from . import docstring as _docstring

BASEPATH = _P(__file__).parent


def _template_text(name: str) -> str:
    """The template source, from wherever this package actually lives."""
    try:
        from importlib.resources import files

        return (files(__package__) / name).read_text(encoding="utf-8")
    except (ImportError, AttributeError, FileNotFoundError, TypeError):
        # Python 3.9 has `files()` but a zip importer may not support it for
        # every layout; a real directory still reads fine.
        return (BASEPATH / name).read_text(encoding="utf-8")


#: Templates shipped with this package, loaded once by name.
_TEMPLATES = {"namespace.pyi.j2": _template_text("namespace.pyi.j2")}

_DEFAULT_ENV = Environment(loader=DictLoader(_TEMPLATES))
# Make the docstring-escaping helper available to every template.
_DEFAULT_ENV.globals["docstring"] = _docstring


class Renderer(_NSCodegen):
    def __init__(self, template: str):
        self.template = _DEFAULT_ENV.get_template(template + ".j2")

    def render(self, **ctx) -> str:
        return self.template.render(**ctx)
