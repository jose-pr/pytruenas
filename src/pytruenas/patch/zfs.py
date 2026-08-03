"""Make a read-only part of the appliance temporarily writable.

TrueNAS mounts most of its root read-only -- ``/usr``, ``/opt``, ``/conf`` are
each a ZFS dataset with ``readonly=on`` set locally. Patching a file under one
means clearing that property first, and putting it back afterwards.

This is the sharpest edge in :mod:`pytruenas.patch`, so it is deliberately
narrow:

* :func:`dataset_for` answers *which* dataset a path lives on, by asking the
  host rather than guessing from the path.
* :func:`writable` is a context manager that flips ``readonly`` off and
  restores it on the way out -- **including when the body raises**, which is
  the entire reason it is a context manager and not two functions.
* It is a no-op when the dataset is already writable, so wrapping something
  that turns out not to need it costs one query and changes nothing.

Underneath those sits a general dataset property API -- :func:`get_property` /
:func:`set_property` (plus the batched :func:`get_properties` /
:func:`set_properties`, and :func:`inherit_property` to clear one). It handles
both native properties and ZFS *user* properties (``com.example:role``), which
are the way to attach your own metadata to a dataset: ZFS stores them verbatim
and they survive send/receive. ``readonly`` is just the one this module needs,
and its two helpers are thin wrappers over that API.

What this cannot protect you from: a boot environment swap on update discards
the whole dataset, patches included. Nothing here makes an unsupported change
supported -- it only makes it possible, and reversible while the system runs.
"""

from __future__ import annotations

import contextlib as _contextlib
import logging as _logging
import os as _os
import typing as _ty
from pathlib import PurePosixPath as _PurePosixPath

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from ..host import TrueNASHost as TrueNASClient

#: A path on the *host*: a ``client.path(...)`` instance or its string form.
PathLike = _ty.Union[str, "_ty.Any"]

__all__ = [
    "dataset_for",
    "get_properties",
    "get_property",
    "inherit_property",
    "is_readonly",
    "set_properties",
    "set_property",
    "set_readonly",
    "writable",
    "host_path",
    "PathLike",
]


def host_path(path: "PathLike") -> str:
    """The plain filesystem path ``path`` names *on the host*.

    A remote path does not stringify to something usable in a command line:
    ``str()`` on a ``UriPath`` gives a whole URI, and ``as_posix()`` gives scp
    syntax (``root@nas:/usr/lib/x``). ``os.fspath()`` is the protocol for this,
    and pathlib_next >=0.9.0 answers it with the host path for schemes marked
    ``_host_filesystem_path`` -- ``sftp``, plus pytruenas' own
    ``truenas``/``tnasws`` (see :mod:`pytruenas.fs.tnasws`).

    A plain ``str`` passes through. Anything else raises whatever ``fspath``
    raises: a scheme that has not opted in has no host-local path, and
    inventing one from ``str()`` would put a URI into an argv.
    """
    if isinstance(path, str):
        return path
    return _os.fspath(path)


LOGGER = _logging.getLogger(__name__)


def dataset_for(client: "TrueNASClient", path: "PathLike") -> str:
    """The ZFS dataset backing ``path``.

    ``path`` is a remote path -- a ``client.path(...)`` instance, or the string
    form of one. Both are accepted because callers hold one or the other
    depending on where they are: a :class:`~pytruenas.patch.templates.FileTarget`
    has a real path object, a caller writing a literal has a string.

    Asking the host beats deriving it from the path: ``/usr`` and
    ``/usr/local`` may be separate datasets, and the name carries the boot
    environment's version, which changes on every update.

    ``findmnt --target`` **fails on a path that does not exist**, which is the
    ordinary "create a new file here" case -- so this walks up to the nearest
    existing ancestor and asks about that. A file and the directory it will be
    created in are on the same dataset by definition.
    """
    # Walk with the path's own `.parent` when it has one (it keeps the type,
    # and so keeps `.path` meaningful); wrap a bare string in a POSIX pure path
    # so a Windows controller does not hand `\usr\lib` to the host.
    candidate = path if hasattr(path, "parent") else _PurePosixPath(path)
    tried: "list[str]" = []
    while True:
        target = host_path(candidate)
        tried.append(target)
        result = client.run(
            ["findmnt", "--noheadings", "--output", "SOURCE", "--target", target],
            capture_output="stdout",
            encoding="utf-8",
            check=False,
        )
        dataset = result.stdout.strip()
        if result.returncode == 0 and dataset:
            return dataset
        parent = candidate.parent
        if host_path(parent) == target:  # reached "/" without an answer
            break
        candidate = parent

    raise RuntimeError(
        f"could not determine the dataset backing {path!r} "
        f"(tried: {', '.join(tried)})"
    )


#: What ``zfs get`` prints for a property that has no value set. ZFS uses this
#: for an unset *user* property rather than failing, so it is a value to
#: recognise, not an error to raise.
_UNSET = "-"


def get_property(
    client: "TrueNASClient",
    dataset: str,
    name: str,
    *,
    default: "str | None" = None,
) -> "str | None":
    """The value of ZFS property ``name`` on ``dataset``.

    Works for both kinds of property ZFS has: a native one (``readonly``,
    ``compression``, ``mountpoint``) and a *user* property, which is any name
    containing a colon (``com.example:role``). User properties are the ones
    worth setting on a dataset to carry your own metadata -- ZFS stores them
    verbatim, and they survive send/receive.

    Returns ``default`` when the property is unset. ZFS prints ``-`` for an
    unset user property (and exits 0), so "absent" is a value here rather than
    an error; a *native* property is never absent, so this only bites for user
    properties. ``zfs get`` still fails loudly for a bad dataset name.

    ``-H -o value`` asks for exactly one unheadered field, so the result needs
    no parsing beyond a strip.
    """
    result = client.run(
        ["zfs", "get", "-H", "-o", "value", name, dataset],
        capture_output="stdout",
        encoding="utf-8",
        check=True,
    )
    value = result.stdout.strip()
    return default if value == _UNSET else value


def get_properties(
    client: "TrueNASClient",
    dataset: str,
    names: "_ty.Sequence[str]",
) -> "dict[str, str]":
    """Several ZFS properties of ``dataset`` at once, as ``{name: value}``.

    One ``zfs get`` for the whole set rather than one per property -- over a
    websocket or SSH leg the round trip dominates, so asking for five properties
    individually is five times the latency for the same data.

    Unset properties are **omitted** from the mapping rather than mapped to
    ``None``, so a caller can use ``in`` / ``.get(...)`` to distinguish "not
    set" without a sentinel. Passing no names returns an empty mapping without
    calling the host (``zfs get`` with an empty property list is an error).
    """
    if not names:
        return {}
    result = client.run(
        ["zfs", "get", "-H", "-o", "property,value", ",".join(names), dataset],
        capture_output="stdout",
        encoding="utf-8",
        check=True,
    )
    values: "dict[str, str]" = {}
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        # -H separates fields with a single tab; a value may itself contain
        # spaces, so split on tab and only once.
        prop, _, value = line.partition("\t")
        if value.strip() == _UNSET:
            continue
        values[prop.strip()] = value.strip()
    return values


def set_property(
    client: "TrueNASClient",
    dataset: str,
    name: str,
    value: "str | bool",
) -> None:
    """Set ZFS property ``name`` to ``value`` on ``dataset``.

    Takes effect immediately. ``True``/``False`` are written as ZFS' own
    ``on``/``off`` so a caller does not have to spell those for boolean
    properties; any other value is passed through as its string form.

    As with :func:`get_property`, a name containing a colon is a user property
    and may be any string.
    """
    rendered = _render(value)
    LOGGER.info("Setting %s=%s on %s", name, rendered, dataset)
    client.run(["zfs", "set", f"{name}={rendered}", dataset], check=True)


def set_properties(
    client: "TrueNASClient",
    dataset: str,
    properties: "_ty.Mapping[str, str | bool]",
) -> None:
    """Set several ZFS properties on ``dataset`` in one call.

    ``zfs set`` accepts multiple ``name=value`` pairs, and applying them
    together is both one round trip and one atomic-ish change, rather than a
    window where half the properties are set. Does nothing when ``properties``
    is empty.
    """
    if not properties:
        return
    pairs = [f"{name}={_render(value)}" for name, value in properties.items()]
    LOGGER.info("Setting %s on %s", ", ".join(pairs), dataset)
    client.run(["zfs", "set", *pairs, dataset], check=True)


def inherit_property(
    client: "TrueNASClient",
    dataset: str,
    name: str,
    *,
    received: bool = False,
) -> None:
    """Clear ``name`` on ``dataset``, reverting to inherited/default.

    This is how a property is *removed*: there is no ``zfs unset``. For a user
    property the result is genuinely absent (:func:`get_property` returns its
    ``default`` again); for a native one it reverts to the parent's value or the
    ZFS default.

    ``received=True`` (``zfs inherit -S``) reverts to the value received with a
    ``zfs send``/``recv`` stream instead of clearing outright.
    """
    argv = ["zfs", "inherit"]
    if received:
        argv.append("-S")
    argv += [name, dataset]
    LOGGER.info(
        "Clearing %s on %s%s", name, dataset, " (to received)" if received else ""
    )
    client.run(argv, check=True)


def _render(value: "str | bool") -> str:
    """A ZFS property value as ``zfs set`` wants it (``bool`` -> ``on``/``off``)."""
    if isinstance(value, bool):
        return "on" if value else "off"
    return str(value)


def is_readonly(client: "TrueNASClient", dataset: str) -> bool:
    """Whether ``dataset`` has ``readonly=on``."""
    return get_property(client, dataset, "readonly") == "on"


def set_readonly(client: "TrueNASClient", dataset: str, readonly: bool) -> None:
    """Set ``readonly`` on ``dataset``. Takes effect immediately."""
    set_property(client, dataset, "readonly", readonly)


@_contextlib.contextmanager
def writable(client: "TrueNASClient", path: "PathLike") -> "_ty.Iterator[str]":
    """Make the dataset holding ``path`` writable for the duration.

    Yields the dataset name. Restores the original ``readonly`` value on exit
    however the block ends -- leaving ``/usr`` writable because a patch raised
    halfway is exactly the failure this exists to prevent.

    A dataset that is already writable is left alone, and nothing is restored
    on exit: the flag is only ever put *back* to what it was found as, never
    set from scratch.

        with writable(nas, "/usr/lib/python3/dist-packages/middlewared"):
            target.write(patched)
    """
    dataset = dataset_for(client, path)
    was_readonly = is_readonly(client, dataset)
    if not was_readonly:
        LOGGER.debug("%s is already writable; nothing to do", dataset)
        yield dataset
        return

    set_readonly(client, dataset, False)
    try:
        yield dataset
    finally:
        # Best-effort restore: if putting it back fails we must still surface
        # the original exception, but a silently-writable root is worth a loud
        # log line of its own.
        try:
            set_readonly(client, dataset, True)
        except Exception:  # pragma: no cover - needs a host that fails here
            LOGGER.exception(
                "FAILED to restore readonly=on for %s -- it is still WRITABLE",
                dataset,
            )
            raise
