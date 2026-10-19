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
* It is a no-op when the dataset is already writable, or when the path is not
  on ZFS at all, so wrapping something that turns out not to need it costs a
  query or two and changes nothing.

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
import re as _re
import typing as _ty
from pathlib import PurePosixPath as _PurePosixPath

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from ..host import TrueNASClient

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
]


def host_path(path: "_ty.Union[str, _os.PathLike[str]]") -> str:
    """The plain filesystem path ``path`` names *on the host*.

    A remote path does not always stringify to something usable in a command
    line: ``str()`` on a ``uripath.URIPath`` gives a whole URI, and
    ``as_posix()`` gives scp syntax (``root@nas:/usr/lib/x``). ``os.fspath()``
    is the protocol for this: a ``client.path(...)`` composite answers with its
    logical path, and a URI path answers with the host path when its scheme is
    marked ``_host_filesystem_path`` -- ``sftp``, plus pytruenas' own
    ``truenas``/``truenas+ws`` (see :mod:`pytruenas.fs.tnasws`).

    A plain ``str`` passes through. Anything else raises whatever ``fspath``
    raises: a scheme that has not opted in has no host-local path, and
    inventing one from ``str()`` would put a URI into an argv.
    """
    if isinstance(path, str):
        return path
    return _os.fspath(path)


LOGGER = _logging.getLogger(__name__)


def dataset_for(
    client: "TrueNASClient", path: "_ty.Union[str, _os.PathLike[str]]"
) -> str:
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

    Raises ``ValueError`` naming the filesystem type when ``path`` is not on
    ZFS, and ``RuntimeError`` when the host answers for no ancestor.
    """
    fstype, source = _mount_for(client, path)
    if fstype != "zfs":
        raise ValueError(
            f"{path!r} is on a {fstype} filesystem ({source}), not a ZFS dataset"
        )
    return source


def _mount_for(
    client: "TrueNASClient", path: "_ty.Union[str, _os.PathLike[str]]"
) -> "tuple[str, str]":
    """``(FSTYPE, SOURCE)`` of the mount holding ``path`` or its nearest
    existing ancestor, as ``findmnt`` reports them."""
    # Walk with the path's own `.parent` when it has one (it keeps the type,
    # and so keeps `.path` meaningful); wrap a bare string in a POSIX pure path
    # so a Windows controller does not hand `\usr\lib` to the host.
    candidate = path if hasattr(path, "parent") else _PurePosixPath(path)
    tried: "list[str]" = []
    while True:
        target = host_path(candidate)
        tried.append(target)
        # --raw: columns split by one space, a space inside a value escaped.
        # --nofsroot: a bind mount's SOURCE without the "[/subdir]" suffix,
        # which no `zfs` command accepts.
        result = client.run(
            [
                "findmnt",
                "--noheadings",
                "--raw",
                "--nofsroot",
                "--output",
                "FSTYPE,SOURCE",
                "--target",
                target,
            ],
            capture_output="stdout",
            encoding="utf-8",
            check=False,
        )
        lines = result.stdout.strip().splitlines()
        fstype, _, source = lines[0].partition(" ") if lines else ("", "", "")
        if result.returncode == 0 and source:
            return _unescape(fstype), _unescape(source)
        parent = candidate.parent
        if host_path(parent) == target:  # reached "/" without an answer
            break
        candidate = parent

    raise RuntimeError(
        f"could not determine the dataset backing {path!r} "
        f"(tried: {', '.join(tried)})"
    )


def _unescape(value: str) -> str:
    """Undo the ``\\xNN`` escapes of ``findmnt --raw``."""
    return _re.sub(r"\\x([0-9a-fA-F]{2})", lambda m: chr(int(m.group(1), 16)), value)


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

    Returns ``default`` when ZFS prints ``-``, which means "unset or not
    applicable": an unset user property, or a native one that does not apply
    to this dataset (``origin`` on a dataset that is not a clone, ``volsize``
    on a filesystem). ``zfs get`` exits 0 for both, and still fails loudly for
    a bad dataset name.

    ``-H -o value`` asks for exactly one unheadered field; only the line end
    is removed, so a user property keeps its own surrounding spaces.
    """
    result = client.run(
        ["zfs", "get", "-H", "-o", "value", name, dataset],
        capture_output="stdout",
        encoding="utf-8",
        check=True,
    )
    value = result.stdout.rstrip("\r\n")
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
        prop, _, value = line.rstrip("\r").partition("\t")
        if value == _UNSET:
            continue
        values[prop.strip()] = value
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


#: User property set together with ``readonly=off`` while :func:`writable`
#: holds a dataset open. Its value says how to put ``readonly`` back (``on``:
#: set it locally; ``inherit``: ``zfs inherit`` it), so a window that never
#: closed -- a crash, a dropped connection -- is closed by the next one.
_RESTORE_MARK = "pytruenas:restore-readonly"


@_contextlib.contextmanager
def writable(
    client: "TrueNASClient", path: "_ty.Union[str, _os.PathLike[str]]"
) -> "_ty.Iterator[str]":
    """Make the dataset holding ``path`` writable for the duration.

    Yields the dataset name. Restores ``readonly`` on exit however the block
    ends -- leaving ``/usr`` writable because a patch raised halfway is exactly
    the failure this exists to prevent. The restore keeps the property's
    source: a ``readonly=on`` inherited from a parent is inherited again
    rather than set locally.

    A dataset that is already writable is left alone, and nothing is restored
    on exit: the flag is only ever put *back* to what it was found as, never
    set from scratch. A path that is not on ZFS is left alone too, and the
    yield is then the mount's source as ``findmnt`` names it.

    While the window is open the dataset carries the user property
    ``pytruenas:restore-readonly``. A later ``writable()`` that finds it on a
    writable dataset takes the window as left open, and restores on exit. Two
    windows over one dataset at the same time (two processes) are not
    coordinated: the first to close makes the dataset read-only for both.

    If the body raises and the restore fails too, the body's exception is the
    one raised and the restore failure is logged; after a body that
    completed, a failed restore raises.

        with writable(nas, "/usr/lib/python3/dist-packages/middlewared"):
            target.write(patched)
    """
    fstype, dataset = _mount_for(client, path)
    if fstype != "zfs":
        LOGGER.debug("%s is on %s (%s), not ZFS; nothing to do", path, fstype, dataset)
        yield dataset
        return

    readonly, source, pending = _readonly_state(client, dataset)
    if readonly == "on":
        restore = "inherit" if source in ("default", "inherited") else "on"
        set_properties(client, dataset, {"readonly": False, _RESTORE_MARK: restore})
    elif pending in ("on", "inherit"):
        LOGGER.warning(
            "%s is writable and carries %s=%s: an earlier window was left open, "
            "and readonly is restored when this one closes",
            dataset,
            _RESTORE_MARK,
            pending,
        )
        restore = pending
    else:
        LOGGER.debug("%s is already writable; nothing to do", dataset)
        yield dataset
        return

    body_failed = True
    try:
        yield dataset
        body_failed = False
    finally:
        try:
            _restore_readonly(client, dataset, restore)
        except Exception:
            # A silently writable root is worth a loud line of its own; the
            # body's exception, when there is one, is still the one raised.
            LOGGER.exception(
                "FAILED to restore readonly=on for %s -- it is still WRITABLE",
                dataset,
            )
            if not body_failed:
                raise


def _readonly_state(client: "TrueNASClient", dataset: str) -> "tuple[str, str, str]":
    """``(value, source, restore mark)`` of ``readonly`` on ``dataset``.

    ``source`` is its first word: ``local``, ``default``, ``inherited``
    (ZFS prints ``inherited from <parent>``), ``temporary`` or ``received``.
    """
    result = client.run(
        [
            "zfs",
            "get",
            "-H",
            "-o",
            "property,value,source",
            f"readonly,{_RESTORE_MARK}",
            dataset,
        ],
        capture_output="stdout",
        encoding="utf-8",
        check=True,
    )
    fields: "dict[str, tuple[str, str]]" = {}
    for line in result.stdout.splitlines():
        prop, _, rest = line.rstrip("\r").partition("\t")
        value, _, source = rest.partition("\t")
        fields[prop.strip()] = (value, source)
    value, source = fields.get("readonly", ("", ""))
    mark, _ = fields.get(_RESTORE_MARK, (_UNSET, ""))
    return value, source.split(" ", 1)[0], mark


def _restore_readonly(client: "TrueNASClient", dataset: str, restore: str) -> None:
    if restore == "inherit":
        inherit_property(client, dataset, "readonly")
    else:
        set_readonly(client, dataset, True)
    try:
        inherit_property(client, dataset, _RESTORE_MARK)
    except Exception:
        # readonly is back on; a mark left on a read-only dataset is ignored,
        # and the next window replaces it.
        LOGGER.warning("could not clear %s on %s", _RESTORE_MARK, dataset)
