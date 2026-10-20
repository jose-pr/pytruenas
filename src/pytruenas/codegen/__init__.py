"""Typings generation: one ``.pyi`` stub module per namespace of an API version.

``Codegen().generate(version, root)`` is the entry point; ``generate-typings``
runs it.
"""

from __future__ import annotations

import copy as _copy
import logging as _logging
import os as _os
import shutil
import tempfile
import time as _time
import typing as _ty
from pathlib import Path as _P

from duho import qualname as _qn
from pathapi.providers import is_safe_child_name as _is_safe_child_name
from duho import text as _text

from ..exceptions import TrueNASError
from ..models import apidump as _api
from . import _declarations as _decl
from ._render import render as _render

__all__ = ["Codegen", "BadAPIName"]

#: Generation is a library call; it has no host logger to borrow.
_LOGGER = _logging.getLogger("pytruenas.codegen")

_INIT = "__init__.pyi"
#: Written into every generated tree, so a later run knows it may replace it.
_MARKER = ".pytruenas-typings"


def _check_replaceable(root: _P) -> None:
    """Refuse to replace a directory that is not a typings tree.

    Replaceable: absent, empty, or carrying the marker every generated tree
    has. Anything else is someone's data -- a checkout's ``.git``, notes, or
    hand-written stubs (``typings/`` is where pyright looks for them).
    """
    if not root.exists():
        return
    if not root.is_dir():
        raise FileExistsError(f"{root} exists and is not a directory")
    if (root / _MARKER).exists() or next(root.iterdir(), None) is None:
        return
    raise FileExistsError(
        f"refusing to replace {root}: it is not a tree generate-typings wrote "
        f"(no {_MARKER}); choose another path"
    )


def _runtime_namespace_attributes() -> "frozenset[str]":
    """Names a generated namespace class must not redefine.

    The real `Namespace` methods (`subscribe`, and the `_query`/`_get`/...
    helpers, which are generated deliberately from the schema and so are
    excluded by the caller).
    """
    from ..namespace import Namespace as _RuntimeNamespace

    return frozenset(
        name for name in dir(_RuntimeNamespace) if not name.startswith("__")
    )


def _shadows_runtime(declaration: "_decl.Method") -> bool:
    """Whether this dump method would redefine a real ``Namespace`` member."""
    name = declaration.pyname.name
    if name.startswith("_"):
        # The synthetic helpers are meant to describe the runtime ones.
        return False
    return name in _runtime_namespace_attributes()


def _swap(new: _P, final: _P) -> None:
    """Put the tree ``new`` at ``final``.

    The previous tree is renamed aside and deleted only once ``new`` is in
    place, so a failure (on Windows, a stub held open or a shell inside the
    tree) leaves it whole at ``final``.
    """
    old = None
    if final.exists():
        old = new.with_name(new.name + ".old")
        _rename(final, old)
    try:
        _rename(new, final)
    except BaseException:
        if old is not None:
            try:
                _rename(old, final)
            except OSError:
                _LOGGER.error("the previous output is left at %s", old)
        raise
    if old is not None:
        shutil.rmtree(old, ignore_errors=True)
        if old.exists():
            _LOGGER.warning("could not delete the previous output at %s", old)


def _rename(source: _P, target: _P) -> None:
    """``source.rename(target)``, retried for about a second on Windows, where
    a scanner or indexer opening a file just written fails it briefly."""
    attempts = 5 if _os.name == "nt" else 1
    for attempt in range(attempts):
        try:
            source.rename(target)
            return
        except PermissionError:
            if attempt == attempts - 1:
                raise
            _time.sleep(0.05 * 2**attempt)


def _empty_arrays(node: object) -> None:
    """Rewrite ``items: false`` in place, so that the stub names the header's
    ``_Never`` (``typing`` has ``Never`` only from 3.11) whatever interpreter
    generates it. With ``prefixItems`` it closes a tuple: any JSON array."""
    if isinstance(node, dict):
        if node.get("items") is False:
            if "prefixItems" in node:
                del node["items"]
            else:
                node["items"] = {"type": "!_Never"}
        for value in node.values():
            _empty_arrays(value)
    elif isinstance(node, list):
        for value in node:
            _empty_arrays(value)


def _check_inside(root: _P, path: _P) -> None:
    """Refuse a generated path a filesystem would not take as written.

    Every component comes from the API dump (namespace and method names): one
    holding a separator or ``..`` would escape ``root``, and one naming a
    Windows device (``nul``, ``con``) would write to it.
    """
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        raise BadAPIName(f"{path} would be written outside {root}") from None
    bad = [part for part in parts if not _is_safe_child_name(part, windows=True)]
    if bad:
        raise BadAPIName(f"{path}: {bad[0]!r} cannot be a file name")


class BadAPIName(TrueNASError, ValueError):
    """A name from the API definition cannot be used as a file name: written
    as given, it would land outside the output directory."""


class Codegen:
    """Writes the typings for one version of the API definition."""

    def generate(self, api: _api.Version, root: "_ty.Union[_P, str]") -> None:
        """Write one ``__init__.pyi`` per namespace of ``api`` under ``root``.

        ``api`` is one entry of ``client.dump_api()["versions"]``; it is not
        modified. ``root`` is replaced only when it is absent, empty or a
        previous output (it holds a ``.pytruenas-typings`` marker), and only
        once the new tree is complete. Raises ``FileExistsError`` for any
        other ``root``, and :class:`BadAPIName` for a name that would write
        outside it.
        """
        # A copy: method names are prefixed and return titles rewritten below,
        # and the caller's dump must come back as it was given.
        api = _copy.deepcopy(api)
        _empty_arrays(api)
        declarations: "list[_decl.Declaration]" = []
        # The version string (e.g. ``v26.0.0``) is ONE opaque root segment, not a
        # dotted qualname -- collapse its dots so it does not split into three
        # namespace levels with a leaf named ``0`` (an invalid class name).
        version = _qn.DotQualNamed(_text.pysafe(api["version"].replace(".", "_")))
        version_ns = _decl.Namespace(version)
        for method in api["methods"]:
            method["name"] = version / method["name"]
            declaration = _decl.Method(method)
            if _shadows_runtime(declaration):
                # A middleware method named like a real `Namespace` method
                # (`core.subscribe`): a stub would redefine the class member, and
                # a checker would type the runtime method with the middleware's
                # signature. `ns(_method="subscribe", ...)` reaches it.
                _LOGGER.info(
                    "%s is shadowed by Namespace.%s; call it as "
                    '_method="%s" (no stub emitted)',
                    method["name"],
                    declaration.pyname.name,
                    declaration.pyname.name,
                )
                continue
            declarations.append(declaration)

        namespaces: "list[_decl.Namespace]" = [version_ns]
        for decl in declarations:
            while True:
                namespace = decl.qualname.parent
                if namespace and namespace not in namespaces:
                    decl = _decl.Namespace(namespace)
                    namespaces.append(decl)
                else:
                    break

        final = _P(root)
        _check_replaceable(final)
        # Render into a sibling first and swap it in only once every stub is
        # written: a failure part-way leaves the previous output untouched.
        final.parent.mkdir(parents=True, exist_ok=True)
        root = _P(tempfile.mkdtemp(prefix=f".{final.name}.", dir=final.parent))
        try:
            self._write(version, declarations, namespaces, root)
            (root / _MARKER).write_bytes(
                b"Generated by `pytruenas generate-typings`; replaced on regeneration.\n"
            )
            _swap(root, final)
        except BaseException:
            shutil.rmtree(root, ignore_errors=True)
            raise

    @staticmethod
    def _write(version, declarations, namespaces, root: _P) -> None:
        for ns in sorted(namespaces, key=lambda ns: ns.qualname):
            ns_path = ns.pyname.relative_to(version).as_path(root) / _INIT
            _check_inside(root, ns_path)
            ns_path.parent.mkdir(exist_ok=True, parents=True)
            for decl in [*declarations, *namespaces]:
                if decl.qualname.parent == ns and ns != decl:
                    ns.childs.append(decl)
            ns.init()
            # Bytes in UTF-8: docstrings from the dump contain non-ASCII that the
            # platform default (cp1252) would mangle, and text mode would write
            # CRLF on Windows, so one dump would give two different trees.
            # The root class is named after the version (`V2600` for v26.0.0);
            # `Current` is the documented name for it.
            alias = "Current" if ns.qualname == version else None
            ns_path.write_bytes(_render(ns, alias=alias).encode("utf-8"))
