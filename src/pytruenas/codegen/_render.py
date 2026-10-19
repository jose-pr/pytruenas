"""The source of one stub module."""

from __future__ import annotations

import json as _json
import typing as _ty

from ._declarations import Namespace, docstring

#: The start of every stub module, up to its child-namespace imports.
_HEADER = """\
from __future__ import annotations

from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import sys
import typing as _ty

# Never, NotRequired and Unpack are typing members only from 3.11; this
# project's floor -- and so a consumer's checking target -- is 3.9. `sys` is not
# aliased: mypy reads a version check only on the module's own name.
if sys.version_info >= (3, 11):
    from typing import Never as _Never, NotRequired as _NotRequired, Unpack as _Unpack
else:
    from typing_extensions import (
        Never as _Never,
        NotRequired as _NotRequired,
        Unpack as _Unpack,
    )"""

#: Ends the root module: `TrueNASClient[Current]` is the documented spelling.
_CURRENT = """

#: The documented spelling: `TrueNASClient[Current]`, so a consumer pins "the
#: version these typings were generated from" without naming it.
{alias} = {classname}"""


def render(ns: "Namespace", alias: "_ty.Optional[str]" = None) -> str:
    """The source of one namespace's stub module.

    ``alias``, given for the root namespace only, names an alias of its class.
    TypedDicts are collected while the signatures are rendered, so they follow
    the class.
    """
    typeddicts: "dict[str, dict[str, str]]" = {}
    out = [_HEADER]
    children = ns.namespaces()
    for child in children:
        module = child.pyname.relative_to(ns.pyname)
        out.append(f"\nfrom .{module} import {child.classname}")
    out.append(f"\n\n\nclass {ns.classname}(_NS):\n    ")
    methods = ns.methods()
    for method in methods:
        ignore = "  # type: ignore[override]" if method.overrides_runtime else ""
        out.append(f"\n    def {method.pyname.name}(self,{ignore}")
        out.extend(
            f"\n        {decl}," for decl in method.declared_parameters(typeddicts)
        )
        returns = method.returns.type_def(typeddicts)
        out.append(f'\n    ) -> {returns}:\n        """{docstring(method.doc)}"""')
        out.append("\n        ...")
    for child in children:
        out.append(f"\n    {child.pyname.name}: {child.classname}")
    if not methods and not children:
        out.append("\n    pass")
    out.append("\n\n")
    for name, properties in typeddicts.items():
        out.append(f"\n{name} = _ty.TypedDict('{name}', {{")
        # JSON string syntax is valid Python string syntax.
        out.extend(
            f"\n    {_json.dumps(key)}: {value}," for key, value in properties.items()
        )
        out.append("\n})\n")
    if alias:
        out.append(_CURRENT.format(alias=alias, classname=ns.classname))
    return "".join(out)
