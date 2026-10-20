"""The ``pytruenas`` command line: the app, its global options and output helpers.

:func:`main` is the console script. A derived tool subclasses
:class:`PyTrueNASArgs` (global options) or :class:`PyTrueNAS` (the app) and
calls :func:`main` with them; a command module writes its results with
:func:`emit_json`. RunPath step helpers are in :mod:`pytruenas.cli.runpath`.
"""

from .._utils.env import ENV
from ._app import PyTrueNAS, main
from ._args import (
    PyTrueNASArgs,
    TargetsField,
    default_config_path,
    emit,
    emit_json,
    json_default,
    with_targets,
)

__all__ = [
    "main",
    "PyTrueNAS",
    "PyTrueNASArgs",
    "TargetsField",
    "with_targets",
    "default_config_path",
    "emit",
    "emit_json",
    "json_default",
    "ENV",
]
