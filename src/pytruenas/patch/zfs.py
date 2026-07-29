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

What this cannot protect you from: a boot environment swap on update discards
the whole dataset, patches included. Nothing here makes an unsupported change
supported -- it only makes it possible, and reversible while the system runs.
"""

from __future__ import annotations

import contextlib as _contextlib
import logging as _logging
import typing as _ty
from pathlib import PurePosixPath as _PurePosixPath

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from ..host import TrueNASHost as TrueNASClient

#: A path on the *host*: a ``client.path(...)`` instance or its string form.
PathLike = _ty.Union[str, "_ty.Any"]

__all__ = [
    "dataset_for",
    "is_readonly",
    "set_readonly",
    "writable",
    "host_path",
    "PathLike",
]


def host_path(path: "PathLike") -> str:
    """The plain filesystem path ``path`` names *on the host*.

    Needed because a remote path does not stringify to something you can put in
    a command line. A ``pathlib_next`` ``UriPath`` -- what the SFTP backend
    hands back -- renders three different wrong ways:

    * ``str()`` -> ``sftp://root@nas/usr/lib/x``: a whole URI, and one that
      **puts credentials in an argv** if the target carried any;
    * ``as_posix()`` -> ``root@nas:/usr/lib/x``: scp syntax, not a path;
    * ``os.fspath()`` -> ``NotImplementedError``.

    The real path is on ``.path``, so prefer that; fall back to ``as_posix()``
    for an ordinary pure path, and ``str()`` for a plain string.
    """
    inner = getattr(path, "path", None)
    if isinstance(inner, str):
        return inner
    as_posix = getattr(path, "as_posix", None)
    if callable(as_posix):
        return as_posix()
    return str(path)


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


def is_readonly(client: "TrueNASClient", dataset: str) -> bool:
    """Whether ``dataset`` has ``readonly=on``."""
    result = client.run(
        ["zfs", "get", "-H", "-o", "value", "readonly", dataset],
        capture_output="stdout",
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip() == "on"


def set_readonly(client: "TrueNASClient", dataset: str, readonly: bool) -> None:
    """Set ``readonly`` on ``dataset``. Takes effect immediately."""
    value = "on" if readonly else "off"
    LOGGER.info("Setting readonly=%s on %s", value, dataset)
    client.run(["zfs", "set", f"readonly={value}", dataset], check=True)


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
