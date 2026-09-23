"""CLI argument classes and the command-module contract.

``pytruenas`` commands are plain modules that expose:

* ``run(client, args, logger)`` -- required; the command body, called once per
  target with a connected :class:`~pytruenas.TrueNASClient`.
* ``register(parser, args, logger)`` -- optional; add argparse arguments.
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
import threading as _threading
import typing as _ty
from logging import Logger as _Logger
from pathlib import Path as _Path

from argparse import SUPPRESS as _SUPPRESS
from argparse import BooleanOptionalAction as _BooleanOptional

from duho import Arg, Extend, LoggingArgs, NS
from duho.env import Env as _Env

from . import io as _ioutils  # noqa: F401


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


#: Serializes result writes. `print()` is two writes (the text, then the
#: newline), so under `--parallel` two targets' JSON interleaved mid-line and
#: neither line parsed.
_WRITE_LOCK = _threading.Lock()


def json_default(obj):
    """JSON fallback for what the middleware sends back.

    `default=str` turned a set into its Python repr (`"{1, 2}"`) and a datetime
    into whatever `str()` gives, neither of which round-trips as JSON.
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
    except ImportError as exc:  # pragma: no cover - only without the extra
        raise ImportError(
            "reading a config file requires the 'config' extra: "
            "pip install pytruenas[config]"
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


def register_targets(parser) -> None:
    """Add the trailing ``targets`` positional to a command parser.

    Applied centrally -- a command module never calls this itself.
    :func:`pytruenas.main._with_targets` wraps every module command's
    ``register`` hook and calls this *after* it, so the target host(s) are the
    trailing positionals (``pytruenas query <namespace> <host>...``) whatever
    positionals the command added; :class:`~pytruenas.utils.runpath.
    PyTrueNASRunPathArgs` does the same for class/RunPath commands. Targets
    support comma-separated lists and ``[A-Z]``/``[0-9]`` range patterns,
    expanded by ``PyTrueNASArgs._expanded_targets_`` (empty -> ``localhost``).
    """
    parser.add_argument(
        "targets",
        nargs="*",
        metavar="TARGET",
        help="Target host(s) as trailing arguments; comma-separated and "
        "[A-Z]/[0-9] range patterns supported. Defaults to localhost.",
    )


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
    config: "Arg[_Path, NS(metavar='FILE')]" = _Path(
        ENV.get("CONFIG") or ENV.get("CFG") or "./pytruenas.yaml"
    )
    "Config file to use"
    ("--config", "-c")  # type: ignore

    cmdspath: "Arg[list[str], Extend(':')]" = []
    "Extra directories/packages to search for commands"
    ("--cmdspath",)  # type: ignore

    # Tri-state: unset (None) falls through to $PYTRUENAS_SSLVERIFY, then the
    # config file, then the library default. The CLI used to default to False,
    # so every `pytruenas call ... nas` sent its credentials over a connection
    # it did not verify -- the opposite of what the library does.
    # `_ty.Optional`, not `bool | None`: duho evaluates this annotation when
    # the class is built, and a PEP 604 union is a TypeError on the 3.9 floor.
    sslverify: "Arg[_ty.Optional[bool], NS(action=_BooleanOptional, default=None)]" = (
        None
    )
    "Verify the server's TLS certificate (default: yes)"
    ("--sslverify",)  # type: ignore

    insecure: bool = False
    "Do not verify the server's TLS certificate (curl's -k)"
    ("--insecure", "-k")  # type: ignore

    # Targets are supplied as the TRAILING POSITIONAL arguments of the command
    # (after any command-specific positionals), not a -t/--target flag. The
    # positional is added centrally, after each command's own register() hook
    # (main._with_targets), so argparse can split e.g. `query <namespace>
    # <host>...` without the command taking part. SUPPRESS keeps duho from
    # auto-registering this field as a `--targets` option; it only holds the
    # parsed value + default, populated by the imperative positional.
    targets: "Arg[list[str], _SUPPRESS]" = []

    parallel: int = 1
    "Number of targets to operate on concurrently"

    logto: str = "-"
    "Where to log: '-' for stderr, or a path template (supports {target}, {isodate})"

    def _config_dict_(self) -> dict:
        """Return the loaded config mapping (empty when the file is absent)."""
        config = self.config
        if isinstance(config, _Path):
            return _load_config(config)
        return config or {}

    def _config_is_implicit_(self) -> bool:
        """Whether the config file was found rather than asked for.

        ``./pytruenas.yaml`` in the process's working directory is a default,
        and a CLI is routinely run from a directory its user does not control.
        Which matters for one key only -- ``commandspath``, i.e. "import code
        from here" -- so the caller can refuse *that* from an implicit file
        while still reading targets and options from it. Same reasoning as
        ``ENV``'s ``autoload=False``.
        """
        if ENV.get("CONFIG") or ENV.get("CFG"):
            return False
        default = type(self).__dict__.get("config", None)
        if default is None:  # pragma: no cover - the field always has a default
            return False
        return _Path(self.config) == _Path(default)

    def _sslverify_(self) -> "bool | str":
        """TLS verification for clients this CLI builds.

        ``-k``/``--insecure`` wins, then ``--sslverify``/``--no-sslverify``,
        then ``$PYTRUENAS_SSLVERIFY``, then the config file's ``sslverify``,
        then the library default (verify). A string is a CA bundle path, as it
        is for ``TrueNASClient(sslverify=...)``.
        """
        if self.insecure:
            return False
        if self.sslverify is not None:
            return self.sslverify
        value = ENV.get("SSLVERIFY")
        if value is None:
            value = self._config_dict_().get("sslverify")
        if value is None:
            return True
        if isinstance(value, str):
            lowered = value.strip().casefold()
            if lowered in ("1", "true", "yes", "on"):
                return True
            if lowered in ("0", "false", "no", "off", ""):
                return False
            return value  # a CA bundle path
        return bool(value)

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
        per :meth:`_sslverify_`, and credentials from the environment or the
        config file only when the target itself carries none (passing both
        raises).
        """
        from ..host import TrueNASHost
        from .target import Target

        credentials = None
        if not Target.parse(target, resolve_port=False).password:
            credentials = self._credentials_()
        return TrueNASHost(target, credentials, sslverify=self._sslverify_())

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


def _expand_target(item: str, expand) -> "list[str]":
    """One positional into its targets, expanding only the HOST part.

    A comma separates targets and ``[A-Z]``/``[0-9]`` is a range -- but only
    outside the credentials. Running either over the whole string turned
    ``wss://root:pw,with,commas@nas`` into three bogus targets and made
    ``root:secret@nas1,nas2`` a second target with no credentials at all.
    """
    prefix, hostpart = _split_userinfo(item)
    parts = [part for part in hostpart.split(",") if part]
    return [prefix + host for part in parts for host in expand(part)]


class CommandModule(_ty.Protocol):
    """The attributes the app expects from a command module."""

    def run(
        self, client: "TrueNASClient", args: PyTrueNASArgs, logger: _Logger
    ) -> object: ...


__all__ = [
    "PyTrueNASArgs",
    "CommandModule",
    "json_value",
    "json_default",
    "emit",
    "emit_json",
]
