from jinja2 import Environment, FileSystemLoader
from pathlib import Path as _P
from . import Renderer as _NSCodegen
from . import docstring as _docstring

BASEPATH = _P(__file__).parent

_DEFAULT_ENV = Environment(loader=FileSystemLoader(BASEPATH))
# Make the docstring-escaping helper available to every template.
_DEFAULT_ENV.globals["docstring"] = _docstring


class Renderer(_NSCodegen):
    def __init__(self, template: str):
        self.template = _DEFAULT_ENV.get_template(template + ".j2")

    def render(self, **ctx) -> str:
        return self.template.render(**ctx)
