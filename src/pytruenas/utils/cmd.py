"""CLI argument classes and the command-module contract.

``pytruenas`` commands are plain modules that expose:

* ``run(client, args, logger)`` -- required; the command body, called once per
  target with a connected :class:`~pytruenas.TrueNASClient`.
* ``register(parser, args, logger)`` -- optional; add argparse arguments.
* ``validate_args(args)`` -- optional; called once before any target runs.
  Raising :class:`duho.UsageError` ends the run with its message and exit
  status 2.
* ``init(args, logger) -> client`` / ``success(client, args, logger)`` /
  ``finally_(client, args, logger)`` -- optional lifecycle hooks.

The app (see :mod:`pytruenas.main`) parses global options into
:class:`PyTrueNASArgs`, then for each target fans out and invokes the selected
command's ``run`` with a per-target client and logger. Argument parsing and
command discovery are provided by :mod:`duho`; the per-target fan-out and the
client/logger threading are ``pytruenas``-specific and live here + in
:mod:`pytruenas.main`.
"""

from __future__ import annotations

import logging as _pylogging
import os as _os
import re as _re
import threading as _threading
import typing as _ty
from logging import Logger as _Logger
from pathlib import Path as _Path


from duho import Arg, Extend, LoggingArgs, Meta
from duho.env import Env as _Env


def json_value(raw: str):
    """A CLI value as its JSON type, falling back to the raw string.

    Shared by ``call -p`` and ``query -f``: a filter value is otherwise always
    a string, so a filter on a numeric or boolean field silently matches
    nothing (``-f uid=0`` compares ``"0"`` against ``0``).
    """
    import json

    try:
        return json.loads(raw)
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
    import datetime

    if isinstance(obj, (set, frozenset)):
        return sorted(obj, key=str)
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode("utf-8", "replace")
    return str(obj)


def emit(text: str) -> None:
    """Write one result line to stdout atomically."""
    import sys

    with _WRITE_LOCK:
        sys.stdout.write(text + "\n")
        sys.stdout.flush()


def emit_json(value: object, args: "PyTrueNASArgs | None" = None) -> None:
    """Write ``value`` as one JSON line, attributed when fanning out.

    With more than one target the lines are interleaved and were
    indistinguishable, so each becomes ``{"target": ..., "result": ...}``. A
    single target keeps the bare result, which is what scripts already parse.
    """
    import json

    target = getattr(args, "target", None)
    if target is not None and args is not None and len(args._expanded_targets_()) > 1:
        from .target import redact

        value = {"target": redact(str(target)), "result": value}
    emit(json.dumps(value, default=json_default))


if _ty.TYPE_CHECKING:
    from ..host import TrueNASHost as TrueNASClient

#: Every ``PYTRUENAS_*`` setting, read through one accessor.
#:
#: Reading ``os.environ`` directly at each site is how this app ended up with
#: three names for two settings (``PYTRUENAS_CFG`` here, ``PYTRUENAS_CONFIG``
#: in ``ops``, ``PYTRUENAS_PATH`` in ``main``) -- a prefixed accessor makes the
#: full set enumerable (``list(ENV)``) instead of something you find by
#: grepping. ``.paths()`` also splits on ``os.pathsep`` rather than a hardcoded
#: separator, so a Windows ``C:\...`` entry is not mis-split on its drive
#: colon.
#:
#: ``autoload=False``: the companion-module feature would import a
#: ``pytruenas_env`` module from anywhere on ``sys.path``, including the CWD.
#: This app ships no such defaults, so the import is pure attack surface --
#: and a CLI is routinely run from a directory the user does not control.
ENV = _Env("pytruenas", autoload=False)


def _load_config(path: "_Path") -> dict:
    """Load a YAML config file, or return ``{}`` if it does not exist.

    YAML support is optional (the ``config`` extra); a missing ``pyyaml`` with a
    present config file is a clear, actionable error rather than a silent skip.
    """
    if not path.exists():
        return {}
    try:
        import yaml
    except ImportError as exc:
        from hostctl import MissingExtraError

        raise MissingExtraError(
            "config", f"reading the config file {path}", distribution="pytruenas"
        ) from exc
    # read_bytes(), not read_text(): PyYAML detects UTF-8/16 itself, while
    # read_text() uses the locale encoding and raised UnicodeDecodeError on a
    # UTF-8 config file under a cp1252 default.
    loaded = yaml.safe_load(path.read_bytes()) or {}
    if not isinstance(loaded, dict):
        _pylogging.getLogger("pytruenas").warning(
            "ignoring config %s: expected a mapping, got %s",
            path,
            type(loaded).__name__,
        )
        return {}
    return loaded


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
    :func:`pytruenas.main._with_targets` applies this to every module command.
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


def register_targets(parser) -> None:
    """Add the trailing ``targets`` positional to a parser imperatively.

    Commands no longer need it: :func:`with_targets` declares the positional,
    which also puts it in the MCP tool schema. Kept for code that builds its
    own parser.
    """
    parser.add_argument("targets", nargs="*", metavar="TARGET", help=_TARGETS_HELP)


def _env_bool(name: str) -> bool:
    """``$PYTRUENAS_<name>`` as a boolean; unset or empty is ``False``."""
    from duho.text import parse_bool

    value = ENV.get(name)
    if not value or not value.strip():
        return False
    try:
        return parse_bool(value)
    except ValueError:
        raise ValueError(
            f"${ENV.prefix}{name} is {value!r}: expected true or false"
        ) from None


def _config_bool(config: "_ty.Mapping[str, object]", key: str, path: object) -> bool:
    value = config.get(key, False)
    if not isinstance(value, bool):
        raise ValueError(f"{key} in {path} must be true or false, not {value!r}")
    return value


class PyTrueNASArgs(LoggingArgs):
    """Global options shared by every ``pytruenas`` command.

    A data mixin (``LoggingArgs``): it carries the global fields and config
    loading; :class:`pytruenas.main.PyTrueNAS` combines it with ``duho.Cli`` to
    make the runnable app root.
    """

    # `CONFIG` first, `CFG` for compatibility: both spellings existed (`CFG`
    # here, `CONFIG` in `ops.main`), which is exactly the drift a single
    # accessor is meant to stop. `CONFIG` wins as the spelled-out name.
    # A PATH field, not `dict`: duho hands a dict-typed option its KEY=VALUE
    # UpdateAction, so every `--config file.yaml` died in argparse
    # ("'WindowsPath' object is not iterable") before a command could run.
    # `_config_dict_()` is what turns it into the mapping.
    config: "Arg[_Path, Meta(metavar='FILE')]" = _Path(
        ENV.get("CONFIG") or ENV.get("CFG") or "./pytruenas.yaml"
    )
    "Config file to use"
    ("--config", "-c")  # type: ignore

    cmdspath: "Arg[list[str], Extend(':')]" = []
    "Extra directories/packages to search for commands"
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

    def _config_dict_(self) -> dict:
        """Return the loaded config mapping.

        Empty when the implicit ``./pytruenas.yaml`` is absent. A file named
        with ``--config`` or ``$PYTRUENAS_CONFIG`` must exist: a typo there
        would otherwise drop its credentials and TLS setting without a word.
        Raises :class:`duho.UsageError` (exit status 2) when it does not.
        """
        config = self.config
        if isinstance(config, _Path):
            if not config.exists() and not self._config_is_implicit_():
                from duho import UsageError

                raise UsageError(f"config file not found: {config}")
            return _load_config(config)
        return config or {}

    def _config_is_implicit_(self) -> bool:
        """Whether the config file was found rather than asked for.

        ``./pytruenas.yaml`` in the process's working directory is a default,
        and a CLI is routinely run from a directory its user does not control.
        Which matters for two things: an implicit file may be absent, and its
        ``commandspath`` (i.e. "import code from here") is refused while its
        ``credentials`` and TLS settings are still read. Same reasoning as
        ``ENV``'s ``autoload=False``.
        """
        if ENV.get("CONFIG") or ENV.get("CFG"):
            return False
        # Through the MRO: the parsed instance is the app root, a subclass that
        # does not redeclare the field.
        default = next(
            (
                k.__dict__["config"]
                for k in type(self).__mro__
                if "config" in k.__dict__
            ),
            None,
        )
        if default is None:  # pragma: no cover - the field always has a default
            return False
        return _Path(self.config) == _Path(default)

    def _verify_(self) -> "bool | str":
        """``verify=`` for the clients this CLI builds.

        Each layer in turn -- the flags, then ``$PYTRUENAS_INSECURE`` /
        ``$PYTRUENAS_CA_BUNDLE``, then the config file's ``insecure`` /
        ``ca_bundle`` -- can turn verification off or name a CA bundle; the
        first that does wins. With none, ``True``: the OS trust. An empty
        variable is unset.
        """
        if ENV.get("SSLVERIFY"):
            raise ValueError(
                f"${ENV.prefix}SSLVERIFY was replaced by ${ENV.prefix}INSECURE "
                f"and ${ENV.prefix}CA_BUNDLE"
            )
        config = self._config_dict_()
        if "sslverify" in config:
            raise ValueError(
                f"sslverify in {self.config} was replaced by insecure and ca_bundle"
            )
        layers = (
            (self.insecure, self.ca_bundle, "--ca-bundle"),
            (
                _env_bool("INSECURE"),
                ENV.get("CA_BUNDLE") or None,
                f"${ENV.prefix}CA_BUNDLE",
            ),
            (
                _config_bool(config, "insecure", self.config),
                config.get("ca_bundle") or None,
                f"ca_bundle in {self.config}",
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

        ``$TN_CREDS`` (the spelling :meth:`Credentials.from_env` documents),
        else the config file's ``credentials`` -- a connection string or a
        mapping of keyword arguments. ``None`` when neither is set, which is
        what a local socket wants.
        """
        from ..auth import Credentials

        raw: object = _os.environ.get("TN_CREDS")
        if not raw:
            raw = self._config_dict_().get("credentials")
        if not raw:
            return None
        if isinstance(raw, _ty.Mapping):
            return Credentials(**raw)
        return Credentials(raw)

    def _client_(self, target: str) -> "TrueNASClient":
        """The client this CLI builds for one target.

        One place, so a plain command and a RunPath step connect alike: TLS
        per :meth:`_verify_`, and credentials from the environment or the
        config file only when the target itself carries none (passing both
        raises).
        """
        from ..host import TrueNASHost
        from .target import Target

        credentials = None
        if not Target.parse(target, resolve_port=False).password:
            credentials = self._credentials_()
        return TrueNASHost(target, credentials, verify=self._verify_())

    def _expanded_targets_(self) -> "list[str]":
        """Return the target list with commas split and range patterns expanded.

        Targets arrive as the trailing positionals (a flat ``list[str]``); each
        item may itself be a comma-separated list (``nas1,nas2``) and/or carry a
        ``[A-Z]``/``[0-9]`` range pattern. An empty list defaults to
        ``localhost``. Flattens defensively in case a nested list slips through.
        """
        from duho import expand

        def _flatten(values):
            for value in values:
                if isinstance(value, (list, tuple)):
                    yield from _flatten(value)
                else:
                    yield value

        items = list(_flatten(self.targets)) or ["localhost"]
        expanded: "list[str]" = []
        for item in items:
            expanded.extend(_expand_target(str(item), expand))
        return expanded


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


def _expand_target(item: str, expand) -> "list[str]":
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
        target
        for chunk in _NEXT_TARGET.split(item)
        for target in _expand_one(chunk, expand)
    ]


def _expand_one(item: str, expand) -> "list[str]":
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


class CommandModule(_ty.Protocol):
    """The attributes the app expects from a command module."""

    def run(
        self, client: "TrueNASClient", args: PyTrueNASArgs, logger: _Logger
    ) -> object: ...


__all__ = [
    "PyTrueNASArgs",
    "TargetsField",
    "with_targets",
    "register_targets",
    "CommandModule",
    "json_value",
    "json_default",
    "emit",
    "emit_json",
]
