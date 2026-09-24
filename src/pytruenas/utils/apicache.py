"""Fetch and cache the middleware API definition.

The API definition is the only machine-readable description of what a
middleware method accepts, and getting it off an appliance is harder than it
looks. Measured against TrueNAS 26.0.0-BETA.1:

* ``core.get_methods()`` makes the **server** close the websocket. That is not
  a timeout and not this client -- a raw ``websocket-client`` socket sending a
  hand-written JSON-RPC frame loses the connection the same way. There is no
  per-method accessor to fall back on either: ``core.get_methods("user.create")``
  returns ``{}`` (the argument is not a name filter) and
  ``core.get_method_info`` does not exist.
* ``middlewared --dump-api`` therefore is the source, and its output is
  **24,103,000 bytes** produced in about 75 seconds.
* Streaming that through a command channel's stdout loses a web shell
  connection outright, and fetching it through the ``filesystem.get`` HTTP side
  channel breaks mid-stream (``IncompleteRead``) at 23 MB *and* at 2 MB. So the
  side channel cannot be the transport, whatever the size.

What works is to compress on the target (``gzip -9`` takes it to 2,025,240
bytes, 11.9x) and pull the compressed file over a leg that can carry it:
:func:`fetch` prefers SFTP -- an in-process ``scp``, with no dependency on an
``scp`` or ``rsync`` binary existing locally -- and falls back to reading the
file in verified chunks through whatever command channel the host has, which is
what makes a host reachable only on 443 work at all.

Because that costs ~75 seconds and a couple of megabytes, the result is cached
per host and API version. :func:`load` is the entry point every consumer uses;
``generate-typings`` and the ``help`` command read the same cache.
"""

from __future__ import annotations

import gzip as _gzip
import hashlib as _hashlib
import json as _json
import os as _os
import pathlib as _pathlib
import typing as _ty

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from ..host import TrueNASHost
    from ..models.apidump import Api

#: Where the dump is built on the target. ``/var/db/system`` is a dataset on a
#: data pool, so it survives an update -- and unlike ``/tmp`` it is not mounted
#: ``noexec``. Only data is written here, but the same reasoning applies: a
#: boot environment swap would discard anything under ``/var/db`` itself.
REMOTE_DIR = "/var/db/system"

#: Bytes per chunk for the fallback fetch. Large enough that a 2 MB file is
#: eight round trips, small enough that a broken one is cheap to retry.
CHUNK_SIZE = 256 * 1024

#: Attempts per chunk before giving up on the whole fetch.
CHUNK_ATTEMPTS = 3


class ApiDumpError(RuntimeError):
    """The API definition could not be fetched or did not survive the trip."""


def cache_root() -> _pathlib.Path:
    """The directory cached dumps live in.

    ``$PYTRUENAS_CACHE`` wins; otherwise the platform's user cache directory.
    Read through :data:`pytruenas.utils.cmd.ENV` like every other setting, so
    the set of variables stays enumerable rather than grepped for.
    """
    from .cmd import ENV

    configured = ENV.get("CACHE")
    if configured:
        return _pathlib.Path(configured).expanduser()
    if _os.name == "nt":
        base = _os.environ.get("LOCALAPPDATA") or "~/AppData/Local"
        return _pathlib.Path(base).expanduser() / "pytruenas" / "cache"
    base = _os.environ.get("XDG_CACHE_HOME") or "~/.cache"
    return _pathlib.Path(base).expanduser() / "pytruenas"


def _safe_component(value: str) -> str:
    """A single path component that cannot escape the cache directory.

    A host label reaches this from a connection string, so it may hold a colon
    (``nas:8443``), a slash, or on Windows a drive letter. Anything outside a
    conservative set becomes ``_``.
    """
    keep = "-._"
    cleaned = "".join(c if (c.isalnum() or c in keep) else "_" for c in value)
    return cleaned.strip("._") or "unknown"


def path_for(host: str, version: str) -> _pathlib.Path:
    """The cache file for one host and API version."""
    return cache_root() / _safe_component(host) / f"{_safe_component(version)}.json.gz"


def _remote_paths(client: "TrueNASHost") -> "tuple[str, str]":
    # One name per connected host, not per call: a second fetch reuses (and
    # overwrites) it rather than littering the dataset.
    stem = f"{REMOTE_DIR}/pytruenas-apidump"
    return f"{stem}.json", f"{stem}.json.gz"


def _build_remote(client: "TrueNASHost") -> "tuple[str, int, str]":
    """Dump and compress on the target; return ``(gz_path, size, sha256)``."""
    raw, gz = _remote_paths(client)
    client.logger.info("Dumping the API definition on the target (this takes ~75s)")
    # `set -e` is not portable across every login shell here; check explicitly.
    result = client.run(
        f"middlewared --dump-api > {raw} && gzip -9 -f {raw} && "
        f"wc -c < {gz} && sha256sum {gz} | cut -d' ' -f1",
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode != 0:
        raise ApiDumpError(
            f"middlewared --dump-api failed on the target (rc={result.returncode}): "
            f"{(result.stderr or '').strip()[:400]}"
        )
    fields = (result.stdout or "").split()
    if len(fields) < 2 or not fields[0].isdigit():
        raise ApiDumpError(f"could not read the dump's size and digest: {fields!r}")
    size, digest = int(fields[0]), fields[1]
    client.logger.info("Dump compressed to %d bytes on the target", size)
    return gz, size, digest


def _fetch_sftp(client: "TrueNASHost", remote: str) -> "bytes | None":
    """Pull the file over SFTP, or ``None`` when this host has no such leg.

    This is the ``scp`` of the plan, done in process: the SFTP leg is already a
    path provider here, so it needs no external binary (Windows ships no
    ``rsync``, and depending on one would be a new requirement for something
    this package already owns).
    """
    try:
        return client.path(remote, backend="sftp").read_bytes()
    except ValueError:
        # `path(backend=...)` raises for a provider this host has not got --
        # no SSH leg configured, which is the ordinary web-shell-only case.
        return None
    except Exception as exc:  # noqa: BLE001 - any SFTP failure falls back
        client.logger.debug("SFTP fetch unavailable (%s); falling back", exc)
        return None


def _fetch_chunked(client: "TrueNASHost", remote: str, size: int) -> bytes:
    """Read the file in base64 chunks through the command channel.

    ``tail -c +N | head -c K`` rather than ``dd``: ``dd bs=1`` reads a byte at a
    time and is unusably slow over a PTY. Each chunk is retried, because the
    point of chunking is that a broken transfer costs one chunk instead of the
    whole file.
    """
    import base64 as _base64

    out = bytearray()
    offset = 0
    while offset < size:
        count = min(CHUNK_SIZE, size - offset)
        for attempt in range(1, CHUNK_ATTEMPTS + 1):
            try:
                encoded = client.run(
                    f"tail -c +{offset + 1} < {remote} | head -c {count} | base64 -w0",
                    capture_output=True,
                    encoding="utf-8",
                ).stdout
                chunk = _base64.b64decode(encoded)
                if len(chunk) != count:
                    raise ApiDumpError(
                        f"chunk at {offset} returned {len(chunk)} of {count} bytes"
                    )
                out += chunk
                break
            except Exception as exc:  # noqa: BLE001, PERF203
                if attempt == CHUNK_ATTEMPTS:
                    raise ApiDumpError(
                        f"chunk at offset {offset} failed after "
                        f"{CHUNK_ATTEMPTS} attempts: {exc}"
                    ) from exc
                client.logger.debug(
                    "retrying chunk at %d (attempt %d): %s", offset, attempt, exc
                )
        offset += count
    return bytes(out)


def fetch(client: "TrueNASHost", *, keep_remote: bool = False) -> "Api":
    """Build the API definition on the target and return the parsed dump.

    Raises :class:`ApiDumpError` when the transfer does not reproduce the
    target's own digest -- a truncated dump parses as nothing useful and would
    otherwise be cached as if it were real.
    """
    remote, size, digest = _build_remote(client)
    try:
        blob = _fetch_sftp(client, remote)
        how = "sftp"
        if blob is None:
            blob = _fetch_chunked(client, remote, size)
            how = "chunked"
        got = _hashlib.sha256(blob).hexdigest()
        if len(blob) != size or got != digest:
            raise ApiDumpError(
                f"fetched dump does not match the target ({how}): "
                f"{len(blob)} of {size} bytes, digest "
                f"{'matches' if got == digest else 'differs'}"
            )
        client.logger.info("Fetched the API definition over %s (%d bytes)", how, size)
        return _json.loads(_gzip.decompress(blob))
    finally:
        if not keep_remote:
            raw, gz = _remote_paths(client)
            client.run(f"rm -f {raw} {gz}", check=False)


def load(
    client: "TrueNASHost",
    *,
    refresh: bool = False,
    version: "str | None" = None,
) -> "Api":
    """Return the API definition for ``client``, from cache when possible.

    ``version`` names the appliance's version for cache keying; omitted, it is
    read with one cheap ``system.info()`` call. ``refresh=True`` re-fetches and
    overwrites. A cache file that cannot be read is treated as absent rather
    than fatal -- a corrupt cache should cost a re-fetch, not an error.
    """
    if version is None:
        version = str(client.api.system.info()["version"])
    cache = path_for(client.name, version)
    if not refresh and cache.exists():
        try:
            data = _json.loads(_gzip.decompress(cache.read_bytes()))
            client.logger.info("Using the cached API definition at %s", cache)
            return data
        except Exception as exc:  # noqa: BLE001
            client.logger.warning("Ignoring an unreadable cache at %s: %s", cache, exc)
    api = fetch(client)
    store(api, cache)
    client.logger.info("Cached the API definition at %s", cache)
    return api


def store(api: "Api", cache: "_pathlib.Path") -> None:
    """Write ``api`` to ``cache``, atomically and compressed."""
    cache.parent.mkdir(parents=True, exist_ok=True)
    # Written beside and renamed: an interrupted write must not leave a
    # half-file that the next run would read as a cache hit.
    tmp = cache.with_name(cache.name + ".part")
    tmp.write_bytes(_gzip.compress(_json.dumps(api).encode("utf-8"), 6))
    tmp.replace(cache)
