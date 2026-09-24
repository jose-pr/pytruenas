"""Call an arbitrary TrueNAS middleware method and print its JSON result.

Unlike ``query`` (which only covers queryable ``<namespace>.query`` methods),
``call`` invokes any method by its dotted name, e.g. ``system.info``,
``core.ping``, ``pool.dataset.details``. Parameters are passed with ``-p`` as
JSON values (repeatable), so the trailing positionals stay the target host(s).

**Fields after a literal ``--``.** Hand-writing ``-p '{"username": "svc", ...}'``
is the reason this command was unpleasant for anything that writes, so the
method's own schema is used instead::

    pytruenas call user.create nas1 -- --username=svc --full_name='Svc' --group_create=true

``--name=value`` and bare ``name=value`` are interchangeable there. The
separator is what makes this unambiguous: the valid field names are only known
after the method name is parsed, so arbitrary top-level ``--flags`` would
collide with the global options (a middleware field named ``config`` or
``parallel`` would be unreachable). Targets come before the separator, as they
do for ``deploy``.

Fields fill the **last object-typed parameter** -- the payload -- so a method
taking ``(id, payload)`` still reads its id from ``-p``::

    pytruenas call user.update -p 1 nas1 -- --full_name='New name'

Field names, types, defaults and enum values come from the cached API
definition; ``pytruenas help <method>`` prints them.

Any ordering of ``-p`` relative to ``method``/the trailing targets now parses,
including between them (``pytruenas call method -p '{"a": 1}' nas1``) -- as of
duho >=0.5.1, whose flag-between-positionals reorder fix extends to a module
command's subparser (this one); 0.5.0 alone only covered duho's own
declarative ``_subcommands_`` tree. Earlier duho versions required ``-p``
before ``method`` or after the targets; see the duho finding
``2026-07-24_module_command_subparsers_bypass_positional_reorder.md`` for the
history if this regresses.
"""

from __future__ import annotations

from logging import Logger

from duho import Arg, NS

from pytruenas import TrueNASClient
from pytruenas.utils import apihelp, fields as _fields
from pytruenas.utils.cmd import PyTrueNASArgs, emit_json, json_value


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``call`` (added ahead of the trailing targets)."""

    method: str
    "Method to call, e.g. system.info or core.ping"
    ("method",)  # type: ignore

    # duho >=0.5.0 defaults a list-typed OPTION to action="append", nargs=None
    # (one value per occurrence, `-p a -p b`) -- no explicit override needed.
    params: "Arg[list[str], NS(metavar='JSON')]" = []
    """A parameter as a JSON value (repeatable); a value that is not valid JSON
    is passed as a plain string."""
    ("--param", "-p")  # type: ignore

    refresh_api: bool = False
    """Re-fetch the API definition instead of using the cache (only needed when
    the appliance was upgraded in place)."""

    no_schema: bool = False
    """Do not consult the API definition: field values are then typed the way
    ``-p`` is (a JSON value, else a string) and no name is validated."""


def _schema_fields(client: TrueNASClient, args: Args, logger: Logger):
    """``(fields, payload_index)`` for ``args.method``, or ``({}, None)``.

    Asks the API for just this method's **service**
    (``core.get_methods(<service>)``): it declares no roles and needs no command
    access, so it works for an API-key account with no shell -- and one
    namespace is a small answer rather than the 24 MB whole definition.

    Failing to read the schema is a warning, not an error: the untyped path
    still works, and refusing to call because help metadata is unavailable would
    be worse than calling. A field name that does not exist is still caught --
    by the appliance's own validation rather than locally.
    """
    from pytruenas.utils import apicache

    service = args.method.rpartition(".")[0]
    if not service:
        return {}, None
    try:
        found = apicache.service_methods(client, service, refresh=args.refresh_api)
        method = apihelp.from_get_methods(args.method, found[args.method])
    except KeyError:
        import difflib

        close = difflib.get_close_matches(args.method, list(found), n=5)
        hint = f"; did you mean: {', '.join(close)}" if close else ""
        raise apihelp.UnknownMethod(f"no method named {args.method!r}{hint}") from None
    except apihelp.UnknownMethod:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "Could not read %s's schema (%s); typing fields as plain JSON", service, exc
        )
        return {}, None
    return apihelp.fields(method), apihelp.payload_index(method)


def run(client: TrueNASClient, args: Args, logger: Logger):
    params = [json_value(p) for p in (args.params or [])]
    tokens = list(getattr(args, "_passthrough_", None) or [])

    payload = None
    if tokens:
        schema: "dict" = {}
        index = None
        if not args.no_schema:
            try:
                schema, index = _schema_fields(client, args, logger)
            except apihelp.UnknownMethod as exc:
                logger.error("%s", exc)
                return 2
        try:
            if schema:
                payload = _fields.collect(tokens, schema)
            else:
                # No schema to check against: same rule as `-p`.
                payload = {}
                for token in tokens:
                    name, raw = _fields.split(token)
                    payload[name] = json_value(raw)
        except _fields.FieldError as exc:
            # Nothing is called: a wrong field name or value must not reach the
            # appliance as a partial payload.
            logger.error("%s", exc)
            return 2

        # Place the payload where the method wants it. With no schema (or a
        # method whose parameters we could not read) it goes last, which is
        # where a create/update payload sits.
        if index is None:
            params.append(payload)
        else:
            while len(params) < index:
                params.append(None)
            params.insert(index, payload)

    logger.info(
        "Calling %s with %d param(s)%s",
        args.method,
        len(params),
        f" and {len(payload)} field(s)" if payload else "",
    )
    result = client.api[args.method](*params)
    # default=str so ejson-decoded datetimes/sets serialize instead of raising.
    emit_json(result, args)
