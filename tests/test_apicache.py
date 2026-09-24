"""The API-definition cache and the two ways of fetching a dump.

The transport facts these pin down were measured against TrueNAS
26.0.0-BETA.1: the dump is 24 MB raw and ~2 MB gzipped, streaming it through a
command channel's stdout loses a web shell connection, and the HTTP side
channel truncates it. So every test here is about *not* trusting a transfer:
the digest is checked, a short chunk is retried, and a truncated result is an
error rather than a cache entry.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess

import pytest

from pytruenas.utils import apicache

API = {"versions": [{"version": "26.0.0-BETA.1", "methods": [], "events": []}]}
BLOB = gzip.compress(json.dumps(API).encode("utf-8"))
DIGEST = hashlib.sha256(BLOB).hexdigest()


class FakeClient:
    """Enough of a host for apicache: ``run``, ``path``, ``logger``, ``name``."""

    def __init__(self, *, sftp=None, chunk_failures=0, blob=BLOB):
        self.name = "nas1"
        self.logger = __import__("logging").getLogger("test.apicache")
        self.commands: "list[str]" = []
        self._sftp = sftp
        self._blob = blob
        self._chunk_failures = chunk_failures
        self.api = self  # so client.api.system.info() resolves below
        self.system = self

    # -- the middleware call `load()` makes for the cache key ---------------
    def info(self):
        return {"version": "26.0.0-BETA.1"}

    # -- command channel ---------------------------------------------------
    def run(self, cmd, **kwargs):
        self.commands.append(cmd)
        if "--dump-api" in cmd:
            out = f"{len(self._blob)}\n{DIGEST}\n"
            return subprocess.CompletedProcess(cmd, 0, out, "")
        if "tail -c" in cmd:
            import base64
            import re

            start = int(re.search(r"tail -c \+(\d+)", cmd).group(1)) - 1
            count = int(re.search(r"head -c (\d+)", cmd).group(1))
            if self._chunk_failures:
                # Fail the FIRST attempt of the first chunk only: a retry that
                # is never exercised is a retry that does not work.
                self._chunk_failures -= 1
                raise OSError("channel hiccup")
            piece = self._blob[start : start + count]
            return subprocess.CompletedProcess(
                cmd, 0, base64.b64encode(piece).decode(), ""
            )
        return subprocess.CompletedProcess(cmd, 0, "", "")

    # -- path providers ----------------------------------------------------
    def path(self, remote, backend=None):
        if self._sftp is None:
            # What `Host.path` raises for a provider this host has not got.
            raise ValueError(f"unknown path provider: {backend!r}")
        return self._sftp


class FakePath:
    def __init__(self, blob):
        self._blob = blob

    def read_bytes(self):
        return self._blob


def test_cache_path_is_per_host_and_version(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTRUENAS_CACHE", str(tmp_path))
    path = apicache.path_for("nas1", "26.0.0-BETA.1")
    assert path == tmp_path / "nas1" / "26.0.0-BETA.1.json.gz"


@pytest.mark.parametrize(
    "host, expected",
    [
        ("nas1:8443", "nas1_8443"),
        ("../../etc", "etc"),
        ("a/b", "a_b"),
        ("", "unknown"),
    ],
)
def test_a_host_label_cannot_escape_the_cache_directory(
    host, expected, tmp_path, monkeypatch
):
    # The label comes from a connection string, so it may hold a colon, a slash
    # or a traversal. Writing outside the cache dir would be the bug.
    monkeypatch.setenv("PYTRUENAS_CACHE", str(tmp_path))
    path = apicache.path_for(host, "26.0")
    assert path.parent.name == expected
    assert tmp_path in path.parents


def test_fetch_prefers_sftp_and_verifies_the_digest():
    client = FakeClient(sftp=FakePath(BLOB))
    assert apicache.fetch(client) == API
    # gzip on the target, and the temporary files cleaned up afterwards.
    assert any("gzip -9" in c for c in client.commands)
    assert any(c.startswith("rm -f ") for c in client.commands)
    # Nothing was read in chunks: SFTP carried it.
    assert not any("tail -c" in c for c in client.commands)


def test_fetch_falls_back_to_chunks_without_an_ssh_leg():
    client = FakeClient(sftp=None)
    assert apicache.fetch(client) == API
    assert any("tail -c" in c for c in client.commands)


def test_a_failed_chunk_is_retried():
    client = FakeClient(sftp=None, chunk_failures=1)
    assert apicache.fetch(client) == API


def test_a_chunk_that_keeps_failing_is_an_error_not_a_short_dump():
    client = FakeClient(sftp=None, chunk_failures=apicache.CHUNK_ATTEMPTS)
    with pytest.raises(apicache.ApiDumpError, match="offset 0 failed"):
        apicache.fetch(client)


def test_every_command_carries_a_timeout():
    """A stalled channel must not hang the call.

    The web shell waits *forever* by default, so an unbounded `run()` turns a
    stalled PTY into an indefinite wait and the chunk retry never gets a turn.
    Measured the hard way: a 17-minute wait that burned 0.5 s of CPU.
    """
    timeouts = []

    class Recording(FakeClient):
        def run(self, cmd, **kwargs):
            timeouts.append((cmd.split()[0], kwargs.get("timeout")))
            return super().run(cmd, **kwargs)

    client = Recording(sftp=None)
    apicache.fetch(client)
    assert timeouts, "no commands ran"
    for first_word, timeout in timeouts:
        assert timeout is not None, f"{first_word} ran without a timeout"


def test_a_chunk_that_times_out_is_retried():
    # subprocess.TimeoutExpired is what a bounded `run()` raises, and it has to
    # be retryable like any other transport failure.
    class Stalling(FakeClient):
        def __init__(self):
            super().__init__(sftp=None)
            self._stalled = False

        def run(self, cmd, **kwargs):
            if "tail -c" in cmd and not self._stalled:
                self._stalled = True
                raise subprocess.TimeoutExpired(cmd, kwargs.get("timeout") or 1)
            return super().run(cmd, **kwargs)

    assert apicache.fetch(Stalling()) == API


def test_failing_cleanup_does_not_mask_the_result():
    # Removing the temporary files is courtesy; the next fetch overwrites them.
    class BadCleanup(FakeClient):
        def run(self, cmd, **kwargs):
            if cmd.startswith("rm -f"):
                raise OSError("channel gone")
            return super().run(cmd, **kwargs)

    assert apicache.fetch(BadCleanup(sftp=FakePath(BLOB))) == API


def test_a_truncated_transfer_is_refused():
    # The HTTP side channel really did return a short read; a dump that does
    # not match the target's digest must never be returned or cached.
    client = FakeClient(sftp=FakePath(BLOB[:-20]))
    with pytest.raises(apicache.ApiDumpError, match="does not match the target"):
        apicache.fetch(client)


def test_a_failed_dump_reports_the_targets_error():
    client = FakeClient(sftp=FakePath(BLOB))

    def failing(cmd, **kwargs):
        client.commands.append(cmd)
        return subprocess.CompletedProcess(cmd, 127, "", "middlewared: not found")

    client.run = failing
    with pytest.raises(apicache.ApiDumpError, match="not found"):
        apicache.fetch(client)


def test_load_writes_then_reuses_the_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTRUENAS_CACHE", str(tmp_path))
    client = FakeClient(sftp=FakePath(BLOB))
    assert apicache.load(client) == API
    first = list(client.commands)
    assert any("--dump-api" in c for c in first)

    # Second call: cache hit, so the target is not touched at all.
    client.commands.clear()
    assert apicache.load(client) == API
    assert client.commands == []

    # ... and refresh=True does go back to the target.
    assert apicache.load(client, refresh=True) == API
    assert any("--dump-api" in c for c in client.commands)


def test_an_unreadable_cache_costs_a_refetch_not_an_error(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTRUENAS_CACHE", str(tmp_path))
    cache = apicache.path_for("nas1", "26.0.0-BETA.1")
    cache.parent.mkdir(parents=True)
    cache.write_bytes(b"not gzip at all")
    client = FakeClient(sftp=FakePath(BLOB))
    assert apicache.load(client) == API
    # It was replaced with a good one.
    assert json.loads(gzip.decompress(cache.read_bytes())) == API


def test_store_leaves_no_partial_file(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTRUENAS_CACHE", str(tmp_path))
    cache = apicache.path_for("nas1", "26.0")
    apicache.store(API, cache)
    assert cache.exists()
    assert not list(cache.parent.glob("*.part"))
