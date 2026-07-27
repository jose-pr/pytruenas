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

from pytruenas.providers import (  # noqa: E402
    WS_PATH_CAPABILITIES,
    MiddlewareExecutorProvider,
    TnasWsPathProvider,
)


class _FakeConfig:
    def __init__(self, is_local):
        self.is_local = is_local


def _client(is_local=False):
    client = MagicMock()
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
    # It must pin the websocket backend explicitly: falling through to "auto"
    # would let this provider hand back an SFTP path, defeating the ordering.
    assert seen["backend"] == "ws"
    assert seen["client"] is client


# -- MiddlewareExecutorProvider --------------------------------------------


def test_middleware_executor_is_an_executor_provider():
    provider = MiddlewareExecutorProvider(_client(True))
    assert isinstance(provider, ExecutorProvider)
    assert provider.name == "middleware"


def test_middleware_executor_available_only_when_local():
    assert MiddlewareExecutorProvider(_client(True)).probe().usable
    probe = MiddlewareExecutorProvider(_client(False)).probe()
    assert not probe.usable
    assert "remote command execution" in probe.reason


def test_middleware_executor_declines_remotely_without_dispatching():
    """Declining must use OperationNotStarted -- that is the failover signal.

    hostctl retries the next provider only when a provider proves it started no
    work; any other exception is treated as a real failure and propagates.
    """
    provider = MiddlewareExecutorProvider(_client(False))
    with pytest.raises(OperationNotStarted):
        provider.connect()
    with pytest.raises(OperationNotStarted):
        provider.execute("echo", "hi")


def test_middleware_executor_connect_is_a_noop_when_local():
    MiddlewareExecutorProvider(_client(True)).connect()


def test_middleware_executor_declares_args_capability():
    """Without ``args`` the whole invocation arrives as one string.

    Regression: hostctl renders ``/bin/sh -c 'printf hi'`` and, for a provider
    that cannot take argv, passes it as a *single* command. subprocess then
    looks that entire string up as one literal filename and raises
    FileNotFoundError. Declaring ``args`` makes the shell flavour split it into
    a real argv (``["/bin/sh", "-c", "printf hi"]``).

    This was caught only on a real POSIX target -- the Windows suite mocks the
    host, so every run() test passed while the provider was broken.
    """
    provider = MiddlewareExecutorProvider(_client(True))
    assert "args" in provider.capabilities


def test_middleware_executor_uses_hostctl_local_executor():
    """Dispatch must go through hostctl's executor, not a bare subprocess call.

    LocalExecutor owns input normalization against the stream mode, the
    extended capture_output convention, and the stdin/input conflict check.
    Reimplementing those here is how the bytes-input deadlock reappeared once.
    """
    from hostctl.executor import LocalExecutor

    provider = MiddlewareExecutorProvider(_client(True))
    result = provider.execute(
        sys.executable,
        "-c",
        "print('hi')",
        capture_output=True,
        check=False,
        encoding="utf-8",
    )
    assert result.stdout.strip() == "hi"
    assert isinstance(provider._executor, LocalExecutor)


def test_middleware_executor_reads_legacy_client_target():
    """A pre-migration client carries `_api`, not `config` -- still work."""
    client = MagicMock(spec=["_api"])
    client._api = MagicMock()
    client._api.is_local = True
    assert MiddlewareExecutorProvider(client).probe().usable


# -- selector integration --------------------------------------------------


def test_selector_falls_through_to_ssh_when_middleware_declines():
    """The whole point of step 3: an honest decline yields a clean fallback."""
    middleware = MiddlewareExecutorProvider(_client(False))
    ssh = ExecutorProvider("ssh", lambda *a, **k: "ran-over-ssh")

    selector = ProviderSelector((middleware, ssh))
    chosen = selector.select().provider
    # An unusable probe means the selector never even offers the middleware.
    assert chosen is ssh
    assert chosen.execute("echo") == "ran-over-ssh"


def test_selector_prefers_middleware_when_local():
    middleware = MiddlewareExecutorProvider(_client(True))
    ssh = ExecutorProvider("ssh", lambda *a, **k: "ran-over-ssh")

    selector = ProviderSelector((middleware, ssh))
    assert selector.select().provider is middleware


def test_path_selector_prefers_sftp_then_websocket():
    """Ordering reproduces TruenasPath's SFTP-preferred behaviour."""
    sftp = PathProvider("sftp", lambda *s: "sftp-path")
    ws = TnasWsPathProvider(_client())

    selector = ProviderSelector((sftp, ws))
    assert selector.select().provider is sftp

    # With SFTP declined (no SSH configured), the websocket leg serves.
    selector.decline("sftp", "no ssh configured")
    assert selector.select().provider is ws
