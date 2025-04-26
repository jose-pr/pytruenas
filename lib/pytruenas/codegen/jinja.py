from jinja2 import Environment, FileSystemLoader
from pathlib import Path as _P
from . import Renderer as _NSCodegen

_DEFAULT_TEMPLATE = _P(__file__).parent / "ns_template.pyi.j2"

_DEFAULT_ENV = Environment(loader=FileSystemLoader(_DEFAULT_TEMPLATE.parent))


class NamespaceRenderer(_NSCodegen):
    template = _DEFAULT_ENV.get_template(_DEFAULT_TEMPLATE.name)

    def render(self, **ctx) -> str:
        return self.template.render(**ctx)