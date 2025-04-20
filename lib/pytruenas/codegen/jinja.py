from jinja2 import Environment, FileSystemLoader
from pathlib import Path as _P
import typing as _ty
from . import NamespaceCodegen as _NSCodegen, Namespace

_DEFAULT_TEMPLATE = _P(__file__).parent / "ns_template.pyi.j2"

_DEFAULT_ENV = Environment(loader=FileSystemLoader(_DEFAULT_TEMPLATE.parent))


class NamespaceCodegen(_NSCodegen):
    template = _DEFAULT_ENV.get_template(_DEFAULT_TEMPLATE.name)

    def render(self, ns: Namespace) -> str:
        return self.template.render(ns=ns)