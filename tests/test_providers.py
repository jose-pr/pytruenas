"""hostctl providers for a TrueNAS target (step 3 of the migration).

The load-bearing behaviour here is *declining honestly*: a provider that cannot
serve a request must say so via ``probe()``/``OperationNotStarted`` so hostctl's
selector falls through to the next one. These tests pin that, and pin the
SFTP -> websocket ordering the selector reproduces.
"""

import sys
from unittest.mock import MagicMock

import pytest

pytest.importorskip("hostctl")

from hostctl.provider import (  # noqa: E402
    ExecutorProvider,
    OperationNotStarted,
    PathProvider,
    ProviderSelector,
)

from pathlib_next import LocalPath  # noqa: E402

from pytruenas.providers import (  # noqa: E402
    WS_PATH_CAPABILITIES,
    TnasWsPathProvider,
    local_providers,
)


class _FakeConfig:
    def __init__(self, is_local):
        self.is_local = is_local


def _client(is_local=False):
    """A stand-in TrueNASClient.

    ``spec`` matters: a bare MagicMock auto-creates *every* attribute, including
    ``.client``, which the providers use to tell a host from a client. Without
    it a fake client would be mistaken for a host and unwrapped into its own
    auto-created child mock.
    """
    client = MagicMock(spec=["config", "_api", "api", "run", "path"])
    client.config = _FakeConfig(is_local)
    return client


# -- TnasWsPathProvider ----------------------------------------------------


def test_ws_path_provider_is_a_path_provider():
    provider = TnasWsPathProvider(_client())
    assert isinstance(provider, PathProvider)
    assert provider.name == "tnasws"


def test_ws_path_provider_is_always_available():
    # The middleware socket is the client's own connection: there is no
    # separate transport that could be down.
    for is_local in (True, False):
        assert TnasWsPathProvider(_client(is_local)).probe().usable


def test_ws_path_capabilities_exclude_what_the_api_cannot_do():
    """The websocket API has no symlink/rename/realpath -- do not claim them.

    Claiming them would make the selector pick this provider for operations it
    cannot perform, converting a clean fallback into a runtime failure.
    """
    for missing in ("rename", "symlink_to", "readlink", "resolve"):
        assert missing not in WS_PATH_CAPABILITIES
    # ...but the ordinary surface is claimed.
    for present in ("stat", "read", "write", "mkdir", "unlink", "rmdir"):
        assert present in WS_PATH_CAPABILITIES


def test_ws_path_provider_unwraps_a_host(monkeypatch):
    """A TrueNASHost passes *itself*; the fs layer needs the client.

    Regression: the host builds its providers with `self` (the client is
    created lazily from the host's own config), so a provider that assumed it
    held a client raised `AttributeError: no attribute '_api'` on the first
    `host.path(...)`. Caught only on a live target.
    """
    import pytruenas.fs as fs
    from pathlib_next import LocalPath

    seen = {}

    def fake_path(client, *segments, backend=None):
        seen["client"] = client
        return LocalPath("/etc/hostname")

    monkeypatch.setattr(fs, "path", fake_path)

    inner = _client()
    host_like = MagicMock()
    host_like.client = inner
    host_like.config = _FakeConfig(False)

    TnasWsPathProvider(host_like).path("/etc/hostname")
    assert seen["client"] is inner


def test_ws_path_provider_always_uses_the_websocket_backend(monkeypatch):
    """This provider is unconditionally the websocket leg.

    A *local* target is served by hostctl's own local path provider, which the
    host orders ahead of this one, so there is no local case to special-case
    here. (It used to switch to `backend="local"` itself -- necessary before
    the local provider existed, because `filesystem.get` routes reads through
    the HTTP side channel, which a unix-socket client cannot reach at all.)
    """
    import pytruenas.fs as fs

    seen = {}

    def fake_path(client, *segments, backend=None):
        seen["backend"] = backend
        return LocalPath("/etc/hostname")

    monkeypatch.setattr(fs, "path", fake_path)

    for is_local in (True, False):
        TnasWsPathProvider(_client(is_local=is_local)).path("/etc/hostname")
        assert seen["backend"] == "truenas"


def test_ws_path_provider_builds_a_ws_path(monkeypatch):
    import pytruenas.fs as fs
    from pathlib_next import LocalPath

    seen = {}
    # PathProvider validates that the factory returns a real pathlib_next.Path,
    # so the stand-in has to be one (LocalPath is the cheapest such value).
    sentinel = LocalPath("/etc/hosts")

    def fake_path(client, *segments, backend=None):
        seen["client"] = client
        seen["segments"] = segments
        seen["backend"] = backend
        return sentinel

    monkeypatch.setattr(fs, "path", fake_path)
    client = _client()
    assert TnasWsPathProvider(client).path("/etc/hosts") is sentinel
    # It must pin the backend explicitly: falling through to "auto" would let
    # this provider hand back an SFTP path, defeating the ordering.
    #
    # "truenas" rather than "ws": both ride the same TnasWsBackend, so the
    # transport is identical -- but TruenasPath carries the documented
    # `symlink_to(force=, onremove=)` extension and the SFTP->websocket
    # fallback that TnasWsPath lacks. Pinning "ws" silently narrowed the API.
    assert seen["backend"] == "truenas"
    assert seen["client"] is client


# -- local_providers -------------------------------------------------------
#
# pytruenas defines no executor provider of its own for a local target. There
# was one -- it wrapped hostctl's LocalExecutor behind an `is_local` guard and
# called itself MiddlewareExecutorProvider, which was doubly misleading:
# nothing about the dispatch involved middlewared, and the guard only repeated
# a decision the caller had already made. These tests pin that the stock
# hostctl pair is what gets used.


def test_local_providers_are_hostctls_own():
    from hostctl.executor import LocalExecutor

    executor, path = local_providers()
    assert isinstance(executor, ExecutorProvider)
    assert isinstance(path, PathProvider)
    assert executor.name == "local"
    assert path.name == "local"
    assert isinstance(executor.executor, LocalExecutor)


def test_local_executor_runs_a_command():
    executor, _ = local_providers()
    result = executor.execute(
        sys.executable,
        "-c",
        "print('hi')",
        capture_output=True,
        check=False,
        encoding="utf-8",
    )
    assert result.stdout.strip() == "hi"


def test_local_executor_declares_argv_support():
    """hostctl's LocalExecutor takes a real argv.

    Regression: a provider without the `args` capability gets the whole
    invocation as one string (``/bin/sh -c 'printf hi'``), which subprocess
    then looks up as a single literal filename -> FileNotFoundError. Caught
    only on a real POSIX target, because the Windows suite mocks the host.
    """
    executor, _ = local_providers()
    assert "args" in executor.capabilities


def test_local_path_provider_returns_a_real_path():
    from pathlib_next import Path

    _, path = local_providers()
    assert isinstance(path.path("/etc/hostname"), Path)


# -- selector integration --------------------------------------------------


def test_executor_order_prefers_local_then_ssh():
    """Local first: reaching this machine over SSH would be strictly worse."""
    local, _ = local_providers()
    ssh = ExecutorProvider("ssh", lambda *a, **k: "ran-over-ssh")

    selector = ProviderSelector((local, ssh))
    assert selector.select().provider is local

    # If the local leg is declined, the remote one still serves.
    selector.decline("local", "not this machine")
    assert selector.select().provider is ssh


def test_path_selector_prefers_sftp_then_websocket():
    """Ordering reproduces TruenasPath's SFTP-preferred behaviour."""
    sftp = PathProvider("sftp", lambda *s: LocalPath("/sftp-path"))
    ws = TnasWsPathProvider(_client())

    selector = ProviderSelector((sftp, ws))
    assert selector.select().provider is sftp

    # With SFTP declined (no SSH configured), the websocket leg serves.
    selector.decline("sftp", "no ssh configured")
    assert selector.select().provider is ws
