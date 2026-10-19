"""Call any middleware method by its dotted name and print the JSON result.

Parameters are JSON values given with -p (repeatable); a value that is not
JSON is sent as a string. For a method that takes an object, give its fields
after a literal --, as --name=value or name=value: each is typed from the
method's schema (`pytruenas help METHOD` lists them) and fills the last object
parameter, so `call user.update -p 1 nas1 -- --full_name=x` still takes its id
from -p. Targets go before the --.
"""

from __future__ import annotations

from logging import Logger

from duho import Arg, Meta

from pytruenas import TrueNASClient
from pytruenas.utils import apihelp, fields as _fields
from pytruenas.utils.cmd import PyTrueNASArgs, emit_json, json_value

# Fields come after a literal `--` because their names are only known once the
# method is parsed: as top-level options they would collide with the global
# ones (a field named `config` or `parallel` would be unreachable).
_allow_passthrough_ = True


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``call`` (added ahead of the trailing targets)."""

    method: str
    "Method to call, e.g. system.info or core.ping"
    ("method",)  # type: ignore

    # duho >=0.5.0 defaults a list-typed OPTION to action="append", nargs=None
    # (one value per occurrence, `-p a -p b`) -- no explicit override needed.
    params: "Arg[list[str], Meta(metavar='JSON')]" = []
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
        entry = found.get(args.method)
        method = None if entry is None else apihelp.from_get_methods(args.method, entry)
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "Could not read %s's schema (%s); typing fields as plain JSON", service, exc
        )
        return {}, None
    if method is None:
        import difflib

        close = difflib.get_close_matches(args.method, list(found), n=5)
        hint = f"; did you mean: {', '.join(close)}" if close else ""
        raise apihelp.UnknownMethod(f"no method named {args.method!r}{hint}")
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
    emit_json(result, args)
