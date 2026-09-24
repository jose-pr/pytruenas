"""CLI-style help for a middleware method, read from the API definition.

``pytruenas help user.create nas1`` prints what the method takes: every field
with its type, whether it is required, its default, and the values an enum
allows -- in the same spelling ``call`` accepts them::

    pytruenas help user.create nas1          # one method
    pytruenas help user nas1                 # the methods of a namespace
    pytruenas help nas1                      # every namespace, with counts

The source is the cached API definition (see
:mod:`pytruenas.utils.apicache`), because descriptions, defaults, enum values
and required-ness exist only there -- generated ``.pyi`` stubs cannot carry
them. The first run on a host fetches and caches the definition; later runs
touch only the cache.

``NAME`` is optional, which makes it ambiguous with a target: a single bare
word is treated as a **method or namespace** when the API definition has one by
that name, and as a target otherwise. Pass ``--name`` to be explicit.
"""

from __future__ import annotations

from logging import Logger

from pytruenas import TrueNASClient
from pytruenas.utils import apicache, apihelp
from pytruenas.utils.cmd import PyTrueNASArgs, emit, emit_json


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``help``."""

    name: str = None
    """Method (``user.create``) or namespace (``user``) to describe; omitted,
    every namespace is listed."""

    refresh_api: bool = False
    "Re-fetch the API definition instead of using the cache"

    api_version: str = None
    "Describe this API version from the dump (default: the newest)"

    json: bool = False
    "Emit the definition slice as JSON instead of prose, for tooling"


def run(client: TrueNASClient, args: Args, logger: Logger):
    api = apicache.load(client, refresh=args.refresh_api)
    versions = api["versions"]
    # The dump lists versions newest-first; `generate-typings` reads it the
    # same way.
    if args.api_version:
        version = next((v for v in versions if v["version"] == args.api_version), None)
        if version is None:
            logger.error(
                "version %r not found; available: %s",
                args.api_version,
                ", ".join(v["version"] for v in versions),
            )
            return 2
    else:
        version = versions[0]

    name = args.name
    if not name:
        emit(apihelp.render_index(version).rstrip("\n"))
        return 0

    methods = apihelp.methods(version)
    if name in methods:
        if args.json:
            emit_json(methods[name], args)
        else:
            emit(apihelp.render(name, methods[name]).rstrip("\n"))
        return 0

    try:
        text = apihelp.render_namespace(version, name)
    except apihelp.UnknownMethod:
        # Not a namespace either -- report it as the method miss, which carries
        # the near-miss suggestions.
        try:
            apihelp.find(version, name)
        except apihelp.UnknownMethod as exc:
            logger.error("%s", exc)
            return 2
        raise
    if args.json:
        prefix = name + "."
        emit_json(
            {n: m for n, m in methods.items() if n.startswith(prefix)},
            args,
        )
    else:
        emit(text.rstrip("\n"))
    return 0
