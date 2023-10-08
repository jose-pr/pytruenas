from mako.template import Template as _MakoTemplate
from pathlib import Path as _P
import typing as _ty
from . import NamespaceCodegen as _NSCodegen, NamespaceInfo

_DEFAULT_TEMPLATE = _P(__file__).parent.parent / "namespace" / "_template.py.mako"


class NamespaceCodegen(_NSCodegen):
    template = _MakoTemplate(filename=str(_DEFAULT_TEMPLATE)), _MakoTemplate(
        filename=str(_DEFAULT_TEMPLATE).removesuffix(".py.mako") + ".pyi.mako"
    )

    def generate(self, ns: NamespaceInfo, exportas: str, modname: str) -> str:
        return [
            t.render(ns=ns, exportas=exportas, modname=modname)
            for t in (
                self.template
                if isinstance(self.template, _ty.Sequence)
                else [self.template]
            )
        ]
