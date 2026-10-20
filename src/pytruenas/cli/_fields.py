"""Turn ``--field=value`` text into the JSON values a middleware method wants.

The alternative to ``-p '{"username": "svc", ...}'`` -- hand-written JSON,
quoted twice through a shell: given a property's schema from the API
definition, this casts one command-line string to the right JSON type, and
says so clearly when it cannot.

Two rules are deliberate, both because silence is the expensive failure:

* **An unknown field is an error**, listing near-misses. A dropped field would
  change the call's meaning without a word: a dropped filter queries every row.
* **A bad enum value names the valid ones.** The appliance's own error for a
  bad enum is a validation failure with a schema path, which is much harder to
  act on than a list of the five strings it accepts.

Fields come after a literal ``--``, and ``--name=value`` and bare
``name=value`` are interchangeable there.
"""

from __future__ import annotations

import json as _json
import pathlib as _pathlib
import typing as _ty

from duho.text import BOOL_FALSE as _BOOL_FALSE
from duho.text import BOOL_TRUE as _BOOL_TRUE

from .._utils import schema as _schema
from ..exceptions import FieldError

#: Accepted spellings for a boolean: duho's sets, without its empty "false",
#: so ``--flag=`` is an error rather than a quiet ``false``.
TRUE = _BOOL_TRUE
FALSE = _BOOL_FALSE - {""}

#: Suffix that forces a raw JSON value: ``filters:json=[["id","=",1]]``.
JSON_SUFFIX = ":json"


def split(token: str) -> "tuple[str, str]":
    """``--name=value`` or ``name=value`` -> ``(name, value)``.

    Delegates to ``split_assignment``, the one spelling
    ``query -f`` uses too, so the three places that take a ``NAME=VALUE`` agree
    on what one is.
    """
    from ._args import split_assignment

    try:
        return split_assignment(token)
    except ValueError as exc:
        raise FieldError(str(exc)) from None


def _coerce_scalar(name: str, schema: "_ty.Mapping[str, _ty.Any]", raw: str) -> object:
    declared = schema.get("type")
    types = declared if isinstance(declared, (list, tuple)) else [declared]

    # A null-able field takes an explicit empty value or "null" as null; the
    # middleware treats null as "clear this", which a caller does want to send.
    if raw in ("", "null") and "null" in types:
        return None

    for candidate in types:
        if candidate == "boolean":
            low = raw.strip().lower()
            if low in TRUE:
                return True
            if low in FALSE:
                return False
            continue
        if candidate == "integer":
            try:
                return int(raw, 10)
            except ValueError:
                continue
        if candidate in ("number", "float"):
            try:
                return float(raw)
            except ValueError:
                continue
        if candidate == "string":
            return raw
    if types in ([None], []):
        # No declared type: fall back to the CLI's existing untyped rule, the
        # one `query -f` and `call -p` already use (JSON value, else string).
        from ._args import json_value

        return json_value(raw)
    expected = "|".join(str(t) for t in types if t)
    raise FieldError(f"--{name}: {raw!r} is not a valid {expected}")


def coerce(name: str, schema: "_ty.Any", raw: str) -> object:
    """Cast one raw command-line value per ``schema``."""
    resolved = _schema.unwrap_optional(schema)

    values = _schema.enum_values(resolved)
    if values is not None:
        # Compare as text so `--uid=0` matches an integer enum member, then
        # return the schema's own value (the appliance wants its type).
        for value in values:
            if raw == value or raw == str(value):
                return value
        if raw in ("", "null") and None in values:
            return None
        rendered = ", ".join(repr(v) for v in values)
        raise FieldError(f"--{name}: {raw!r} is not one of: {rendered}")

    declared = resolved.get("type")
    types = declared if isinstance(declared, (list, tuple)) else [declared]

    if "array" in types:
        if raw in ("", "null") and "null" in types:
            return None
        items = resolved.get("items")
        parts = [p for p in raw.split(",")] if raw else []
        if not isinstance(items, dict) or not items:
            return parts
        return [coerce(name, items, part) for part in parts]

    if "object" in types:
        # A whole object on one flag only makes sense as JSON; dotted names
        # (`--options.acl=true`) are assembled by `collect` instead.
        try:
            return _json.loads(raw)
        except ValueError as exc:
            raise FieldError(
                f"--{name} is an object: pass dotted fields "
                f"(--{name}.key=value) or JSON (--{name}:json={{...}})"
            ) from exc

    return _coerce_scalar(name, resolved, raw)


def _resolve(
    fields: "_ty.Mapping[str, _ty.Any]", name: str
) -> "tuple[list[str], _ty.Any]":
    """Walk a dotted name to its schema, returning ``(path, schema)``."""
    parts = name.split(".")
    schema: "_ty.Any" = None
    available: "_ty.Mapping[str, _ty.Any]" = fields
    for index, part in enumerate(parts):
        if part not in available:
            import difflib

            close = difflib.get_close_matches(part, list(available), n=5)
            where = ".".join(parts[:index]) or "this method"
            hint = f"; did you mean: {', '.join(close)}" if close else ""
            raise FieldError(f"unknown field {part!r} for {where}{hint}")
        schema = _schema.unwrap_optional(available[part])
        available = schema.get("properties") or {}
    return parts, schema


def collect(
    tokens: "_ty.Sequence[str]", fields: "_ty.Mapping[str, _ty.Any]"
) -> "dict[str, object]":
    """Build a payload from ``--name=value`` tokens against a field schema.

    * a dotted name nests (``options.acl=true``);
    * a repeated name accumulates into a list, so an array field can be given
      one value per flag as well as comma-separated;
    * ``name:json=<json>`` takes a literal JSON value, the escape hatch for
      anything this coercion cannot express;
    * ``name=@path`` reads the value from a file (trailing newline stripped),
      for a key or a certificate.
    """
    payload: "dict[str, object]" = {}
    seen: "dict[str, int]" = {}

    for token in tokens:
        name, raw = split(token)

        as_json = name.endswith(JSON_SUFFIX)
        if as_json:
            name = name[: -len(JSON_SUFFIX)]

        path, schema = _resolve(fields, name)

        if as_json:
            try:
                value: object = _json.loads(raw)
            except ValueError as exc:
                raise FieldError(
                    f"--{name}{JSON_SUFFIX}: not valid JSON: {exc}"
                ) from exc
        elif raw.startswith("@"):
            source = _pathlib.Path(raw[1:]).expanduser()
            try:
                value = source.read_text(encoding="utf-8").rstrip("\n")
            except OSError as exc:
                raise FieldError(f"--{name}: cannot read {source}: {exc}") from exc
        else:
            value = coerce(name, schema, raw)

        seen[name] = seen.get(name, 0) + 1
        target = payload
        for part in path[:-1]:
            nested = target.setdefault(part, {})
            if not isinstance(nested, dict):
                raise FieldError(
                    f"--{name}: {part!r} was already given a non-object value"
                )
            target = nested
        leaf = path[-1]
        if seen[name] > 1:
            # Repeated: accumulate. The first occurrence may already have been
            # coerced to a list (a comma-separated array), so extend it.
            current = target.get(leaf)
            existing = list(current) if isinstance(current, list) else [current]
            target[leaf] = existing + (
                list(value) if isinstance(value, list) else [value]
            )
        else:
            target[leaf] = value
    return payload
