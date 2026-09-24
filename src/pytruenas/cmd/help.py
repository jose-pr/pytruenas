"""CLI-style help for a middleware method, read from the API definition.

``pytruenas help user.create nas1`` prints what the method takes: every field
with its type, whether it is required, its default, and the values an enum
allows -- in the same spelling ``call`` accepts them::

    pytruenas help user.create nas1          # one method
    pytruenas help user nas1                 # the methods of a namespace
    pytruenas help all nas1                  # every namespace, with counts

The source is the **API itself**, per namespace: ``core.get_services`` and
``core.get_methods(<service>)`` declare no roles and need no command access, so
this works for an API-key account with no shell, no SSH and no web shell -- and
one namespace is a small answer (13 methods / 100 KB for ``user`` on 26.0)
rather than the 24 MB the whole definition weighs. Answers are cached per host,
version and service.

``--dump`` reads the full ``middlewared --dump-api`` definition instead. That
needs command access on the target and is only necessary to describe an *older*
API version (``--api-version``), which the live API cannot report.

Either way the source is the definition, not generated ``.pyi`` stubs:
descriptions, defaults, enum values and required-ness exist only in the
definition, and stubs cannot carry them.

``NAME`` is required and comes first, before the targets -- ``query``'s
namespace works the same way. It has to be required: made optional, argparse
gives the lone token of ``pytruenas help nas1`` to ``NAME`` and leaves no
target, so the index form could only ever run against the local socket. ``all``
(or ``.``) is therefore the spelling for "list what there is".
"""

from __future__ import annotations

from logging import Logger

from duho import Arg, NS

from pytruenas import TrueNASClient
from pytruenas.utils import apicache, apihelp
from pytruenas.utils.cmd import PyTrueNASArgs, emit, emit_json


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``help``."""

    # A REQUIRED positional, like `query`'s namespace. Two earlier spellings
    # were both wrong, and the reason is worth keeping:
    #   * declared without the tuple it became `--name`, so `help user.create
    #     nas1` read BOTH words as targets and tried to resolve a host called
    #     "user.create";
    #   * declared `nargs='?'` it made the index form UNREACHABLE -- argparse
    #     gives the lone token of `help nas1` to NAME, leaving no target, and
    #     the target list then defaults to the local socket. The obvious fix,
    #     overriding `_expanded_targets_` here, does nothing: a module command's
    #     fields land on the app ROOT instance (`PyTrueNAS`), which is what
    #     `main` reads the targets off, so this class is not in that MRO.
    # Hence: required, with a sentinel for the index.
    name: str
    """Method (``user.create``) or namespace (``user``) to describe; ``all``
    (or ``.``) lists every namespace."""
    ("name",)  # type: ignore

    #: Spellings of "no particular method -- list what there is".
    INDEX_NAMES = ("all", ".")

    refresh_api: bool = False
    "Re-fetch the API definition instead of using the cache"

    api_version: str = None
    "Describe this API version from the dump (default: the newest)"

    json: bool = False
    "Emit the definition slice as JSON instead of prose, for tooling"

    dump: bool = False
    """Read the full ``middlewared --dump-api`` definition instead of asking the
    API per namespace. Needs command access on the target; only necessary for
    ``--api-version``."""


def _version_from_dump(args: "Args", api: dict, logger: Logger):
    versions = api["versions"]
    # The dump lists versions newest-first; `generate-typings` reads it the same way.
    if not args.api_version:
        return versions[0]
    version = next((v for v in versions if v["version"] == args.api_version), None)
    if version is None:
        logger.error(
            "version %r not found; available: %s",
            args.api_version,
            ", ".join(v["version"] for v in versions),
        )
        return None
    return version


def run(client: TrueNASClient, args: Args, logger: Logger):
    # The default source is the API itself, per namespace: `core.get_methods`
    # and `core.get_services` declare NO roles and need no command access, so
    # this works for an API-key account with no shell, no SSH and no web shell.
    # The full dump needs a shell and is 24 MB, so it is opt-in (`--dump`) and
    # only really needed to describe an OLDER api version.
    use_dump = args.dump or bool(args.api_version)
    name = args.name

    if not use_dump:
        try:
            return _from_api(client, args, logger, name)
        except LookupError as exc:
            logger.error("%s", exc)
            return 2

    api = apicache.load(client, refresh=args.refresh_api)
    version = _version_from_dump(args, api, logger)
    if version is None:
        return 2

    if name in Args.INDEX_NAMES:
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


def _from_api(client: TrueNASClient, args: "Args", logger: Logger, name: str):
    """Describe ``name`` using ``core.get_services``/``core.get_methods``.

    No command access and no roles required. ``core.get_methods`` filters by
    **service**, so a dotted method name is split into "the namespace to ask
    for" and "the method to render" -- and a name that is itself a service is
    listed whole.
    """
    if name in Args.INDEX_NAMES:
        found = apicache.services(client, refresh=args.refresh_api)
        if args.json:
            emit_json(sorted(found), args)
        else:
            emit(_render_services(found).rstrip("\n"))
        return 0

    services = apicache.services(client, refresh=args.refresh_api)

    # `name` is either a service itself, or <service>.<method>.
    service = name if name in services else name.rpartition(".")[0]
    if service not in services:
        import difflib

        close = difflib.get_close_matches(service or name, list(services), n=5)
        hint = f"; did you mean: {', '.join(close)}" if close else ""
        raise LookupError(f"no service named {service or name!r}{hint}")

    methods = apihelp.methods_from_get_methods(
        apicache.service_methods(client, service, refresh=args.refresh_api)
    )

    if name in methods:
        if args.json:
            emit_json(methods[name], args)
        else:
            emit(apihelp.render(name, methods[name]).rstrip("\n"))
        return 0

    if name == service:
        version = {
            "version": str(client.api.system.info()["version"]),
            "methods": list(methods.values()),
        }
        if args.json:
            emit_json(methods, args)
        else:
            emit(apihelp.render_namespace(version, service).rstrip("\n"))
        return 0

    import difflib

    close = difflib.get_close_matches(name, list(methods), n=5)
    hint = f"; did you mean: {', '.join(close)}" if close else ""
    raise LookupError(f"no method named {name!r} in {service}{hint}")


def _render_services(found: "dict") -> str:
    """The service index from ``core.get_services``."""
    names = sorted(found)
    out = [f"{len(names)} services (namespaces)", ""]
    width = max((len(n) for n in names), default=1)
    for name in names:
        entry = found[name] or {}
        kind = entry.get("type") or ""
        out.append(f"  {name:<{width}}  {kind}".rstrip())
    out.append("")
    out.append("Try: pytruenas help <service>   or   pytruenas help <service>.<method>")
    return "\n".join(out) + "\n"
