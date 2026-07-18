from jinja2 import Environment, FileSystemLoader
from pathlib import Path as _P
from . import Renderer as _NSCodegen

BASEPATH = _P(__file__).parent

_DEFAULT_ENV = Environment(loader=FileSystemLoader(BASEPATH))


class Renderer(_NSCodegen):
    def __init__(self, template: str):
        self.template = _DEFAULT_ENV.get_template(template + ".j2")

    def render(self, **ctx) -> str:
        return self.template.render(**ctx)
