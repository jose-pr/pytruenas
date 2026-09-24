"""Fetch and cache the middleware API definition.

The API definition is the only machine-readable description of what a
middleware method accepts. There are two ways to get it, and the cheap one is
the default.

**Per service, over the API** -- :func:`service_methods` and :func:`services`,
built on ``core.get_methods(<service>)`` and ``core.get_services``. Both declare
**no roles** and need **no command access**, so they work for an API-key account
with no shell, no SSH and no web shell -- which plenty of accounts are. One
namespace is a small answer: measured on 26.0, ``user`` is 13 methods / 100 KB /
14.5 s, ``network.configuration`` 3 methods / 18 KB / 1.9 s, and
``core.get_services`` 121 services / 79 KB / 5.5 s.

Note the filter is by **service**, not by method name --
``core.get_methods("user.create")`` returns ``{}``, which is what made this
whole route look like a dead end at first. Asking for everything at once
(``core.get_methods()`` with no argument) is also not an option: the **server**
closes the websocket on that payload, and not because of this client -- a raw
``websocket-client`` socket sending a hand-written JSON-RPC frame loses the
connection the same way.

**The whole definition** -- :func:`load`/:func:`fetch`, built on ``middlewared
--dump-api``. This needs command access and is 24,103,000 bytes produced in
about 75 s, so it is the fallback, not the default. It is still the only source
for *older* API versions, which the live API cannot report, and it is what
``generate-typings`` consumes.

Moving that 24 MB is its own problem. Streaming it through a command channel's
stdout loses a web shell connection outright, and the ``filesystem.get`` HTTP
side channel breaks mid-stream (``IncompleteRead``) at 23 MB *and* at 2 MB, so
the side channel cannot be the transport whatever the size. What works: compress
on the target (``gzip -9`` gives 2,025,240 bytes, 11.9x) and pull the compressed
file over a leg that can carry it -- SFTP when the host has an SSH leg (an
in-process ``scp``, needing no ``scp``/``rsync`` binary), else verified 256 KiB
chunks through the command channel, which is what carries a host reachable only
on 443.

Everything is cached under ``$PYTRUENAS_CACHE``, per host and API version, with
per-service answers in their own small files beside the dump's.
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

#: Seconds allowed for the dump-and-compress command. Generous: it took ~75 s on
#: 26.0 and an appliance under load takes longer.
DUMP_TIMEOUT = 900

#: Seconds allowed for **one** chunk. Every command here needs a timeout,
#: because the web shell waits *forever* by default -- a stalled PTY session
#: otherwise hangs the whole call and the retry below never gets a turn (which
#: is exactly what it did: a 17-minute wait burning 0.5 s of CPU, indefinite
#: rather than slow).
CHUNK_TIMEOUT = 180

#: Seconds allowed for removing the temporary files.
CLEANUP_TIMEOUT = 60

#: Seconds allowed for one ``core.get_methods``/``core.get_services`` call. The
#: default per-call timeout is 60 and a big namespace really takes longer:
#: ``pool.dataset`` measured 36.9 s and 348 KB on 26.0.
SERVICE_TIMEOUT = 300


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
        timeout=DUMP_TIMEOUT,
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
    chunks = (size + CHUNK_SIZE - 1) // CHUNK_SIZE
    client.logger.info(
        "Fetching %d bytes in %d chunk(s) through the command channel", size, chunks
    )
    while offset < size:
        count = min(CHUNK_SIZE, size - offset)
        # Progress matters here: this is minutes of work over a PTY, and a silent
        # wait is indistinguishable from the hang this used to be.
        client.logger.info(
            "chunk %d/%d (%d bytes at %d)",
            offset // CHUNK_SIZE + 1,
            chunks,
            count,
            offset,
        )
        for attempt in range(1, CHUNK_ATTEMPTS + 1):
            try:
                encoded = client.run(
                    f"tail -c +{offset + 1} < {remote} | head -c {count} | base64 -w0",
                    capture_output=True,
                    encoding="utf-8",
                    timeout=CHUNK_TIMEOUT,
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
            try:
                client.run(f"rm -f {raw} {gz}", check=False, timeout=CLEANUP_TIMEOUT)
            except Exception as exc:  # noqa: BLE001
                # Cleanup is courtesy: failing it must not mask the fetch's own
                # result (or its exception), and the next fetch overwrites these.
                client.logger.debug("could not remove %s/%s: %s", raw, gz, exc)


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


def _version_of(client: "TrueNASHost") -> str:
    return str(client.api.system.info()["version"])


def _sibling(client: "TrueNASHost", version: str, kind: str) -> "_pathlib.Path":
    """A cache file beside the dump's, named for what it holds.

    ``<version>.<kind>.json.gz`` -- built from the version rather than from
    ``path_for``'s filename, which already carries ``.json.gz`` and would
    otherwise double it (``26.0.json.services.json.gz``).
    """
    return path_for(client.name, version).with_name(
        f"{_safe_component(version)}.{kind}.json.gz"
    )


def services(client: "TrueNASHost", *, refresh: bool = False) -> "dict":
    """Every service (namespace) the appliance exposes, via ``core.get_services``.

    Shell-free and role-free, so this works for an API-key account that cannot
    run commands at all. 121 services / 79 KB / ~5.5 s measured on 26.0.
    """
    cache = _sibling(client, _version_of(client), "services")
    if not refresh and cache.exists():
        try:
            return _json.loads(_gzip.decompress(cache.read_bytes()))
        except Exception as exc:  # noqa: BLE001
            client.logger.warning("Ignoring an unreadable cache at %s: %s", cache, exc)
    client.logger.info("Listing services (core.get_services)")
    found = client.api.core.get_services(_timeout=SERVICE_TIMEOUT)
    store(found, cache)
    return found


def service_methods(
    client: "TrueNASHost", service: str, *, refresh: bool = False
) -> "dict":
    """The methods of one service, via ``core.get_methods(service)``.

    **This is the shell-free path, and the one to prefer.** ``core.get_methods``
    declares no roles and filters by *service* (a namespace -- passing a method
    name returns ``{}``, which is what made it look useless at first), so a
    single namespace is a small payload: 13 methods / 100 KB / 14.5 s for
    ``user`` on 26.0, against 24 MB and ~75 s plus a shell for the whole dump.

    That matters for more than speed: `middlewared --dump-api` needs command
    access, and an API-key account may have no shell, no SSH and no web shell at
    all. This path needs none of them.

    The envelope differs from the dump's (``accepts``/``returns``/``description``
    rather than ``schemas``); :func:`pytruenas.utils.apihelp.from_get_methods`
    normalizes it.

    Asking for the whole set at once (``core.get_methods()`` with no service) is
    **not** an option: the server closes the websocket on that payload.
    """
    version = _version_of(client)
    cache = _sibling(client, version, f"svc.{_safe_component(service)}")
    if not refresh and cache.exists():
        try:
            data = _json.loads(_gzip.decompress(cache.read_bytes()))
            client.logger.debug("Using the cached methods for %s", service)
            return data
        except Exception as exc:  # noqa: BLE001
            client.logger.warning("Ignoring an unreadable cache at %s: %s", cache, exc)
    client.logger.info("Fetching the methods of %s (core.get_methods)", service)
    found = client.api.core.get_methods(service, _timeout=SERVICE_TIMEOUT)
    if not found:
        raise LookupError(
            f"no service named {service!r} (core.get_methods filters by SERVICE, "
            "not by method name)"
        )
    store(found, cache)
    return found


def store(api: "Api", cache: "_pathlib.Path") -> None:
    """Write ``api`` to ``cache``, atomically and compressed."""
    cache.parent.mkdir(parents=True, exist_ok=True)
    # Written beside and renamed: an interrupted write must not leave a
    # half-file that the next run would read as a cache hit.
    tmp = cache.with_name(cache.name + ".part")
    tmp.write_bytes(_gzip.compress(_json.dumps(api).encode("utf-8"), 6))
    tmp.replace(cache)
