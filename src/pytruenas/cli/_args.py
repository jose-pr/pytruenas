"""The CLI's global options, its config file, and the result writers.

``pytruenas`` commands are plain modules that expose:

* ``run(client, args, logger)`` -- required; the command body, called once per
  target with a connected :class:`~pytruenas.TrueNASClient`.
* ``register(parser, args, logger)`` -- optional; add argparse arguments.
* ``validate_args(args)`` -- optional; called once before any target runs.
  Raising :class:`duho.UsageError` ends the run with its message and exit
  status 2.
* ``init(args, logger) -> client`` / ``success(client, args, logger)`` /
  ``finally_(client, args, logger)`` -- optional lifecycle hooks.

The app parses global options into :class:`PyTrueNASArgs`, then for each
target fans out and invokes the selected command's ``run`` with a per-target
client and logger.
"""

from __future__ import annotations

import datetime as _dt
import json as _json
import os as _os
import re as _re
import sys as _sys
import threading as _threading
import typing as _ty
from pathlib import Path as _Path

import anycfg
from duho import Arg, LoggingArgs, Meta, UsageError, expand

from .._utils.env import ENV
from ..auth import Credentials
from .. import host as _host
from ..target import Target, redact


def json_value(raw: str):
    """A CLI value as its JSON type, falling back to the raw string.

    Shared by ``call -p`` and ``query -f``: a filter value is otherwise always
    a string, so a filter on a numeric or boolean field silently matches
    nothing (``-f uid=0`` compares ``"0"`` against ``0``).
    """
    try:
        return _json.loads(raw)
    except (ValueError, TypeError):
        return raw


def split_assignment(token: str) -> "tuple[str, str]":
    """``NAME=VALUE`` -> ``(name, value)``; raises :class:`ValueError` otherwise.

    The one spelling every value-taking option in this CLI uses -- ``query -f``,
    and the ``--field=value`` fields ``call`` accepts after a literal ``--``. A
    leading ``--`` is stripped so both spellings of a field are the same token.
    An empty name or a missing ``=`` is refused rather than guessed: a field
    always needs a value, booleans included, because the middleware
    distinguishes ``false`` from "not sent".
    """
    raw = token[2:] if token.startswith("--") else token
    name, sep, value = raw.partition("=")
    if not sep or not name:
        raise ValueError(
            f"expected NAME=VALUE, got {token!r} "
            "(a value is always required, booleans included: name=false)"
        )
    return name, value


#: Serializes result writes. `print()` is two writes (the text, then the
#: newline), so under `--parallel` two targets' JSON interleaved mid-line and
#: neither line parsed.
_WRITE_LOCK = _threading.Lock()


def json_default(obj):
    """JSON fallback for what the middleware sends back.

    A set becomes a sorted list, a date or time its ISO string, bytes text;
    anything else its ``str()``. Each is a value JSON can read back, which a
    Python repr (``"{1, 2}"``) is not.
    """
    if isinstance(obj, (set, frozenset)):
        return sorted(obj, key=str)
    if isinstance(obj, (_dt.datetime, _dt.date, _dt.time)):
        return obj.isoformat()
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode("utf-8", "replace")
    return str(obj)


def emit(text: str) -> None:
    """Write one result line to stdout atomically."""
    with _WRITE_LOCK:
        _sys.stdout.write(text + "\n")
        _sys.stdout.flush()


def emit_json(value: object, args: "PyTrueNASArgs | None" = None) -> None:
    """Write ``value`` as one JSON line, attributed when fanning out.

    With more than one target the lines are interleaved and were
    indistinguishable, so each becomes ``{"target": ..., "result": ...}``. A
    single target keeps the bare result, which is what scripts already parse.
    """
    target = getattr(args, "target", None)
    if target is not None and args is not None and len(args._expanded_targets_()) > 1:
        value = {"target": redact(str(target)), "result": value}
    emit(_json.dumps(value, default=json_default))


def default_config_path() -> _Path:
    """Where the CLI's config file is when nothing names one.

    ``pytruenas.cfg`` in the platform's configuration directory:
    ``%APPDATA%`` on Windows, ``$XDG_CONFIG_HOME`` or ``~/.config`` elsewhere.
    """
    if _sys.platform == "win32" and _os.environ.get("APPDATA"):
        base = _Path(_os.environ["APPDATA"])
    else:
        base = _Path(_os.environ.get("XDG_CONFIG_HOME") or _Path.home() / ".config")
    return base / "pytruenas.cfg"


_TARGETS_HELP = (
    "Target host(s) as trailing arguments; comma-separated and "
    "[A-Z]/[0-9] range patterns supported. Defaults to localhost."
)

#: The ``targets`` field every command declares as its last field.
TargetsField = Arg[
    list[str], Meta(flags=("targets",), metavar="TARGET", help=_TARGETS_HELP)
]


def with_targets(args_cls: "type | None" = None) -> type:
    """``args_cls`` (default :class:`PyTrueNASArgs`) with ``targets`` declared last.

    A field declared by a subclass comes after its base's fields, so the hosts
    stay the trailing positionals (``pytruenas query <namespace> <host>...``),
    and a declared field is also what duho publishes in a command's MCP tool
    schema -- a positional added in a ``register`` hook is not.
    The app applies this to every module command.
    """
    base = args_cls if args_cls is not None else PyTrueNASArgs
    namespace = {
        "__annotations__": {"targets": TargetsField},
        "targets": [],
        "__module__": base.__module__,
        "__qualname__": base.__qualname__,
        "__doc__": base.__doc__,
        # A class built by type() has no source for duho to read field
        # docstrings from; the help comes from the Meta above.
        "_duho_constants_": {},
    }
    return type(base.__name__, (base,), namespace)


class PyTrueNASArgs(LoggingArgs):
    """Global options shared by every ``pytruenas`` command.

    A data mixin (``LoggingArgs``): it carries the global fields and config
    loading; :class:`pytruenas.cli.PyTrueNAS` combines it with ``duho.Cli`` to
    make the runnable app root.
    """

    # A path, not a `dict` (duho gives a dict-typed option a KEY=VALUE action);
    # `None` until resolved by `_config_path_()`, so `$PYTRUENAS_CONFIG` is
    # read when the file is needed, not when this module is imported.
    config: "Arg[_ty.Optional[_Path], Meta(metavar='FILE')]" = None
    "Config file (default: $PYTRUENAS_CONFIG, else pytruenas.cfg in the user's config directory)"
    ("--config", "-c")  # type: ignore

    # Repeated, never split: a separator character would cut a Windows
    # drive letter (`C:\...`) out of its path.
    cmdspath: "Arg[list[str], Meta(metavar='SOURCE')]" = []
    "A directory or package to search for commands (repeatable; also $PYTRUENAS_PATH)"
    ("--cmdspath",)  # type: ignore

    insecure: bool = False
    "Do not verify the server's TLS certificate or SSH host key (curl's -k)"
    ("--insecure", "-k")  # type: ignore

    ca_bundle: "Arg[_ty.Optional[str], Meta(metavar='FILE')]" = None
    "Trust this CA bundle (a PEM file or hashed directory) instead of the OS"
    ("--ca-bundle",)  # type: ignore

    # The trailing positionals, declared by each command as its LAST field
    # (`with_targets`). Unannotated on purpose: any annotation here, even
    # ClassVar, would fix the field's position ahead of the command's own.
    targets = []  # type: list[str]

    parallel: int = 1
    "Number of targets to operate on concurrently"

    logto: str = "-"
    "Where to log: '-' for stderr, or a path template (supports {target}, {isodate})"

    def _config_path_(self) -> "tuple[_Path, bool]":
        """The config file, and whether it must exist.

        ``--config``, else ``$PYTRUENAS_CONFIG`` -- either must exist, since a
        typo there would drop its credentials and TLS settings without a word
        -- else :func:`default_config_path`, read only when present.
        """
        if self.config is not None:
            return _Path(self.config), True
        named = ENV.get("CONFIG")
        if named:
            return _Path(named), True
        return default_config_path(), False

    def _config_dict_(self) -> dict:
        """The settings in the config file, read by ``anycfg.load``.

        ``{}`` when the default file is absent. A named file that is missing is
        a :class:`duho.UsageError`; one that does not read, an
        ``anycfg.ConfigError``.
        """
        path, required = self._config_path_()
        if not path.exists():
            if required:
                raise UsageError(f"config file not found: {path}")
            return {}
        return anycfg.load(path) or {}

    def _verify_(self) -> "bool | str":
        """``verify=`` for the clients this CLI builds.

        Each layer in turn -- the flags, then ``$PYTRUENAS_INSECURE`` /
        ``$PYTRUENAS_CA_BUNDLE``, then the config file's ``insecure`` /
        ``ca_bundle`` -- can turn verification off or name a CA bundle; the
        first that does wins. With none, ``True``: the OS trust. Only a true
        value turns it off (``ENV.bool``; a config ``insecure = true``), so a
        value that is not one leaves it on.
        """
        config = self._config_dict_()
        where = self._config_path_()[0]
        layers = (
            (self.insecure, self.ca_bundle, "--ca-bundle"),
            (
                ENV.bool("INSECURE"),
                ENV.get("CA_BUNDLE") or None,
                f"${ENV.prefix}CA_BUNDLE",
            ),
            (
                config.get("insecure") is True,
                config.get("ca_bundle") or None,
                f"ca_bundle in {where}",
            ),
        )
        for insecure, bundle, source in layers:
            if insecure:
                return False
            if bundle is not None:
                if not isinstance(bundle, str) or not _os.path.exists(bundle):
                    raise ValueError(f"{source}: no CA bundle at {bundle!r}")
                return bundle
        return True

    def _credentials_(self) -> object:
        """Credentials for a target that carries none.

        ``$PYTRUENAS_CREDENTIALS`` (as :meth:`Credentials.from_env` reads it),
        else the config file's ``credentials`` -- a connection string or a
        mapping of keyword arguments. ``None`` when neither is set, which is
        what a local socket wants.
        """
        raw: object = ENV.get("CREDENTIALS")
        if not raw:
            raw = self._config_dict_().get("credentials")
        if not raw:
            return None
        if isinstance(raw, _ty.Mapping):
            return Credentials(**raw)
        return Credentials(raw)

    def _client_(self, target: str) -> "_host.TrueNASClient":
        """The client this CLI builds for one target.

        One place, so a plain command and a RunPath step connect alike: TLS
        per :meth:`_verify_`, and credentials from the environment or the
        config file only when the target itself carries none (passing both
        raises).
        """
        credentials = None
        if not Target.parse(target, resolve_port=False).password:
            credentials = self._credentials_()
        return _host.TrueNASClient(
            target, credentials=credentials, verify=self._verify_()
        )

    def _expanded_targets_(self) -> "list[str]":
        """Return the target list with commas split and range patterns expanded.

        Targets arrive as the trailing positionals (a flat ``list[str]``); each
        item may itself be a comma-separated list (``nas1,nas2``) and/or carry a
        ``[A-Z]``/``[0-9]`` range pattern. An empty list defaults to
        ``localhost``.
        """
        return [
            target
            for item in self.targets or ["localhost"]
            for target in _expand_target(item)
        ]


def _split_userinfo(target: str) -> "tuple[str, str]":
    """``(prefix, hostpart)`` where ``prefix`` is scheme + userinfo, if any.

    Everything up to and including the last ``@`` of the authority is
    credentials, and nothing in it is target syntax.
    """
    scheme, sep, tail = target.partition("://")
    # Without a scheme, partition puts everything in the first field.
    prefix, rest = (scheme + sep, tail) if sep else ("", target)
    if "@" not in rest:
        return prefix, rest
    # The authority ends at the first "/", "?" or "#"; an "@" after that belongs
    # to a path, not to userinfo.
    end = next((i for i, ch in enumerate(rest) if ch in "/?#"), len(rest))
    if "@" not in rest[:end]:
        return prefix, rest
    userinfo, _, hostpart = rest[:end].rpartition("@")
    return prefix + userinfo + "@", hostpart + rest[end:]


#: A comma followed by a scheme starts another target: `wss://a,ws://b`.
_NEXT_TARGET = _re.compile(r",(?=[A-Za-z][A-Za-z0-9+.-]*://)")


def _expand_target(item: str) -> "list[str]":
    """One positional into its targets, expanding only the HOST part.

    A comma separates targets and ``[A-Z]``/``[0-9]`` is a range -- but only
    outside the credentials. Running either over the whole string turned
    ``wss://root:pw,with,commas@nas`` into three bogus targets and made
    ``root:secret@nas1,nas2`` a second target with no credentials at all.
    A part with its own scheme (``wss://nas1,ws://nas2``) or its own user
    (``nas1,root:pw@nas2``) is a target of its own; the hosts that follow a
    part's credentials share them.
    """
    return [
        target for chunk in _NEXT_TARGET.split(item) for target in _expand_one(chunk)
    ]


def _expand_one(item: str) -> "list[str]":
    prefix, hostpart = _split_userinfo(item)
    scheme, sep, userinfo = prefix.partition("://")
    scheme, userinfo = (scheme + sep, userinfo) if sep else ("", prefix)
    # A comma in the user name (before the password's ":") ends earlier hosts:
    # a user name holds no comma, a password may.
    leading, comma, _ = userinfo.partition(":")[0].rpartition(",")
    if comma:
        userinfo = userinfo[len(leading) + 1 :]
    hosts = [
        scheme + host for part in leading.split(",") if part for host in expand(part)
    ]
    parts = [part for part in hostpart.split(",") if part]
    return hosts + [scheme + userinfo + host for part in parts for host in expand(part)]


__all__ = [
    "PyTrueNASArgs",
    "TargetsField",
    "with_targets",
    "default_config_path",
    "json_default",
    "emit",
    "emit_json",
]
